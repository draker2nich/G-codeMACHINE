"""
Модуль виджета предпросмотра.
Содержит класс для отображения отформатированного текста с возможностью
навигации по страницам и предпросмотра результата.
"""

from typing import List
from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QPixmap, QPainter, QPen, QColor, QFont, QFontMetrics

from config import PageSettings, TextSettings, PageNumberSettings
from text_formatter import SmartFormatter, TextPageManager


class AdvancedTextPreviewCanvas(QLabel):
    """Продвинутый виджет предпросмотра с умным форматированием"""
    
    def __init__(self):
        super().__init__()
        self.setMinimumSize(600, 800)
        self.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        
        # Настройки
        self.page_settings = PageSettings()
        self.text_settings = TextSettings()
        self.page_number_settings = PageNumberSettings()
        
        # Данные
        self.text_content = ""
        self.background_image = None
        self.formatted_pages = []
        self.current_page = 0
        
        # Компоненты
        self.smart_formatter = SmartFormatter(self.page_settings, self.text_settings)
        self.page_manager = TextPageManager(self.smart_formatter)
        
        self.setStyleSheet("""
            QLabel {
                background-color: white;
                border: 2px solid #404040;
                border-radius: 8px;
                padding: 10px;
            }
        """)
        
    def update_settings(self, page_settings: PageSettings = None, 
                       text_settings: TextSettings = None,
                       page_number_settings: PageNumberSettings = None):
        """Обновление настроек"""
        if page_settings:
            self.page_settings = page_settings
        if text_settings:
            self.text_settings = text_settings
        if page_number_settings:
            self.page_number_settings = page_number_settings
            
        self.smart_formatter = SmartFormatter(self.page_settings, self.text_settings)
        self.page_manager = TextPageManager(self.smart_formatter)
        self.update_display()
    
    def set_text(self, text: str):
        """Установка текста с умным форматированием"""
        self.text_content = text
        self.format_text_to_pages()
        self.update_display()
    
    def format_text_to_pages(self):
        """Форматирование текста на страницы"""
        if not self.text_content.strip():
            self.formatted_pages = []
            return
            
        # Резерв места для номера страницы
        page_number_reserve = 0
        if self.page_number_settings.enabled:
            page_number_reserve = self.page_number_settings.offset_mm * 2 + 5
        
        self.formatted_pages = self.page_manager.format_text_to_pages(
            self.text_content, page_number_reserve
        )
    
    def set_background(self, pixmap: QPixmap):
        """Установка фонового изображения"""
        self.background_image = pixmap
        self.update_display()
    
    def update_display(self):
        """Обновление отображения"""
        if not self.formatted_pages:
            self.format_text_to_pages()
            
        canvas_width = self.smart_formatter.mm_to_pixels(self.page_settings.width_mm)
        canvas_height = self.smart_formatter.mm_to_pixels(self.page_settings.height_mm)
        
        pixmap = QPixmap(canvas_width, canvas_height)
        pixmap.fill(QColor("white"))
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Фоновое изображение
        if self.background_image:
            scaled_bg = self.background_image.scaled(
                QSize(canvas_width, canvas_height), 
                Qt.KeepAspectRatio, 
                Qt.SmoothTransformation
            )
            painter.drawPixmap(0, 0, scaled_bg)
        
        # Рендер текущей страницы
        if self.formatted_pages and 0 <= self.current_page < len(self.formatted_pages):
            self.render_page(painter, self.current_page)
        
        painter.end()
        self.setPixmap(pixmap)
    
    def render_page(self, painter: QPainter, page_index: int):
        """Рендеринг страницы"""
        if page_index >= len(self.formatted_pages):
            return
            
        lines = self.formatted_pages[page_index]
        
        # Настройка шрифта
        adaptive_font_size = self.smart_formatter.calculate_adaptive_font_size()
        font = QFont(self.text_settings.font_family, int(adaptive_font_size))
        painter.setFont(font)
        painter.setPen(QPen(QColor("black")))
        
        # Границы текстовой области
        left, top, right, bottom = self.smart_formatter.get_text_area_bounds()
        
        # Рендеринг строк
        font_metrics = QFontMetrics(font)
        line_height = font_metrics.height() * self.text_settings.line_spacing
        
        y = top
        
        for line in lines:
            if line == "":  # Пустая строка
                y += self.smart_formatter.mm_to_pixels(self.text_settings.paragraph_spacing_mm)
                continue
            
            # Выравнивание текста
            x = self.smart_formatter.calculate_line_x_position(line, font_metrics, left, right)
            
            # Выравнивание по сетке
            aligned_x, aligned_y = self.smart_formatter.align_to_grid(x, y)
            
            # Рендеринг строки
            painter.drawText(int(aligned_x), int(aligned_y + font_metrics.ascent()), line)
            
            y += line_height
        
        # Номер страницы
        if self.page_number_settings.enabled:
            self.render_page_number(painter, page_index)
    
    def render_page_number(self, painter: QPainter, page_index: int):
        """Рендеринг номера страницы"""
        page_number_text = self.page_number_settings.format.format(
            page=page_index + 1,
            total=len(self.formatted_pages)
        )
        
        # Шрифт для номера страницы
        page_font = QFont(
            self.text_settings.font_family, 
            int(self.page_number_settings.font_size_pt)
        )
        painter.setFont(page_font)
        
        font_metrics = QFontMetrics(page_font)
        text_width = font_metrics.horizontalAdvance(page_number_text)
        text_height = font_metrics.height()
        
        # Позиция номера страницы
        canvas_width = self.smart_formatter.mm_to_pixels(self.page_settings.width_mm)
        canvas_height = self.smart_formatter.mm_to_pixels(self.page_settings.height_mm)
        offset_px = self.smart_formatter.mm_to_pixels(self.page_number_settings.offset_mm)
        
        position = self.page_number_settings.position
        
        if "bottom" in position:
            y = canvas_height - offset_px
        elif "top" in position:
            y = offset_px + text_height
        else:
            y = canvas_height // 2
        
        if "center" in position:
            x = (canvas_width - text_width) // 2
        elif "right" in position:
            x = canvas_width - text_width - offset_px
        else:  # left
            x = offset_px
        
        painter.drawText(x, y, page_number_text)
    
    def generate_grid(self):
        """Генерация сетки"""
        canvas_width = self.smart_formatter.mm_to_pixels(self.page_settings.width_mm)
        canvas_height = self.smart_formatter.mm_to_pixels(self.page_settings.height_mm)
        cell_size_px = self.smart_formatter.mm_to_pixels(self.page_settings.grid_size_mm)
        
        pixmap = QPixmap(canvas_width, canvas_height)
        pixmap.fill(QColor("white"))
        
        painter = QPainter(pixmap)
        pen = QPen(QColor("#E0E0E0"), 1)
        painter.setPen(pen)
        
        if self.page_settings.grid_type == "клетка":
            # Вертикальные линии
            for x in range(0, canvas_width, cell_size_px):
                painter.drawLine(x, 0, x, canvas_height)
            # Горизонтальные линии
            for y in range(0, canvas_height, cell_size_px):
                painter.drawLine(0, y, canvas_width, y)
        elif self.page_settings.grid_type == "линейка":
            # Только горизонтальные линии
            for y in range(cell_size_px, canvas_height, cell_size_px):
                painter.drawLine(0, y, canvas_width, y)
        
        painter.end()
        self.set_background(pixmap)
    
    def next_page(self):
        """Следующая страница"""
        if self.current_page < len(self.formatted_pages) - 1:
            self.current_page += 1
            self.update_display()
            return True
        return False
    
    def prev_page(self):
        """Предыдущая страница"""
        if self.current_page > 0:
            self.current_page -= 1
            self.update_display()
            return True
        return False
    
    def set_page(self, page_index: int):
        """Переход на конкретную страницу"""
        if 0 <= page_index < len(self.formatted_pages):
            self.current_page = page_index
            self.update_display()
            return True
        return False
    
    def get_page_count(self) -> int:
        """Получение количества страниц"""
        return len(self.formatted_pages)
    
    def get_current_page(self) -> int:
        """Получение номера текущей страницы (начиная с 0)"""
        return self.current_page
    
    def get_text_statistics(self) -> dict:
        """Получение статистики текста"""
        return self.page_manager.get_text_statistics(self.text_content)
    
    def export_current_page_as_pixmap(self) -> QPixmap:
        """Экспорт текущей страницы как QPixmap"""
        return self.pixmap().copy() if self.pixmap() else QPixmap()
    
    def export_all_pages_as_pixmaps(self) -> List[QPixmap]:
        """Экспорт всех страниц как список QPixmap"""
        original_page = self.current_page
        pixmaps = []
        
        for page_index in range(len(self.formatted_pages)):
            self.set_page(page_index)
            pixmap = self.export_current_page_as_pixmap()
            if not pixmap.isNull():
                pixmaps.append(pixmap)
        
        # Вернуться к исходной странице
        self.set_page(original_page)
        
        return pixmaps
    
    def validate_current_text(self) -> tuple[bool, str]:
        """Валидация текущего текста"""
        return self.page_manager.validate_text_fits(self.text_content)
    
    def clear(self):
        """Очистка виджета"""
        self.text_content = ""
        self.formatted_pages = []
        self.current_page = 0
        self.background_image = None
        
        # Создание пустого изображения
        canvas_width = self.smart_formatter.mm_to_pixels(self.page_settings.width_mm)
        canvas_height = self.smart_formatter.mm_to_pixels(self.page_settings.height_mm)
        
        pixmap = QPixmap(canvas_width, canvas_height)
        pixmap.fill(QColor("white"))
        self.setPixmap(pixmap)
