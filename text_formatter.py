"""
Модуль умного форматирования текста.
Содержит логику адаптивного размещения текста, выравнивания по сетке
и разбиения на страницы.
"""

from typing import List, Tuple
from PySide6.QtGui import QFont, QFontMetrics
from config import PageSettings, TextSettings


class SmartFormatter:
    """Класс для умного форматирования текста"""
    
    def __init__(self, page_settings: PageSettings, text_settings: TextSettings):
        self.page_settings = page_settings
        self.text_settings = text_settings
        
    def mm_to_pixels(self, mm: float) -> int:
        """Конвертация мм в пиксели"""
        inches = mm / 25.4
        return int(inches * self.page_settings.dpi)
    
    def pixels_to_mm(self, pixels: int) -> float:
        """Конвертация пикселей в мм"""
        inches = pixels / self.page_settings.dpi
        return inches * 25.4
    
    def calculate_adaptive_font_size(self) -> float:
        """Расчет адаптивного размера шрифта под сетку"""
        if not self.text_settings.auto_font_size:
            return self.text_settings.font_size_pt
            
        grid_size_px = self.mm_to_pixels(self.page_settings.grid_size_mm)
        target_height_px = grid_size_px * self.text_settings.font_fill_ratio
        
        # Конвертация пикселей в пункты (1 пункт = 1/72 дюйма)
        target_height_inches = target_height_px / self.page_settings.dpi
        font_size_pt = target_height_inches * 72
        
        return max(6.0, min(72.0, font_size_pt))
    
    def get_text_area_bounds(self) -> Tuple[int, int, int, int]:
        """Получение границ текстовой области в пикселях"""
        left = self.mm_to_pixels(self.page_settings.margin_left_mm)
        top = self.mm_to_pixels(self.page_settings.margin_top_mm)
        right = self.mm_to_pixels(self.page_settings.width_mm - self.page_settings.margin_right_mm)
        bottom = self.mm_to_pixels(self.page_settings.height_mm - self.page_settings.margin_bottom_mm)
        return left, top, right, bottom
    
    def get_text_area_bounds_mm(self) -> Tuple[float, float, float, float]:
        """Получение границ текстовой области в мм"""
        left = self.page_settings.margin_left_mm
        top = self.page_settings.margin_top_mm
        right = self.page_settings.width_mm - self.page_settings.margin_right_mm
        bottom = self.page_settings.height_mm - self.page_settings.margin_bottom_mm
        return left, top, right, bottom
    
    def align_to_grid(self, x: float, y: float) -> Tuple[float, float]:
        """Выравнивание координат по сетке"""
        grid_size_px = self.mm_to_pixels(self.page_settings.grid_size_mm)
        
        aligned_x = round(x / grid_size_px) * grid_size_px
        aligned_y = round(y / grid_size_px) * grid_size_px
        
        return aligned_x, aligned_y
    
    def align_to_grid_mm(self, coord_mm: float) -> float:
        """Выравнивание координаты по сетке в мм"""
        return round(coord_mm / self.page_settings.grid_size_mm) * self.page_settings.grid_size_mm
    
    def wrap_text_lines(self, text: str, font: QFont, max_width_px: int) -> List[str]:
        """Умный перенос строк по словам"""
        font_metrics = QFontMetrics(font)
        paragraphs = text.split('\n')
        wrapped_lines = []
        
        for paragraph in paragraphs:
            if not paragraph.strip():
                wrapped_lines.append("")
                continue
                
            words = paragraph.split()
            current_line = ""
            
            for word in words:
                test_line = current_line + (" " if current_line else "") + word
                test_width = font_metrics.horizontalAdvance(test_line)
                
                if test_width <= max_width_px or not current_line:
                    current_line = test_line
                else:
                    wrapped_lines.append(current_line)
                    current_line = word
            
            if current_line:
                wrapped_lines.append(current_line)
        
        return wrapped_lines
    
    def format_paragraph(self, lines: List[str], is_first_paragraph: bool = False) -> List[str]:
        """Форматирование абзаца с отступами"""
        if not lines:
            return lines
            
        formatted_lines = []
        
        for i, line in enumerate(lines):
            if i == 0 and is_first_paragraph and self.text_settings.indent_first_line_mm > 0:
                # Красная строка для первой строки абзаца
                indent_spaces = int(self.text_settings.indent_first_line_mm / 2)
                indent = " " * indent_spaces
                formatted_lines.append(indent + line)
            else:
                formatted_lines.append(line)
        
        return formatted_lines
    
    def calculate_line_x_position(self, line: str, font_metrics: QFontMetrics, 
                                left: int, right: int) -> float:
        """Расчет позиции X для строки в зависимости от выравнивания"""
        line_width = font_metrics.horizontalAdvance(line)
        area_width = right - left
        
        if self.text_settings.alignment == "center":
            return left + (area_width - line_width) / 2
        elif self.text_settings.alignment == "right":
            return right - line_width
        elif self.text_settings.alignment == "justify":
            # Простая реализация выравнивания по ширине
            return left
        else:  # left
            return left
    
    def calculate_line_x_position_mm(self, line: str, left_mm: float) -> float:
        """Расчет позиции X для строки в мм"""
        if self.text_settings.alignment == "center":
            text_area_width_mm = (self.page_settings.width_mm - 
                                self.page_settings.margin_left_mm - 
                                self.page_settings.margin_right_mm)
            adaptive_font_size = self.calculate_adaptive_font_size()
            char_width_mm = adaptive_font_size * 0.6 * 0.352778  # pt to mm approximation
            line_width_mm = len(line) * char_width_mm
            return left_mm + (text_area_width_mm - line_width_mm) / 2
        elif self.text_settings.alignment == "right":
            adaptive_font_size = self.calculate_adaptive_font_size()
            char_width_mm = adaptive_font_size * 0.6 * 0.352778
            line_width_mm = len(line) * char_width_mm
            return (self.page_settings.width_mm - self.page_settings.margin_right_mm - line_width_mm)
        else:  # left или justify
            return left_mm


