"""
Модуль главного окна приложения.
Объединяет все компоненты и обеспечивает их взаимодействие.
"""

import os
from typing import Optional
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QSplitter, 
    QTabWidget, QGroupBox, QApplication, QMenuBar
)
from PySide6.QtCore import Qt, QSettings, QTimer
from PySide6.QtGui import QAction, QPixmap

from config import AppSettings, SettingsManager
from styles import ModernStyle
from preview_canvas import AdvancedTextPreviewCanvas
from gcode_generator import SmartGCodeGenerator, GCodeValidator
from ui_components import (
    EditorPanel, PageSettingsTab, TextSettingsTab, SmartFormattingTab, 
    ExportTab, NavigationWidget, BackgroundControlWidget,
    show_error_message, show_info_message, show_warning_message,
    get_save_file_name, get_open_file_name, get_directory
)
from text_formatter import SmartFormatter


class NotesToGCodeStudioPro(QMainWindow):
    """Профессиональная версия Notes to G-code Studio"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Notes → G-code Studio Pro - Умное форматирование")
        self.setGeometry(50, 50, 1600, 1000)
        
        # Настройки
        self.qt_settings = QSettings("NotesToGCodePro", "Settings")
        self.settings_manager = SettingsManager(self.qt_settings)
        self.app_settings = self.settings_manager.load_app_settings()
        
        # Проверка настроек
        is_valid, errors = self.app_settings.validate_all()
        if not is_valid:
            show_warning_message(self, "Предупреждение", 
                               f"Обнаружены проблемы в настройках:\n" + "\n".join(errors))
        
        # Установка темы
        self.setStyleSheet(ModernStyle.get_dark_stylesheet())
        
        # Создание UI
        self.setup_menu()
        self.setup_ui()
        self.setup_connections()
        
        # Инициализация
        self.gcode_generator = None
        
        # Первоначальная генерация сетки
        QTimer.singleShot(100, self.generate_grid)
        
    def setup_menu(self):
        """Создание меню"""
        menubar = self.menuBar()
        
        # Меню файл
        file_menu = menubar.addMenu("Файл")
        
        open_action = QAction("Открыть текст", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_text_file)
        file_menu.addAction(open_action)
        
        save_action = QAction("Сохранить текст", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_text_file)
        file_menu.addAction(save_action)
        
        file_menu.addSeparator()
        
        export_gcode_action = QAction("Экспорт G-code", self)
        export_gcode_action.setShortcut("Ctrl+E")
        export_gcode_action.triggered.connect(self.export_gcode)
        file_menu.addAction(export_gcode_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("Выход", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Меню вид
        view_menu = menubar.addMenu("Вид")
        
        prev_page_action = QAction("Предыдущая страница", self)
        prev_page_action.setShortcut("Ctrl+Left")
        prev_page_action.triggered.connect(self.prev_page)
        view_menu.addAction(prev_page_action)
        
        next_page_action = QAction("Следующая страница", self)
        next_page_action.setShortcut("Ctrl+Right")
        next_page_action.triggered.connect(self.next_page)
        view_menu.addAction(next_page_action)
        
        # Меню помощь
        help_menu = menubar.addMenu("Помощь")
        
        about_action = QAction("О программе", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def setup_ui(self):
        """Настройка интерфейса"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout(central_widget)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        # Левая панель - редактор
        self.editor_panel = EditorPanel()
        
        # Правая панель - предпросмотр и настройки
        right_panel = self.create_preview_and_settings_panel()
        
        # Сплиттер
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.editor_panel)
        splitter.addWidget(right_panel)
        splitter.setStretchFactor(0, 2)
        splitter.setStretchFactor(1, 3)
        splitter.setSizes([600, 1000])
        
        main_layout.addWidget(splitter)
    
    def create_preview_and_settings_panel(self):
        """Создание панели предпросмотра и настроек"""
        panel = QWidget()
        layout = QHBoxLayout(panel)
        layout.setSpacing(10)
        
        # Предпросмотр (левая часть)
        preview_group = QGroupBox("🔍 Умный предпросмотр")
        preview_layout = QVBoxLayout(preview_group)
        
        # Навигация по страницам
        self.navigation_widget = NavigationWidget()
        preview_layout.addWidget(self.navigation_widget)
        
        # Canvas предпросмотра
        self.preview_canvas = AdvancedTextPreviewCanvas()
        self.preview_canvas.update_settings(
            self.app_settings.page,
            self.app_settings.text,
            self.app_settings.page_numbers
        )
        preview_layout.addWidget(self.preview_canvas)
        
        # Управление фоном
        self.background_control = BackgroundControlWidget()
        preview_layout.addWidget(self.background_control)
        
        # Вкладки настроек (правая часть)
        self.settings_tabs = QTabWidget()
        
        # Вкладка страницы
        self.page_tab = PageSettingsTab(self.app_settings.page)
        self.settings_tabs.addTab(self.page_tab, "📄 Страница")
        
        # Вкладка текста
        self.text_tab = TextSettingsTab(self.app_settings.text)
        self.settings_tabs.addTab(self.text_tab, "✏️ Текст")
        
        # Вкладка умного форматирования
        self.smart_tab = SmartFormattingTab(
            self.app_settings.text,
            self.app_settings.page_numbers
        )
        self.settings_tabs.addTab(self.smart_tab, "🧠 Умное форматирование")
        
        # Вкладка экспорта
        self.export_tab = ExportTab()
        self.settings_tabs.addTab(self.export_tab, "📤 Экспорт")
        
        # Добавляем виджеты в горизонтальный layout
        layout.addWidget(preview_group, 2)  # Предпросмотр занимает 2 части
        layout.addWidget(self.settings_tabs, 1)  # Вкладки занимают 1 часть
        
        return panel
    
    def setup_connections(self):
        """Настройка соединений сигналов"""
        # Редактор текста
        self.editor_panel.text_changed.connect(self.on_text_changed)
        
        # Навигация
        self.navigation_widget.prev_page.connect(self.prev_page)
        self.navigation_widget.next_page.connect(self.next_page)
        
        # Управление фоном
        self.background_control.generate_grid.connect(self.generate_grid)
        self.background_control.import_background.connect(self.import_background)
        self.background_control.clear_background.connect(self.clear_background)
        
        # Настройки
        self.page_tab.settings_changed.connect(self.update_page_settings)
        self.text_tab.settings_changed.connect(self.update_text_settings)
        self.smart_tab.settings_changed.connect(self.update_smart_settings)
        
        # Экспорт
        self.export_tab.export_gcode_requested.connect(self.export_gcode)
        self.export_tab.export_image_requested.connect(self.export_image)
        self.export_tab.export_all_pages_requested.connect(self.export_all_pages)
    
    def on_text_changed(self, text: str):
        """Обработка изменения текста"""
        # Обновление предпросмотра
        self.preview_canvas.set_text(text)
        
        # Обновление количества страниц в редакторе
        page_count = self.preview_canvas.get_page_count()
        self.editor_panel.update_page_count(page_count)
        
        # Обновление навигации
        self.update_navigation()
        
        # Обновление статуса экспорта
        stats = self.preview_canvas.get_text_statistics()
        if stats['characters'] > 0:
            self.export_tab.set_status(
                f"Готов к экспорту: {stats['words']} слов, {stats['pages']} страниц"
            )
        else:
            self.export_tab.set_status("Готов к экспорту")
        
        # Предпросмотр G-code с задержкой
        QTimer.singleShot(1000, self.generate_gcode_preview)
        
        # Обновление информации об адаптивном шрифте
        self.update_adaptive_font_info()
    
    def update_page_settings(self):
        """Обновление настроек страницы"""
        self.preview_canvas.update_settings(page_settings=self.app_settings.page)
        self.update_adaptive_font_info()
    
    def update_text_settings(self):
        """Обновление настроек текста"""
        self.preview_canvas.update_settings(text_settings=self.app_settings.text)
        self.update_adaptive_font_info()
    
    def update_smart_settings(self):
        """Обновление настроек умного форматирования"""
        self.preview_canvas.update_settings(
            text_settings=self.app_settings.text,
            page_number_settings=self.app_settings.page_numbers
        )
        self.update_adaptive_font_info()
    
    def update_adaptive_font_info(self):
        """Обновление информации об адаптивном шрифте"""
        smart_formatter = SmartFormatter(self.app_settings.page, self.app_settings.text)
        adaptive_size = smart_formatter.calculate_adaptive_font_size()
        
        info_text = f"Адаптивный размер шрифта: {adaptive_size:.1f} pt\n"
        info_text += f"Размер сетки: {self.app_settings.page.grid_size_mm} мм\n"
        info_text += f"Коэффициент заполнения: {self.app_settings.text.font_fill_ratio}"
        
        self.smart_tab.update_info(info_text)
    
    def update_navigation(self):
        """Обновление навигации по страницам"""
        current_page = self.preview_canvas.get_current_page()
        total_pages = self.preview_canvas.get_page_count()
        self.navigation_widget.update_navigation(current_page, total_pages)
    
    def generate_grid(self):
        """Генерация сетки"""
        self.preview_canvas.generate_grid()
    
    def import_background(self):
        """Импорт фонового изображения"""
        file_path = get_open_file_name(
            self, "Выбор фонового изображения",
            "Изображения (*.png *.jpg *.jpeg *.bmp)"
        )
        
        if file_path:
            pixmap = QPixmap(file_path)
            if not pixmap.isNull():
                self.preview_canvas.set_background(pixmap)
            else:
                show_error_message(self, "Ошибка", "Не удалось загрузить изображение")
    
    def clear_background(self):
        """Очистка фона"""
        self.preview_canvas.background_image = None
        self.preview_canvas.update_display()
    
    def prev_page(self):
        """Предыдущая страница"""
        if self.preview_canvas.prev_page():
            self.update_navigation()
    
    def next_page(self):
        """Следующая страница"""
        if self.preview_canvas.next_page():
            self.update_navigation()
    
    def generate_gcode_preview(self):
        """Генерация предпросмотра G-code"""
        if not self.preview_canvas.formatted_pages:
            self.export_tab.set_gcode_preview("")
            return
        
        # Показать только первые строки первой страницы
        first_page = self.preview_canvas.formatted_pages[0]
        preview_lines = first_page[:5]
        
        smart_formatter = SmartFormatter(self.app_settings.page, self.app_settings.text)
        adaptive_size = smart_formatter.calculate_adaptive_font_size()
        
        preview_text = f"""
; ===== Умный G-code Preview =====
; Страниц: {len(self.preview_canvas.formatted_pages)}
; Адаптивный шрифт: {adaptive_size:.1f}pt
; Выравнивание: {self.app_settings.text.alignment}
; Сетка: {self.app_settings.page.grid_type} {self.app_settings.page.grid_size_mm}мм

G90 ; Абсолютное позиционирование
G21 ; Миллиметры
M5 ; Поднять перо

; === Страница 1 ===
"""
        
        for i, line in enumerate(preview_lines):
            if line.strip():
                preview_text += f"; Строка {i+1}: {line[:30]}{'...' if len(line) > 30 else ''}\n"
                preview_text += f"G0 X5.00 Y{5.0 + i*4.0:.2f}\n"
                preview_text += "M3 ; Опустить перо\n"
                preview_text += f"G1 X{5.0 + len(line[:10])*2:.2f} Y{5.0 + i*4.0:.2f} F1000\n"
                preview_text += "M5 ; Поднять перо\n\n"
        
        preview_text += "...\n; (Полный G-code при экспорте)"
        
        self.export_tab.set_gcode_preview(preview_text)
    
    def export_gcode(self):
        """Экспорт умного G-code"""
        if not self.preview_canvas.formatted_pages:
            show_warning_message(self, "Предупреждение", "Нет текста для экспорта")
            return
        
        file_path = get_save_file_name(
            self, "Сохранить умный G-code", "smart_notes.gcode",
            "G-code файлы (*.gcode *.nc)"
        )
        
        if file_path:
            self.export_tab.show_progress(True)
            self.export_tab.set_progress(0)
            
            self.gcode_generator = SmartGCodeGenerator(
                self.preview_canvas.formatted_pages,
                self.app_settings.page,
                self.app_settings.text,
                self.app_settings.page_numbers
            )
            
            self.gcode_generator.finished.connect(
                lambda gcode: self.save_gcode(file_path, gcode)
            )
            self.gcode_generator.error.connect(
                lambda err: show_error_message(self, "Ошибка", f"Ошибка генерации: {err}")
            )
            self.gcode_generator.progress.connect(self.export_tab.set_progress)
            self.gcode_generator.status_update.connect(self.export_tab.set_status)
            
            self.gcode_generator.start()
    
    def save_gcode(self, file_path: str, gcode: str):
        """Сохранение G-code"""
        try:
            # Валидация G-code
            is_valid, messages = GCodeValidator.validate_gcode(gcode)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(gcode)
            
            self.export_tab.show_progress(False)
            
            # Показать результат
            result_message = f"Умный G-code сохранен:\n{file_path}\n\n"
            result_message += f"Страниц: {len(self.preview_canvas.formatted_pages)}\n"
            
            if not is_valid:
                result_message += f"\nПредупреждения валидации:\n" + "\n".join(messages[:3])
                show_warning_message(self, "G-code сохранен с предупреждениями", result_message)
            else:
                show_info_message(self, "Успех", result_message)
                
        except Exception as e:
            self.export_tab.show_progress(False)
            show_error_message(self, "Ошибка", f"Ошибка сохранения: {str(e)}")
    
    def export_image(self):
        """Экспорт текущей страницы как изображение"""
        file_path = get_save_file_name(
            self, "Сохранить изображение", "page.png",
            "PNG (*.png);;JPEG (*.jpg)"
        )
        
        if file_path:
            pixmap = self.preview_canvas.export_current_page_as_pixmap()
            if not pixmap.isNull() and pixmap.save(file_path):
                show_info_message(self, "Успех", f"Изображение сохранено:\n{file_path}")
            else:
                show_error_message(self, "Ошибка", "Не удалось сохранить изображение")
    
    def export_all_pages(self):
        """Экспорт всех страниц как изображений"""
        dir_path = get_directory(self, "Выберите папку для сохранения страниц")
        
        if dir_path:
            pixmaps = self.preview_canvas.export_all_pages_as_pixmaps()
            saved_count = 0
            
            for page_index, pixmap in enumerate(pixmaps):
                file_name = f"page_{page_index + 1:03d}.png"
                file_path = os.path.join(dir_path, file_name)
                
                if pixmap.save(file_path):
                    saved_count += 1
            
            show_info_message(
                self, "Успех",
                f"Сохранено {saved_count} из {len(pixmaps)} страниц в:\n{dir_path}"
            )
    
    def open_text_file(self):
        """Открытие текстового файла"""
        file_path = get_open_file_name(
            self, "Открыть текстовый файл",
            "Текстовые файлы (*.txt *.md);;Все файлы (*)"
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.editor_panel.set_text(content)
            except Exception as e:
                show_error_message(self, "Ошибка", f"Не удалось открыть файл: {str(e)}")
    
    def save_text_file(self):
        """Сохранение текстового файла"""
        file_path = get_save_file_name(
            self, "Сохранить текстовый файл", "notes.txt",
            "Текстовые файлы (*.txt);;Markdown (*.md)"
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(self.editor_panel.get_text())
                show_info_message(self, "Успех", f"Файл сохранен:\n{file_path}")
            except Exception as e:
                show_error_message(self, "Ошибка", f"Не удалось сохранить файл: {str(e)}")
    
    def show_about(self):
        """Показать информацию о программе"""
        about_text = """
        <h2>Notes → G-code Studio Pro</h2>
        <p><b>Версия:</b> 3.0 Professional</p>
        <p><b>Разработчик:</b> Smart G-code Studio</p>
        <br>
        <p>Профессиональный инструмент для преобразования текстовых конспектов
        в G-code для drawing machine с поддержкой:</p>
        <ul>
        <li>Умного форматирования и адаптивных шрифтов</li>
        <li>Автоматического выравнивания по сетке</li>
        <li>Многостраничной печати</li>
        <li>Нумерации страниц</li>
        <li>Современного интерфейса</li>
        </ul>
        """
        
        show_info_message(self, "О программе", about_text)
    
    def closeEvent(self, event):
        """Обработка закрытия приложения"""
        # Остановка генератора G-code если работает
        if self.gcode_generator and self.gcode_generator.isRunning():
            self.gcode_generator.terminate()
            self.gcode_generator.wait()
        
        # Сохранение настроек
        self.settings_manager.save_app_settings(self.app_settings)
        
        event.accept()
