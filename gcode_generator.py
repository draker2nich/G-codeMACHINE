"""
Модуль генерации G-code.
Содержит класс для умной генерации G-code из отформатированного текста
с поддержкой многостраничности и различных шрифтов.
"""

from typing import List
from PySide6.QtCore import QThread, Signal

from config import PageSettings, TextSettings, PageNumberSettings
from text_formatter import SmartFormatter


class SmartGCodeGenerator(QThread):
    """Умный генератор G-code с поддержкой многостраничности"""
    
    finished = Signal(str)
    error = Signal(str)
    progress = Signal(int)
    status_update = Signal(str)
    
    def __init__(self, formatted_pages: List[List[str]], 
                 page_settings: PageSettings, 
                 text_settings: TextSettings,
                 page_number_settings: PageNumberSettings):
        super().__init__()
        self.formatted_pages = formatted_pages
        self.page_settings = page_settings
        self.text_settings = text_settings
        self.page_number_settings = page_number_settings
        self.smart_formatter = SmartFormatter(page_settings, text_settings)
        
        # Настройки G-code
        self.travel_speed = 3000  # мм/мин для холостого хода
        self.draw_speed = 1500    # мм/мин для рисования
        self.pen_lift_command = "M5"  # команда поднятия пера
        self.pen_down_command = "M3"  # команда опускания пера
    
    def run(self):
        """Основной метод выполнения генерации"""
        try:
            self.status_update.emit("Начинаем генерацию G-code...")
            gcode = self.generate_smart_gcode()
            self.finished.emit(gcode)
        except Exception as e:
            self.error.emit(str(e))
    
    def generate_smart_gcode(self) -> str:
        """Генерация умного G-code"""
        gcode_lines = [
            "; ===== G-code для умной drawing machine (Arduino) =====",
            f"; Страниц: {len(self.formatted_pages)}",
            f"; Размер листа: {self.page_settings.width_mm}x{self.page_settings.height_mm} мм",
            f"; Шрифт: {self.text_settings.font_family}",
            f"; Размер шрифта: {self.smart_formatter.calculate_adaptive_font_size():.1f}pt (адаптивный)",
            f"; Выравнивание: {self.text_settings.alignment}",
            f"; Сетка: {self.page_settings.grid_type} {self.page_settings.grid_size_mm}мм",
            f"; Генератор: Smart G-code Studio Pro v3.0",
            "",
            "; === Инициализация ===",
            "G90 ; Абсолютное позиционирование",
            "G21 ; Миллиметры",
            "G28 ; Домой",
            f"{self.pen_lift_command} ; Поднять перо",
            f"G0 F{self.travel_speed} ; Скорость холостого хода",
            f"G1 F{self.draw_speed} ; Скорость рисования",
            ""
        ]
        
        total_lines = sum(len(page) for page in self.formatted_pages)
        processed_lines = 0
        
        for page_index, page_lines in enumerate(self.formatted_pages):
            self.status_update.emit(f"Обрабатываем страницу {page_index + 1}...")
            
            page_gcode = self.generate_page_gcode(page_index, page_lines)
            gcode_lines.extend(page_gcode)
            
            processed_lines += len(page_lines)
            progress_percent = int((processed_lines / total_lines) * 100) if total_lines > 0 else 100
            self.progress.emit(progress_percent)
            
            # Пауза между страницами
            if page_index < len(self.formatted_pages) - 1:
                gcode_lines.extend([
                    "",
                    f"; === Конец страницы {page_index + 1} ===",
                    f"{self.pen_lift_command} ; Поднять перо",
                    "G0 X0 Y0 ; Возврат в исходную позицию",
                    "M0 ; Пауза для смены листа",
                    f"; === Начало страницы {page_index + 2} ===",
                    ""
                ])
        
        # Завершение
        gcode_lines.extend([
            "",
            "; === Завершение программы ===",
            f"{self.pen_lift_command} ; Поднять перо",
            "G0 X0 Y0 ; Возврат домой",
            "M30 ; Конец программы",
            f"; Всего страниц обработано: {len(self.formatted_pages)}",
            f"; Общее количество строк: {total_lines}"
        ])
        
        self.status_update.emit("G-code готов!")
        return '\n'.join(gcode_lines)
    
    def generate_page_gcode(self, page_index: int, page_lines: List[str]) -> List[str]:
        """Генерация G-code для одной страницы"""
        gcode_lines = [f"; === Страница {page_index + 1} ==="]
        
        # Границы текстовой области
        left_mm, top_mm, right_mm, bottom_mm = self.smart_formatter.get_text_area_bounds_mm()
        
        # Параметры шрифта
        adaptive_font_size = self.smart_formatter.calculate_adaptive_font_size()
        char_width_mm = self.calculate_char_width_mm(adaptive_font_size)
        line_height_mm = self.calculate_line_height_mm(adaptive_font_size)
        
        current_y_mm = top_mm
        pen_down = False
        
        for line_index, line in enumerate(page_lines):
            if line == "":  # Пустая строка
                current_y_mm += self.text_settings.paragraph_spacing_mm
                continue
            
            # Выравнивание по сетке
            aligned_y_mm = self.smart_formatter.align_to_grid_mm(current_y_mm)
            
            # Позиция X в зависимости от выравнивания
            line_x_mm = self.smart_formatter.calculate_line_x_position_mm(line, left_mm)
            aligned_x_mm = self.smart_formatter.align_to_grid_mm(line_x_mm)
            
            # Переход к началу строки
            if pen_down:
                gcode_lines.append(f"{self.pen_lift_command} ; Поднять перо")
                pen_down = False
            
            gcode_lines.append(
                f"G0 X{aligned_x_mm:.2f} Y{aligned_y_mm:.2f} "
                f"; Строка {line_index + 1}: {line[:30]}{'...' if len(line) > 30 else ''}"
            )
            
            # Рисование символов
            char_x_mm = aligned_x_mm
            
            for char_index, char in enumerate(line):
                if char == ' ':
                    char_x_mm += char_width_mm + self.text_settings.letter_spacing_mm
                    continue
                
                if not pen_down:
                    gcode_lines.append(f"{self.pen_down_command} ; Опустить перо")
                    pen_down = True
                
                # Рисование символа
                char_moves = self.generate_char_gcode(
                    char, char_x_mm, aligned_y_mm, char_width_mm, line_height_mm
                )
                gcode_lines.extend(char_moves)
                
                char_x_mm += char_width_mm + self.text_settings.letter_spacing_mm
            
            if pen_down:
                gcode_lines.append(f"{self.pen_lift_command} ; Поднять перо")
                pen_down = False
            
            current_y_mm += line_height_mm
        
        # Номер страницы
        if self.page_number_settings.enabled:
            page_number_gcode = self.generate_page_number_gcode(page_index)
            gcode_lines.extend(page_number_gcode)
        
        return gcode_lines
    
    def calculate_char_width_mm(self, font_size_pt: float) -> float:
        """Расчет ширины символа в мм"""
        return font_size_pt * 0.6 * 0.352778  # pt to mm approximation
    
    def calculate_line_height_mm(self, font_size_pt: float) -> float:
        """Расчет высоты строки в мм"""
        return font_size_pt * 1.2 * 0.352778 * self.text_settings.line_spacing
    
    def generate_char_gcode(self, char: str, x_mm: float, y_mm: float, 
                          width_mm: float, height_mm: float) -> List[str]:
        """Генерация G-code для символа"""
        # Простая реализация - прямоугольник для каждого символа
        # В реальном приложении здесь могут быть векторные шрифты
        
        moves = [f"; Символ '{char}' в позиции ({x_mm:.2f}, {y_mm:.2f})"]
        
        # Определение размеров символа
        char_height = height_mm * 0.8
        char_width = width_mm * 0.8
        
        # Рисование символа как простого прямоугольника
        if char.isalnum() or char in ".,!?;:":
            moves.extend([
                f"G1 X{x_mm:.2f} Y{y_mm:.2f}",
                f"G1 X{x_mm + char_width:.2f} Y{y_mm:.2f}",
                f"G1 X{x_mm + char_width:.2f} Y{y_mm + char_height:.2f}",
                f"G1 X{x_mm:.2f} Y{y_mm + char_height:.2f}",
                f"G1 X{x_mm:.2f} Y{y_mm:.2f}"
            ])
        elif char in "-_":
            # Горизонтальная линия
            moves.extend([
                f"G1 X{x_mm:.2f} Y{y_mm + char_height/2:.2f}",
                f"G1 X{x_mm + char_width:.2f} Y{y_mm + char_height/2:.2f}"
            ])
        elif char in "|":
            # Вертикальная линия
            moves.extend([
                f"G1 X{x_mm + char_width/2:.2f} Y{y_mm:.2f}",
                f"G1 X{x_mm + char_width/2:.2f} Y{y_mm + char_height:.2f}"
            ])
        else:
            # Точка для неизвестных символов
            moves.extend([
                f"G1 X{x_mm + char_width/2:.2f} Y{y_mm + char_height/2:.2f}",
                f"G1 X{x_mm + char_width/2 + 0.5:.2f} Y{y_mm + char_height/2:.2f}"
            ])
        
        return moves
    
    def generate_page_number_gcode(self, page_index: int) -> List[str]:
        """Генерация G-code для номера страницы"""
        page_number_text = self.page_number_settings.format.format(
            page=page_index + 1,
            total=len(self.formatted_pages)
        )
        
        # Позиция номера страницы
        offset_mm = self.page_number_settings.offset_mm
        
        if "bottom" in self.page_number_settings.position:
            y_mm = self.page_settings.height_mm - offset_mm
        elif "top" in self.page_number_settings.position:
            y_mm = offset_mm
        else:
            y_mm = self.page_settings.height_mm / 2
        
        if "center" in self.page_number_settings.position:
            x_mm = self.page_settings.width_mm / 2
        elif "right" in self.page_number_settings.position:
            x_mm = self.page_settings.width_mm - offset_mm
        else:
            x_mm = offset_mm
        
        gcode_lines = [
            "",
            f"; Номер страницы: {page_number_text}",
            f"G0 X{x_mm:.2f} Y{y_mm:.2f}",
            f"{self.pen_down_command} ; Опустить перо"
        ]
        
        # Рисование текста номера страницы
        char_width_mm = self.calculate_char_width_mm(self.page_number_settings.font_size_pt)
        char_height_mm = self.calculate_line_height_mm(self.page_number_settings.font_size_pt)
        char_x_mm = x_mm
        
        for char in page_number_text:
            if char != ' ':
                char_moves = self.generate_char_gcode(
                    char, char_x_mm, y_mm, char_width_mm, char_height_mm
                )
                gcode_lines.extend(char_moves)
            char_x_mm += char_width_mm
        
        gcode_lines.append(f"{self.pen_lift_command} ; Поднять перо")
        
        return gcode_lines
    
    def set_machine_settings(self, travel_speed: int = 3000, draw_speed: int = 1500,
                           pen_lift: str = "M5", pen_down: str = "M3"):
        """Настройка параметров станка"""
        self.travel_speed = travel_speed
        self.draw_speed = draw_speed
        self.pen_lift_command = pen_lift
        self.pen_down_command = pen_down
    
    def estimate_print_time(self) -> dict:
        """Оценка времени печати"""
        total_chars = sum(sum(len(line) for line in page if line) for page in self.formatted_pages)
        
        # Примерная оценка времени
        draw_time_sec = total_chars * 2  # 2 секунды на символ
        travel_time_sec = len(self.formatted_pages) * 30  # 30 секунд на смену страницы
        
        total_time_sec = draw_time_sec + travel_time_sec
        
        return {
            'total_seconds': total_time_sec,
            'minutes': total_time_sec // 60,
            'hours': total_time_sec // 3600,
            'draw_time': draw_time_sec,
            'travel_time': travel_time_sec,
            'characters': total_chars
        }


