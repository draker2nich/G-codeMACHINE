"""
Модуль компонентов интерфейса.
Содержит отдельные виджеты и панели для основного окна приложения.
"""

from typing import Callable, Optional
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QLabel, QSpinBox, 
    QDoubleSpinBox, QPushButton, QFileDialog, QGroupBox, QComboBox,
    QTabWidget, QFormLayout, QFontComboBox, QLineEdit, QProgressBar,
    QTextBrowser, QGridLayout, QCheckBox, QRadioButton, QButtonGroup,
    QMessageBox
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont

from config import PageSettings, TextSettings, PageNumberSettings


class EditorPanel(QGroupBox):
    """Панель редактора текста"""
    
    text_changed = Signal(str)
    
    def __init__(self):
        super().__init__("📝 Умный редактор")
        self.setup_ui()
        
    def setup_ui(self):
        """Настройка интерфейса"""
        layout = QVBoxLayout(self)
        
        # Редактор текста
        self.text_editor = QTextEdit()
        self.text_editor.setPlaceholderText(
            "Введите текст конспекта...\n\n"
            "✨ Умные функции:\n"
            "• Автоматическое выравнивание по сетке\n"
            "• Адаптивный размер шрифта\n"
            "• Умный перенос строк\n"
            "• Красная строка и отступы\n"
            "• Автоматическая нумерация страниц\n\n"
            "📝 Форматирование:\n"
            "• **жирный** *курсив*\n"
            "• LaTeX: $x^2 + y^2 = z^2$\n"
            "• Греческие: $\\alpha, \\beta, \\pi$\n"
        )
        self.text_editor.textChanged.connect(self._on_text_changed)
        self.text_editor.setMinimumHeight(500)
        layout.addWidget(self.text_editor)
        
        # Информация о тексте
        self.info_group = self.create_text_info_widget()
        layout.addWidget(self.info_group)
    
    def create_text_info_widget(self) -> QGroupBox:
        """Создание виджета статистики текста"""
        info_group = QGroupBox("📊 Статистика")
        info_layout = QGridLayout(info_group)
        
        self.chars_label = QLabel("Символов: 0")
        self.words_label = QLabel("Слов: 0")
        self.lines_label = QLabel("Строк: 0")
        self.pages_label = QLabel("Страниц: 0")
        
        info_layout.addWidget(self.chars_label, 0, 0)
        info_layout.addWidget(self.words_label, 0, 1)
        info_layout.addWidget(self.lines_label, 1, 0)
        info_layout.addWidget(self.pages_label, 1, 1)
        
        return info_group
    
    def _on_text_changed(self):
        """Обработка изменения текста"""
        text = self.text_editor.toPlainText()
        self.update_statistics(text)
        self.text_changed.emit(text)
    
    def update_statistics(self, text: str):
        """Обновление статистики"""
        char_count = len(text)
        word_count = len([w for w in text.split() if w.strip()])
        line_count = len(text.split('\n'))
        
        self.chars_label.setText(f"Символов: {char_count}")
        self.words_label.setText(f"Слов: {word_count}")
        self.lines_label.setText(f"Строк: {line_count}")
    
    def update_page_count(self, page_count: int):
        """Обновление количества страниц"""
        self.pages_label.setText(f"Страниц: {page_count}")
    
    def get_text(self) -> str:
        """Получение текста"""
        return self.text_editor.toPlainText()
    
    def set_text(self, text: str):
        """Установка текста"""
        self.text_editor.setPlainText(text)