class TextPageManager:
    """Менеджер разбиения текста на страницы"""
    
    def __init__(self, formatter: SmartFormatter):
        self.formatter = formatter
    
    def format_text_to_pages(self, text: str, page_number_reserve_mm: float = 0) -> List[List[str]]:
        """Форматирование текста на страницы"""
        if not text.strip():
            return []
            
        # Адаптивный размер шрифта
        adaptive_font_size = self.formatter.calculate_adaptive_font_size()
        font = QFont(self.formatter.text_settings.font_family, int(adaptive_font_size))
        
        # Получение границ текстовой области
        left, top, right, bottom = self.formatter.get_text_area_bounds()
        max_width_px = right - left
        max_height_px = bottom - top
        
        # Перенос текста по строкам
        wrapped_lines = self.formatter.wrap_text_lines(text, font, max_width_px)
        
        # Разбиение на страницы
        font_metrics = QFontMetrics(font)
        line_height = font_metrics.height() * self.formatter.text_settings.line_spacing
        
        pages = []
        current_page_lines = []
        current_y = 0
        
        # Резерв места для номера страницы
        page_number_reserve_px = self.formatter.mm_to_pixels(page_number_reserve_mm)
        available_height = max_height_px - page_number_reserve_px
        
        for line in wrapped_lines:
            if line == "":  # Пустая строка (новый абзац)
                paragraph_spacing = self.formatter.mm_to_pixels(
                    self.formatter.text_settings.paragraph_spacing_mm
                )
                if current_y + paragraph_spacing > available_height and current_page_lines:
                    # Начать новую страницу
                    pages.append(current_page_lines.copy())
                    current_page_lines = []
                    current_y = 0
                else:
                    current_y += paragraph_spacing
                current_page_lines.append("")
            else:
                if current_y + line_height > available_height and current_page_lines:
                    # Начать новую страницу
                    pages.append(current_page_lines.copy())
                    current_page_lines = []
                    current_y = 0
                
                current_page_lines.append(line)
                current_y += line_height
        
        # Добавить последнюю страницу
        if current_page_lines:
            pages.append(current_page_lines)
        
        # Если нет страниц, создать пустую
        if not pages:
            pages = [[]]
            
        return pages
    
    def get_text_statistics(self, text: str) -> dict:
        """Получение статистики текста"""
        char_count = len(text)
        word_count = len([w for w in text.split() if w.strip()])
        line_count = len(text.split('\n'))
        
        # Расчет страниц
        pages = self.format_text_to_pages(text)
        page_count = len(pages)
        
        return {
            'characters': char_count,
            'words': word_count,
            'lines': line_count,
            'pages': page_count,
            'avg_words_per_page': word_count / page_count if page_count > 0 else 0
        }
    
    def estimate_print_time(self, text: str, chars_per_second: float = 2.0) -> float:
        """Оценка времени печати в секундах"""
        stats = self.get_text_statistics(text)
        return stats['characters'] / chars_per_second
    
    def validate_text_fits(self, text: str) -> Tuple[bool, str]:
        """Проверка, помещается ли текст в заданные параметры"""
        try:
            pages = self.format_text_to_pages(text)
            if not pages:
                return True, "Текст пуст"
            
            # Проверка на слишком длинные слова
            adaptive_font_size = self.formatter.calculate_adaptive_font_size()
            font = QFont(self.formatter.text_settings.font_family, int(adaptive_font_size))
            font_metrics = QFontMetrics(font)
            
            left, top, right, bottom = self.formatter.get_text_area_bounds()
            max_width_px = right - left
            
            for line in text.split('\n'):
                for word in line.split():
                    word_width = font_metrics.horizontalAdvance(word)
                    if word_width > max_width_px:
                        return False, f"Слово '{word}' слишком длинное для текущих настроек"
            
            return True, f"Текст успешно размещен на {len(pages)} страницах"
            
        except Exception as e:
            return False, f"Ошибка валидации: {str(e)}"