class GCodeValidator:
    """Валидатор G-code"""
    
    @staticmethod
    def validate_gcode(gcode: str) -> tuple[bool, list[str]]:
        """Проверка корректности G-code"""
        lines = gcode.split('\n')
        errors = []
        warnings = []
        
        has_init = False
        has_end = False
        current_x, current_y = 0.0, 0.0
        
        for line_num, line in enumerate(lines, 1):
            line = line.strip()
            
            # Пропуск комментариев и пустых строк
            if not line or line.startswith(';'):
                continue
            
            # Проверка инициализации
            if 'G90' in line or 'G21' in line or 'G28' in line:
                has_init = True
            
            # Проверка завершения
            if 'M30' in line:
                has_end = True
            
            # Проверка координат
            if line.startswith('G0') or line.startswith('G1'):
                try:
                    # Парсинг координат
                    if 'X' in line:
                        x_pos = line.find('X')
                        x_str = line[x_pos+1:].split()[0]
                        current_x = float(x_str)
                    
                    if 'Y' in line:
                        y_pos = line.find('Y')
                        y_str = line[y_pos+1:].split()[0]
                        current_y = float(y_str)
                        
                except ValueError:
                    errors.append(f"Строка {line_num}: Некорректные координаты в '{line}'")
            
            # Проверка выхода за границы (предполагаем максимум 200x200мм)
            if abs(current_x) > 200 or abs(current_y) > 200:
                warnings.append(f"Строка {line_num}: Координаты выходят за пределы ({current_x}, {current_y})")
        
        if not has_init:
            errors.append("Отсутствует инициализация (G90, G21, G28)")
        
        if not has_end:
            warnings.append("Отсутствует команда завершения (M30)")
        
        return len(errors) == 0, errors + warnings