class PageSettingsTab(QWidget):
    """Вкладка настроек страницы"""
    
    settings_changed = Signal()
    
    def __init__(self, settings: PageSettings):
        super().__init__()
        self.settings = settings
        self.setup_ui()
        
    def setup_ui(self):
        """Настройка интерфейса"""
        layout = QVBoxLayout(self)
        
        # Размеры
        size_group = QGroupBox("📏 Размеры листа")
        size_layout = QFormLayout(size_group)
        
        self.width_spinbox = QDoubleSpinBox()
        self.width_spinbox.setRange(10.0, 500.0)
        self.width_spinbox.setValue(self.settings.width_mm)
        self.width_spinbox.setSuffix(" мм")
        self.width_spinbox.valueChanged.connect(self.on_settings_changed)
        
        self.height_spinbox = QDoubleSpinBox()
        self.height_spinbox.setRange(10.0, 500.0)
        self.height_spinbox.setValue(self.settings.height_mm)
        self.height_spinbox.setSuffix(" мм")
        self.height_spinbox.valueChanged.connect(self.on_settings_changed)
        
        size_layout.addRow("Ширина:", self.width_spinbox)
        size_layout.addRow("Высота:", self.height_spinbox)
        
        # Поля
        margins_group = QGroupBox("📐 Поля страницы")
        margins_layout = QFormLayout(margins_group)
        
        self.margin_left_spinbox = QDoubleSpinBox()
        self.margin_left_spinbox.setRange(0.0, 50.0)
        self.margin_left_spinbox.setValue(self.settings.margin_left_mm)
        self.margin_left_spinbox.setSuffix(" мм")
        self.margin_left_spinbox.valueChanged.connect(self.on_settings_changed)
        
        self.margin_right_spinbox = QDoubleSpinBox()
        self.margin_right_spinbox.setRange(0.0, 50.0)
        self.margin_right_spinbox.setValue(self.settings.margin_right_mm)
        self.margin_right_spinbox.setSuffix(" мм")
        self.margin_right_spinbox.valueChanged.connect(self.on_settings_changed)
        
        self.margin_top_spinbox = QDoubleSpinBox()
        self.margin_top_spinbox.setRange(0.0, 50.0)
        self.margin_top_spinbox.setValue(self.settings.margin_top_mm)
        self.margin_top_spinbox.setSuffix(" мм")
        self.margin_top_spinbox.valueChanged.connect(self.on_settings_changed)
        
        self.margin_bottom_spinbox = QDoubleSpinBox()
        self.margin_bottom_spinbox.setRange(0.0, 50.0)
        self.margin_bottom_spinbox.setValue(self.settings.margin_bottom_mm)
        self.margin_bottom_spinbox.setSuffix(" мм")
        self.margin_bottom_spinbox.valueChanged.connect(self.on_settings_changed)
        
        margins_layout.addRow("Слева:", self.margin_left_spinbox)
        margins_layout.addRow("Справа:", self.margin_right_spinbox)
        margins_layout.addRow("Сверху:", self.margin_top_spinbox)
        margins_layout.addRow("Снизу:", self.margin_bottom_spinbox)
        
        # Сетка
        grid_group = QGroupBox("⊞ Настройки сетки")
        grid_layout = QFormLayout(grid_group)
        
        self.grid_type_combo = QComboBox()
        self.grid_type_combo.addItems(["клетка", "линейка"])
        self.grid_type_combo.setCurrentText(self.settings.grid_type)
        self.grid_type_combo.currentTextChanged.connect(self.on_settings_changed)
        
        self.grid_size_spinbox = QDoubleSpinBox()
        self.grid_size_spinbox.setRange(0.5, 20.0)
        self.grid_size_spinbox.setValue(self.settings.grid_size_mm)
        self.grid_size_spinbox.setSuffix(" мм")
        self.grid_size_spinbox.valueChanged.connect(self.on_settings_changed)
        
        self.dpi_spinbox = QSpinBox()
        self.dpi_spinbox.setRange(72, 600)
        self.dpi_spinbox.setValue(self.settings.dpi)
        self.dpi_spinbox.setSuffix(" dpi")
        self.dpi_spinbox.valueChanged.connect(self.on_settings_changed)
        
        grid_layout.addRow("Тип сетки:", self.grid_type_combo)
        grid_layout.addRow("Размер клетки:", self.grid_size_spinbox)
        grid_layout.addRow("Разрешение:", self.dpi_spinbox)
        
        layout.addWidget(size_group)
        layout.addWidget(margins_group)
        layout.addWidget(grid_group)
        layout.addStretch()
    
    def on_settings_changed(self):
        """Обработка изменения настроек"""
        self.update_settings()
        self.settings_changed.emit()
    
    def update_settings(self):
        """Обновление настроек из виджетов"""
        self.settings.width_mm = self.width_spinbox.value()
        self.settings.height_mm = self.height_spinbox.value()
        self.settings.margin_left_mm = self.margin_left_spinbox.value()
        self.settings.margin_right_mm = self.margin_right_spinbox.value()
        self.settings.margin_top_mm = self.margin_top_spinbox.value()
        self.settings.margin_bottom_mm = self.margin_bottom_spinbox.value()
        self.settings.grid_type = self.grid_type_combo.currentText()
        self.settings.grid_size_mm = self.grid_size_spinbox.value()
        self.settings.dpi = self.dpi_spinbox.value()


