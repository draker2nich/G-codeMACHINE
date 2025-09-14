"""
Модуль конфигурации и настроек приложения.
Содержит dataclass'ы для всех настроек приложения.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class PageSettings:
    """Настройки страницы"""
    width_mm: float = 80.0
    height_mm: float = 60.0
    margin_left_mm: float = 5.0
    margin_right_mm: float = 5.0
    margin_top_mm: float = 5.0
    margin_bottom_mm: float = 5.0
    dpi: int = 96
    grid_size_mm: float = 2.0
    grid_type: str = "клетка"  # "клетка" или "линейка"

    def validate(self) -> bool:
        """Проверка корректности настроек"""
        return (
            self.width_mm > 0 and self.height_mm > 0 and
            self.dpi > 0 and self.grid_size_mm > 0 and
            all(margin >= 0 for margin in [
                self.margin_left_mm, self.margin_right_mm,
                self.margin_top_mm, self.margin_bottom_mm
            ])
        )


@dataclass
class TextSettings:
    """Настройки текста"""
    font_family: str = "Arial"
    font_size_pt: float = 12.0
    line_spacing: float = 1.2
    letter_spacing_mm: float = 0.5
    paragraph_spacing_mm: float = 3.0
    indent_first_line_mm: float = 5.0
    alignment: str = "left"  # "left", "center", "right", "justify"
    auto_font_size: bool = True
    font_fill_ratio: float = 0.8  # коэффициент заполнения клетки

    def validate(self) -> bool:
        """Проверка корректности настроек"""
        return (
            self.font_size_pt > 0 and
            self.line_spacing > 0 and
            0 <= self.font_fill_ratio <= 1 and
            self.alignment in ["left", "center", "right", "justify"]
        )


@dataclass
class PageNumberSettings:
    """Настройки нумерации страниц"""
    enabled: bool = True
    position: str = "bottom_center"  # "top_left", "top_center", "top_right", etc.
    format: str = "- {page} -"
    font_size_pt: float = 10.0
    offset_mm: float = 3.0

    def validate(self) -> bool:
        """Проверка корректности настроек"""
        valid_positions = [
            "top_left", "top_center", "top_right",
            "bottom_left", "bottom_center", "bottom_right"
        ]
        return (
            self.font_size_pt > 0 and
            self.offset_mm >= 0 and
            self.position in valid_positions and
            "{page}" in self.format
        )


@dataclass 
class AppSettings:
    """Общие настройки приложения"""
    page: PageSettings
    text: TextSettings
    page_numbers: PageNumberSettings
    
    def __init__(self):
        self.page = PageSettings()
        self.text = TextSettings()
        self.page_numbers = PageNumberSettings()
    
    def validate_all(self) -> tuple[bool, list[str]]:
        """Проверка всех настроек"""
        errors = []
        
        if not self.page.validate():
            errors.append("Некорректные настройки страницы")
        if not self.text.validate():
            errors.append("Некорректные настройки текста")  
        if not self.page_numbers.validate():
            errors.append("Некорректные настройки нумерации")
            
        return len(errors) == 0, errors


class SettingsManager:
    """Менеджер для сохранения/загрузки настроек"""
    
    def __init__(self, settings_object):
        self.settings = settings_object
    
    def save_app_settings(self, app_settings: AppSettings):
        """Сохранение настроек приложения"""
        # Настройки страницы
        self.settings.setValue("page_width", app_settings.page.width_mm)
        self.settings.setValue("page_height", app_settings.page.height_mm)
        self.settings.setValue("grid_size", app_settings.page.grid_size_mm)
        self.settings.setValue("grid_type", app_settings.page.grid_type)
        self.settings.setValue("dpi", app_settings.page.dpi)
        
        # Поля
        self.settings.setValue("margin_left", app_settings.page.margin_left_mm)
        self.settings.setValue("margin_right", app_settings.page.margin_right_mm)
        self.settings.setValue("margin_top", app_settings.page.margin_top_mm)
        self.settings.setValue("margin_bottom", app_settings.page.margin_bottom_mm)
        
        # Настройки текста
        self.settings.setValue("font_family", app_settings.text.font_family)
        self.settings.setValue("font_size", app_settings.text.font_size_pt)
        self.settings.setValue("auto_font_size", app_settings.text.auto_font_size)
        self.settings.setValue("font_fill_ratio", app_settings.text.font_fill_ratio)
        self.settings.setValue("line_spacing", app_settings.text.line_spacing)
        self.settings.setValue("letter_spacing", app_settings.text.letter_spacing_mm)
        self.settings.setValue("paragraph_spacing", app_settings.text.paragraph_spacing_mm)
        self.settings.setValue("alignment", app_settings.text.alignment)
        self.settings.setValue("indent_first_line", app_settings.text.indent_first_line_mm)
        
        # Настройки нумерации
        self.settings.setValue("page_numbers_enabled", app_settings.page_numbers.enabled)
        self.settings.setValue("page_number_position", app_settings.page_numbers.position)
        self.settings.setValue("page_number_format", app_settings.page_numbers.format)
        self.settings.setValue("page_number_font_size", app_settings.page_numbers.font_size_pt)
        self.settings.setValue("page_number_offset", app_settings.page_numbers.offset_mm)
    
    def load_app_settings(self) -> AppSettings:
        """Загрузка настроек приложения"""
        app_settings = AppSettings()
        
        # Настройки страницы
        app_settings.page.width_mm = float(self.settings.value("page_width", 80.0))
        app_settings.page.height_mm = float(self.settings.value("page_height", 60.0))
        app_settings.page.grid_size_mm = float(self.settings.value("grid_size", 2.0))
        app_settings.page.grid_type = self.settings.value("grid_type", "клетка")
        app_settings.page.dpi = int(self.settings.value("dpi", 96))
        
        # Поля
        app_settings.page.margin_left_mm = float(self.settings.value("margin_left", 5.0))
        app_settings.page.margin_right_mm = float(self.settings.value("margin_right", 5.0))
        app_settings.page.margin_top_mm = float(self.settings.value("margin_top", 5.0))
        app_settings.page.margin_bottom_mm = float(self.settings.value("margin_bottom", 5.0))
        
        # Настройки текста
        app_settings.text.font_family = self.settings.value("font_family", "Arial")
        app_settings.text.font_size_pt = float(self.settings.value("font_size", 12.0))
        app_settings.text.auto_font_size = self.settings.value("auto_font_size", True, type=bool)
        app_settings.text.font_fill_ratio = float(self.settings.value("font_fill_ratio", 0.8))
        app_settings.text.line_spacing = float(self.settings.value("line_spacing", 1.2))
        app_settings.text.letter_spacing_mm = float(self.settings.value("letter_spacing", 0.5))
        app_settings.text.paragraph_spacing_mm = float(self.settings.value("paragraph_spacing", 3.0))
        app_settings.text.alignment = self.settings.value("alignment", "left")
        app_settings.text.indent_first_line_mm = float(self.settings.value("indent_first_line", 5.0))
        
        # Настройки нумерации
        app_settings.page_numbers.enabled = self.settings.value("page_numbers_enabled", True, type=bool)
        app_settings.page_numbers.position = self.settings.value("page_number_position", "bottom_center")
        app_settings.page_numbers.format = self.settings.value("page_number_format", "- {page} -")
        app_settings.page_numbers.font_size_pt = float(self.settings.value("page_number_font_size", 10.0))
        app_settings.page_numbers.offset_mm = float(self.settings.value("page_number_offset", 3.0))
        
        return app_settings