class TextSettingsTab(QWidget):
    """Вкладка настроек текста"""
    
    settings_changed = Signal()
    
    def __init__(self, settings: TextSettings):
        super().__init__()
        self.settings = settings
        self.setup_ui()
        
    def setup_ui(self):
        """Настройка интерфейса"""
        layout = QVBoxLayout(self)
        
        # Шрифт
        font_group = QGroupBox("🔤 Настройки шрифта")
        font_layout = QFormLayout(font_group)
        
        self.font_combo = QFontComboBox()
        self.font_combo.setCurrentFont(QFont(self.settings.font_family))
        self.font_combo.currentFontChanged.connect(self.on_settings_changed)
        
        self.font_size_spinbox = QDoubleSpinBox()
        self.font_size_spinbox.setRange(6.0, 72.0)
        self.font_size_spinbox.setValue(self.settings.font_size_pt)
        self.font_size_spinbox.setSuffix(" pt")
        self.font_size_spinbox.valueChanged.connect(self.on_settings_changed)
        
        font_layout.addRow("Шрифт:", self.font_combo)
        font_layout.addRow("Размер:", self.font_size_spinbox)
        
        # Интервалы
        spacing_group = QGroupBox("📐 Интервалы")
        spacing_layout = QFormLayout(spacing_group)
        
        self.line_spacing_spinbox = QDoubleSpinBox()
        self.line_spacing_spinbox.setRange(0.5, 5.0)
        self.line_spacing_spinbox.setValue(self.settings.line_spacing)
        self.line_spacing_spinbox.setSingleStep(0.1)
        self.line_spacing_spinbox.valueChanged.connect(self.on_settings_changed)
        
        self.letter_spacing_spinbox = QDoubleSpinBox()
        self.letter_spacing_spinbox.setRange(0.0, 10.0)
        self.letter_spacing_spinbox.setValue(self.settings.letter_spacing_mm)
        self.letter_spacing_spinbox.setSuffix(" мм")
        self.letter_spacing_spinbox.valueChanged.connect(self.on_settings_changed)
        
        self.paragraph_spacing_spinbox = QDoubleSpinBox()
        self.paragraph_spacing_spinbox.setRange(0.0, 20.0)
        self.paragraph_spacing_spinbox.setValue(self.settings.paragraph_spacing_mm)
        self.paragraph_spacing_spinbox.setSuffix(" мм")
        self.paragraph_spacing_spinbox.valueChanged.connect(self.on_settings_changed)
        
        spacing_layout.addRow("Межстрочный:", self.line_spacing_spinbox)
        spacing_layout.addRow("Между буквами:", self.letter_spacing_spinbox)
        spacing_layout.addRow("Между абзацами:", self.paragraph_spacing_spinbox)
        
        # Выравнивание
        alignment_group = QGroupBox("📍 Выравнивание")
        alignment_layout = QFormLayout(alignment_group)
        
        self.alignment_combo = QComboBox()
        self.alignment_combo.addItems(["left", "center", "right", "justify"])
        self.alignment_combo.setCurrentText(self.settings.alignment)
        self.alignment_combo.currentTextChanged.connect(self.on_settings_changed)
        
        self.indent_spinbox = QDoubleSpinBox()
        self.indent_spinbox.setRange(0.0, 20.0)
        self.indent_spinbox.setValue(self.settings.indent_first_line_mm)
        self.indent_spinbox.setSuffix(" мм")
        self.indent_spinbox.valueChanged.connect(self.on_settings_changed)
        
        alignment_layout.addRow("Выравнивание:", self.alignment_combo)
        alignment_layout.addRow("Красная строка:", self.indent_spinbox)
        
        layout.addWidget(font_group)
        layout.addWidget(spacing_group)
        layout.addWidget(alignment_group)
        layout.addStretch()
    
    def on_settings_changed(self):
        """Обработка изменения настроек"""
        self.update_settings()
        self.settings_changed.emit()
    
    def update_settings(self):
        """Обновление настроек из виджетов"""
        self.settings.font_family = self.font_combo.currentFont().family()
        self.settings.font_size_pt = self.font_size_spinbox.value()
        self.settings.line_spacing = self.line_spacing_spinbox.value()
        self.settings.letter_spacing_mm = self.letter_spacing_spinbox.value()
        self.settings.paragraph_spacing_mm = self.paragraph_spacing_spinbox.value()
        self.settings.alignment = self.alignment_combo.currentText()
        self.settings.indent_first_line_mm = self.indent_spinbox.value()


class SmartFormattingTab(QWidget):
    """Вкладка умного форматирования"""
    
    settings_changed = Signal()
    info_updated = Signal(str)
    
    def __init__(self, text_settings: TextSettings, page_number_settings: PageNumberSettings):
        super().__init__()
        self.text_settings = text_settings
        self.page_number_settings = page_number_settings
        self.setup_ui()
        
    def setup_ui(self):
        """Настройка интерфейса"""
        layout = QVBoxLayout(self)
        
        # Адаптивный шрифт
        adaptive_group = QGroupBox("🧠 Адаптивный шрифт")
        adaptive_layout = QFormLayout(adaptive_group)
        
        self.auto_font_checkbox = QCheckBox("Автоматический размер под сетку")
        self.auto_font_checkbox.setChecked(self.text_settings.auto_font_size)
        self.auto_font_checkbox.toggled.connect(self.on_settings_changed)
        
        self.font_fill_ratio_spinbox = QDoubleSpinBox()
        self.font_fill_ratio_spinbox.setRange(0.1, 1.0)
        self.font_fill_ratio_spinbox.setValue(self.text_settings.font_fill_ratio)
        self.font_fill_ratio_spinbox.setSingleStep(0.1)
        self.font_fill_ratio_spinbox.valueChanged.connect(self.on_settings_changed)
        
        adaptive_layout.addRow(self.auto_font_checkbox)
        adaptive_layout.addRow("Коэффициент заполнения:", self.font_fill_ratio_spinbox)
        
        # Нумерация страниц
        page_num_group = QGroupBox("📄 Нумерация страниц")
        page_num_layout = QFormLayout(page_num_group)
        
        self.page_numbers_checkbox = QCheckBox("Включить нумерацию")
        self.page_numbers_checkbox.setChecked(self.page_number_settings.enabled)
        self.page_numbers_checkbox.toggled.connect(self.on_settings_changed)
        
        self.page_position_combo = QComboBox()
        positions = ["bottom_center", "bottom_left", "bottom_right", 
                    "top_center", "top_left", "top_right"]
        self.page_position_combo.addItems(positions)
        self.page_position_combo.setCurrentText(self.page_number_settings.position)
        self.page_position_combo.currentTextChanged.connect(self.on_settings_changed)
        
        self.page_format_line = QLineEdit()
        self.page_format_line.setText(self.page_number_settings.format)
        self.page_format_line.setPlaceholderText("Например: - {page} - или стр. {page} из {total}")
        self.page_format_line.textChanged.connect(self.on_settings_changed)
        
        self.page_font_size_spinbox = QDoubleSpinBox()
        self.page_font_size_spinbox.setRange(6.0, 24.0)
        self.page_font_size_spinbox.setValue(self.page_number_settings.font_size_pt)
        self.page_font_size_spinbox.setSuffix(" pt")
        self.page_font_size_spinbox.valueChanged.connect(self.on_settings_changed)
        
        page_num_layout.addRow(self.page_numbers_checkbox)
        page_num_layout.addRow("Позиция:", self.page_position_combo)
        page_num_layout.addRow("Формат:", self.page_format_line)
        page_num_layout.addRow("Размер шрифта:", self.page_font_size_spinbox)
        
        # Информация
        info_group = QGroupBox("ℹ️ Информация")
        info_layout = QVBoxLayout(info_group)
        
        self.adaptive_font_info = QLabel()
        info_layout.addWidget(self.adaptive_font_info)
        
        layout.addWidget(adaptive_group)
        layout.addWidget(page_num_group)
        layout.addWidget(info_group)
        layout.addStretch()
    
    def on_settings_changed(self):
        """Обработка изменения настроек"""
        self.update_settings()
        self.settings_changed.emit()
    
    def update_settings(self):
        """Обновление настроек из виджетов"""
        self.text_settings.auto_font_size = self.auto_font_checkbox.isChecked()
        self.text_settings.font_fill_ratio = self.font_fill_ratio_spinbox.value()
        
        self.page_number_settings.enabled = self.page_numbers_checkbox.isChecked()
        self.page_number_settings.position = self.page_position_combo.currentText()
        self.page_number_settings.format = self.page_format_line.text()
        self.page_number_settings.font_size_pt = self.page_font_size_spinbox.value()
    
    def update_info(self, info_text: str):
        """Обновление информационного текста"""
        self.adaptive_font_info.setText(info_text)


class ExportTab(QWidget):
    """Вкладка экспорта"""
    
    export_gcode_requested = Signal()
    export_image_requested = Signal()
    export_all_pages_requested = Signal()
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
    def setup_ui(self):
        """Настройка интерфейса"""
        layout = QVBoxLayout(self)
        
        # Прогресс
        progress_group = QGroupBox("⚙️ Процесс экспорта")
        progress_layout = QVBoxLayout(progress_group)
        
        self.export_progress = QProgressBar()
        self.export_progress.setVisible(False)
        progress_layout.addWidget(self.export_progress)
        
        self.export_status_label = QLabel("Готов к экспорту")
        progress_layout.addWidget(self.export_status_label)
        
        # Кнопки экспорта
        buttons_layout = QVBoxLayout()
        
        export_gcode_btn = QPushButton("📤 Экспорт умного G-code")
        export_gcode_btn.clicked.connect(self.export_gcode_requested.emit)
        export_gcode_btn.setMinimumHeight(40)
        
        export_image_btn = QPushButton("🖼️ Экспорт изображения")
        export_image_btn.clicked.connect(self.export_image_requested.emit)
        
        export_all_pages_btn = QPushButton("📚 Экспорт всех страниц")
        export_all_pages_btn.clicked.connect(self.export_all_pages_requested.emit)
        
        buttons_layout.addWidget(export_gcode_btn)
        buttons_layout.addWidget(export_image_btn)
        buttons_layout.addWidget(export_all_pages_btn)
        
        # Предпросмотр G-code
        preview_group = QGroupBox("👀 Предпросмотр G-code")
        preview_layout = QVBoxLayout(preview_group)
        
        self.gcode_preview = QTextBrowser()
        self.gcode_preview.setMaximumHeight(200)
        self.gcode_preview.setPlaceholderText("Умный G-code будет отображен здесь...")
        preview_layout.addWidget(self.gcode_preview)
        
        layout.addWidget(progress_group)
        layout.addLayout(buttons_layout)
        layout.addWidget(preview_group)
        layout.addStretch()
    
    def show_progress(self, show: bool):
        """Показать/скрыть прогресс"""
        self.export_progress.setVisible(show)
    
    def set_progress(self, value: int):
        """Установить значение прогресса"""
        self.export_progress.setValue(value)
    
    def set_status(self, status: str):
        """Установить статус экспорта"""
        self.export_status_label.setText(status)
    
    def set_gcode_preview(self, gcode: str):
        """Установить предпросмотр G-code"""
        self.gcode_preview.setPlainText(gcode)


class NavigationWidget(QWidget):
    """Виджет навигации по страницам"""
    
    prev_page = Signal()
    next_page = Signal()
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
    def setup_ui(self):
        """Настройка интерфейса"""
        layout = QHBoxLayout(self)
        
        self.prev_page_btn = QPushButton("◀ Предыдущая")
        self.prev_page_btn.clicked.connect(self.prev_page.emit)
        
        self.page_info_label = QLabel("Страница 1 из 1")
        self.page_info_label.setAlignment(Qt.AlignCenter)
        
        self.next_page_btn = QPushButton("Следующая ▶")
        self.next_page_btn.clicked.connect(self.next_page.emit)
        
        layout.addWidget(self.prev_page_btn)
        layout.addWidget(self.page_info_label)
        layout.addWidget(self.next_page_btn)
    
    def update_navigation(self, current_page: int, total_pages: int):
        """Обновление навигации"""
        self.page_info_label.setText(f"Страница {current_page + 1} из {total_pages}")
        self.prev_page_btn.setEnabled(current_page > 0)
        self.next_page_btn.setEnabled(current_page < total_pages - 1)


class BackgroundControlWidget(QWidget):
    """Виджет управления фоном"""
    
    generate_grid = Signal()
    import_background = Signal()
    clear_background = Signal()
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
    def setup_ui(self):
        """Настройка интерфейса"""
        layout = QHBoxLayout(self)
        
        generate_grid_btn = QPushButton("🎨 Генерировать сетку")
        generate_grid_btn.clicked.connect(self.generate_grid.emit)
        
        import_bg_btn = QPushButton("📁 Импорт фона")
        import_bg_btn.clicked.connect(self.import_background.emit)
        
        clear_bg_btn = QPushButton("🗑️ Очистить фон")
        clear_bg_btn.clicked.connect(self.clear_background.emit)
        
        layout.addWidget(generate_grid_btn)
        layout.addWidget(import_bg_btn)
        layout.addWidget(clear_bg_btn)


def show_error_message(parent: QWidget, title: str, message: str):
    """Показать сообщение об ошибке"""
    QMessageBox.critical(parent, title, message)


def show_info_message(parent: QWidget, title: str, message: str):
    """Показать информационное сообщение"""
    QMessageBox.information(parent, title, message)


def show_warning_message(parent: QWidget, title: str, message: str):
    """Показать предупреждение"""
    QMessageBox.warning(parent, title, message)


def get_save_file_name(parent: QWidget, title: str, default_name: str, filter: str) -> Optional[str]:
    """Диалог сохранения файла"""
    file_path, _ = QFileDialog.getSaveFileName(parent, title, default_name, filter)
    return file_path if file_path else None


def get_open_file_name(parent: QWidget, title: str, filter: str) -> Optional[str]:
    """Диалог открытия файла"""
    file_path, _ = QFileDialog.getOpenFileName(parent, title, "", filter)
    return file_path if file_path else None


def get_directory(parent: QWidget, title: str) -> Optional[str]:
    """Диалог выбора директории"""
    dir_path = QFileDialog.getExistingDirectory(parent, title)
    return dir_path if dir_path else None
