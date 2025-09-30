"""
GUI модуль - интерфейс текстового редактора
"""

import customtkinter as ctk
import tkinter as tk
from functions import EditorFunctions

class WordClone(ctk.CTk, EditorFunctions):
    def __init__(self):
        ctk.CTk.__init__(self)
        EditorFunctions.__init__(self)
        
        self.title("Текстовый редактор")
        self.geometry("1400x850")
        ctk.set_appearance_mode("dark")
        
        # Состояние приложения
        self.current_file = None
        self.zoom_level = 100
        self.current_font_family = "Arial"
        self.current_font_size = 12
        self.is_bold = False
        self.is_italic = False
        self.is_underline = False
        self.show_ruler = False
        self.show_symbols_visible = False
        
        # Создание интерфейса
        self.create_title_bar()
        self.create_menu_bar()
        self.create_ribbon()
        self.create_text_area()
        self.create_status_bar()
        
    def create_title_bar(self):
        """Строка заголовка с панелью быстрого доступа"""
        title_frame = ctk.CTkFrame(self, height=35, fg_color="#2b2b2b", corner_radius=0)
        title_frame.pack(fill="x")
        title_frame.pack_propagate(False)
        
        # ЛЕВАЯ ЧАСТЬ
        left_section = ctk.CTkFrame(title_frame, fg_color="transparent")
        left_section.pack(side="left", fill="y", padx=5)
        
        icon_label = ctk.CTkLabel(left_section, text="📄", font=("Segoe UI", 14))
        icon_label.pack(side="left", padx=(0, 8))
        
        ctk.CTkButton(
            left_section, text="💾", width=28, height=28,
            fg_color="transparent", hover_color="#3f3f3f",
            font=("Segoe UI", 14), corner_radius=2,
            command=self.save_file
        ).pack(side="left", padx=1)
        
        ctk.CTkButton(
            left_section, text="↶", width=28, height=28,
            fg_color="transparent", hover_color="#3f3f3f",
            font=("Segoe UI", 14), corner_radius=2,
            command=self.undo
        ).pack(side="left", padx=1)
        
        ctk.CTkButton(
            left_section, text="↷", width=28, height=28,
            fg_color="transparent", hover_color="#3f3f3f",
            font=("Segoe UI", 14), corner_radius=2,
            command=self.redo
        ).pack(side="left", padx=1)
        
        # ЦЕНТР
        center_section = ctk.CTkFrame(title_frame, fg_color="transparent")
        center_section.pack(side="left", expand=True, fill="both")
        
        self.doc_title = ctk.CTkLabel(
            center_section, text="Документ1",
            font=("Segoe UI", 11), text_color="#ffffff"
        )
        self.doc_title.pack(expand=True)
        
        # ПРАВАЯ ЧАСТЬ
        right_section = ctk.CTkFrame(title_frame, fg_color="transparent")
        right_section.pack(side="right", fill="y", padx=5)
        
        ctk.CTkButton(
            right_section, text="Примечания", width=90, height=28,
            fg_color="transparent", hover_color="#3f3f3f",
            font=("Segoe UI", 9), corner_radius=2,
            command=self.show_notes
        ).pack(side="left", padx=2)
        
        ctk.CTkButton(
            right_section, text="Встреча", width=70, height=28,
            fg_color="transparent", hover_color="#3f3f3f",
            font=("Segoe UI", 9), corner_radius=2,
            command=self.schedule_meeting
        ).pack(side="left", padx=2)
        
        ctk.CTkButton(
            right_section, text="Редактирование ▼", width=110, height=28,
            fg_color="transparent", hover_color="#3f3f3f",
            font=("Segoe UI", 10), corner_radius=2,
            command=self.show_edit_mode_menu
        ).pack(side="left", padx=2)
        
        ctk.CTkButton(
            right_section, text="📤", width=28, height=28,
            fg_color="#0078d4", hover_color="#1084d8",
            font=("Segoe UI", 12), corner_radius=2,
            command=self.share_document
        ).pack(side="left", padx=2)
        
    def create_menu_bar(self):
        """Вкладки меню"""
        self.menu_frame = ctk.CTkFrame(self, height=30, fg_color="#2b2b2b", corner_radius=0)
        self.menu_frame.pack(fill="x")
        self.menu_frame.pack_propagate(False)
        
        menu_items = ["Файл", "Главная", "Вставка", "Макет", "Ссылки", 
                      "Рецензирование", "Вид", "Справка"]
        
        self.menu_buttons = {}
        for item in menu_items:
            btn = ctk.CTkButton(
                self.menu_frame, text=item, width=85, height=26,
                fg_color="transparent", hover_color="#3f3f3f",
                corner_radius=0, font=("Segoe UI", 10),
                text_color="#ffffff", border_width=0,
                command=lambda x=item: self.switch_tab(x)
            )
            btn.pack(side="left", padx=1, pady=2)
            self.menu_buttons[item] = btn
        
        self.active_tab = "Главная"
        self.menu_buttons["Главная"].configure(fg_color="#3f3f3f")
        
    def switch_tab(self, tab_name):
        """Переключение между вкладками"""
        self.menu_buttons[self.active_tab].configure(fg_color="transparent")
        self.active_tab = tab_name
        self.menu_buttons[tab_name].configure(fg_color="#3f3f3f")
        
        if tab_name == "Файл":
            self.show_file_menu()
        elif tab_name == "Вставка":
            self.show_insert_menu()
        elif tab_name == "Вид":
            self.show_view_menu()
        elif tab_name == "Справка":
            self.show_help_menu()
        
    def create_ribbon(self):
        """Лента инструментов"""
        self.ribbon_frame = ctk.CTkFrame(self, height=105, fg_color="#2b2b2b", corner_radius=0)
        self.ribbon_frame.pack(fill="x")
        self.ribbon_frame.pack_propagate(False)
        
        main_container = ctk.CTkFrame(self.ribbon_frame, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=6, pady=5)
        
        self.create_clipboard_group(main_container)
        self.add_separator(main_container)
        self.create_font_group(main_container)
        self.add_separator(main_container)
        self.create_paragraph_group(main_container)
        self.add_separator(main_container)
        self.create_styles_group(main_container)
        self.add_separator(main_container)
        self.create_editing_group(main_container)
        
    def add_separator(self, parent):
        """Добавить разделитель"""
        sep = ctk.CTkFrame(parent, width=1, fg_color="#404040")
        sep.pack(side="left", fill="y", padx=6, pady=8)
        
    def create_clipboard_group(self, parent):
        """Группа: Буфер обмена"""
        group = ctk.CTkFrame(parent, fg_color="transparent")
        group.pack(side="left", padx=3)
        
        ctk.CTkButton(
            group, text="📋\nВставить", width=45, height=60,
            fg_color="#0078d4", hover_color="#1084d8",
            font=("Segoe UI", 9), corner_radius=2,
            command=self.paste
        ).pack(side="left", padx=(0, 2))
        
        right_col = ctk.CTkFrame(group, fg_color="transparent")
        right_col.pack(side="left")
        
        ctk.CTkButton(
            right_col, text="✂ Вырезать", width=75, height=18,
            fg_color="transparent", hover_color="#3f3f3f",
            font=("Segoe UI", 8), corner_radius=2,
            anchor="w", command=self.cut
        ).pack(pady=(0, 1))
        
        ctk.CTkButton(
            right_col, text="📄 Копировать", width=75, height=18,
            fg_color="transparent", hover_color="#3f3f3f",
            font=("Segoe UI", 8), corner_radius=2,
            anchor="w", command=self.copy
        ).pack(pady=1)
        
        ctk.CTkButton(
            right_col, text="🖌 Формат", width=75, height=18,
            fg_color="transparent", hover_color="#3f3f3f",
            font=("Segoe UI", 8), corner_radius=2,
            anchor="w", command=self.format_painter
        ).pack(pady=(1, 0))
        
    def create_font_group(self, parent):
        """Группа: Шрифт"""
        group = ctk.CTkFrame(parent, fg_color="transparent")
        group.pack(side="left", padx=3)
        
        # СТРОКА 1: Шрифт и размер
        row1 = ctk.CTkFrame(group, fg_color="transparent", height=26)
        row1.pack(fill="x", pady=(0, 2))
        row1.pack_propagate(False)
        
        self.font_family = ctk.CTkComboBox(
            row1, values=["Arial", "Calibri", "Aptos", "Times New Roman", "Courier New", "Georgia", "Verdana"],
            width=130, height=24, font=("Segoe UI", 9),
            command=self.change_font_family, corner_radius=2,
            border_width=1, border_color="#555555",
            button_color="#0078d4", fg_color="#3a3a3a"
        )
        self.font_family.set("Arial")
        self.font_family.pack(side="left", padx=(0, 2))
        
        self.font_size = ctk.CTkComboBox(
            row1, values=["8", "9", "10", "11", "12", "14", "16", "18", "20", "24", "28", "32", "36", "48", "72"],
            width=50, height=24, font=("Segoe UI", 9),
            command=self.change_font_size, corner_radius=2,
            border_width=1, border_color="#555555",
            button_color="#0078d4", fg_color="#3a3a3a"
        )
        self.font_size.set("12")
        self.font_size.pack(side="left", padx=2)
        
        ctk.CTkButton(
            row1, text="▲", width=24, height=24,
            fg_color="transparent", hover_color="#3f3f3f",
            font=("Segoe UI", 8), corner_radius=2,
            command=self.increase_font
        ).pack(side="left", padx=1)
        
        ctk.CTkButton(
            row1, text="▼", width=24, height=24,
            fg_color="transparent", hover_color="#3f3f3f",
            font=("Segoe UI", 8), corner_radius=2,
            command=self.decrease_font
        ).pack(side="left", padx=1)
        
        # СТРОКА 2: Форматирование
        row2 = ctk.CTkFrame(group, fg_color="transparent", height=26)
        row2.pack(fill="x", pady=2)
        row2.pack_propagate(False)
        
        self.bold_btn = ctk.CTkButton(
            row2, text="Ж", width=24, height=24,
            fg_color="transparent", hover_color="#3f3f3f",
            font=("Segoe UI", 10, "bold"), corner_radius=2,
            command=self.toggle_bold
        )
        self.bold_btn.pack(side="left", padx=1)
        
        self.italic_btn = ctk.CTkButton(
            row2, text="К", width=24, height=24,
            fg_color="transparent", hover_color="#3f3f3f",
            font=("Segoe UI", 10, "italic"), corner_radius=2,
            command=self.toggle_italic
        )
        self.italic_btn.pack(side="left", padx=1)
        
        self.underline_btn = ctk.CTkButton(
            row2, text="Ч", width=24, height=24,
            fg_color="transparent", hover_color="#3f3f3f",
            font=("Segoe UI", 10, "underline"), corner_radius=2,
            command=self.toggle_underline
        )
        self.underline_btn.pack(side="left", padx=1)
        
        ctk.CTkButton(
            row2, text="abc", width=24, height=24,
            fg_color="transparent", hover_color="#3f3f3f",
            font=("Segoe UI", 10, "overstrike"), corner_radius=2,
            command=self.toggle_strikethrough
        ).pack(side="left", padx=1)
        
        ctk.CTkButton(
            row2, text="x₂", width=24, height=24,
            fg_color="transparent", hover_color="#3f3f3f",
            font=("Segoe UI", 10), corner_radius=2,
            command=self.insert_subscript
        ).pack(side="left", padx=1)
        
        ctk.CTkButton(
            row2, text="x²", width=24, height=24,
            fg_color="transparent", hover_color="#3f3f3f",
            font=("Segoe UI", 10), corner_radius=2,
            command=self.insert_superscript
        ).pack(side="left", padx=1)
        
        # СТРОКА 3: Эффекты и цвета
        row3 = ctk.CTkFrame(group, fg_color="transparent", height=26)
        row3.pack(fill="x", pady=(2, 0))
        row3.pack_propagate(False)
        
        ctk.CTkButton(
            row3, text="Aa", width=24, height=24,
            fg_color="transparent", hover_color="#3f3f3f",
            font=("Segoe UI", 10), corner_radius=2,
            command=self.change_case
        ).pack(side="left", padx=1)
        
        ctk.CTkButton(
            row3, text="A", width=24, height=24,
            fg_color="transparent", hover_color="#3f3f3f",
            font=("Segoe UI", 10), corner_radius=2,
            command=self.clear_format
        ).pack(side="left", padx=1)
        
        ctk.CTkButton(
            row3, text="🖍", width=24, height=24,
            fg_color="transparent", hover_color="#3f3f3f",
            font=("Segoe UI", 10), corner_radius=2,
            command=self.change_bg_color
        ).pack(side="left", padx=1)
        
        self.text_color_btn = ctk.CTkButton(
            row3, text="А", width=24, height=24,
            fg_color="#c83232", hover_color="#d84040",
            font=("Segoe UI", 11, "bold"), corner_radius=2,
            command=self.change_text_color
        )
        self.text_color_btn.pack(side="left", padx=1)
        
    def create_paragraph_group(self, parent):
        """Группа: Абзац"""
        group = ctk.CTkFrame(parent, fg_color="transparent")
        group.pack(side="left", padx=3)
        
        # СТРОКА 1: Списки и отступы
        row1 = ctk.CTkFrame(group, fg_color="transparent", height=26)
        row1.pack(fill="x", pady=(0, 2))
        row1.pack_propagate(False)
        
        ctk.CTkButton(
            row1, text="• ▼", width=32, height=24,
            fg_color="transparent", hover_color="#3f3f3f",
            font=("Segoe UI", 9), corner_radius=2,
            command=self.insert_bullet
        ).pack(side="left", padx=1)
        
        ctk.CTkButton(
            row1, text="1. ▼", width=32, height=24,
            fg_color="transparent", hover_color="#3f3f3f",
            font=("Segoe UI", 9), corner_radius=2,
            command=self.insert_numbered
        ).pack(side="left", padx=1)
        
        ctk.CTkButton(
            row1, text="≡ ▼", width=32, height=24,
            fg_color="transparent", hover_color="#3f3f3f",
            font=("Segoe UI", 9), corner_radius=2,
            command=self.insert_multilevel
        ).pack(side="left", padx=1)
        
        ctk.CTkButton(
            row1, text="◁", width=24, height=24,
            fg_color="transparent", hover_color="#3f3f3f",
            font=("Segoe UI", 10), corner_radius=2,
            command=self.decrease_indent
        ).pack(side="left", padx=1)
        
        ctk.CTkButton(
            row1, text="▷", width=24, height=24,
            fg_color="transparent", hover_color="#3f3f3f",
            font=("Segoe UI", 10), corner_radius=2,
            command=self.increase_indent
        ).pack(side="left", padx=1)
        
        # СТРОКА 2: Выравнивание
        row2 = ctk.CTkFrame(group, fg_color="transparent", height=26)
        row2.pack(fill="x", pady=2)
        row2.pack_propagate(False)
        
        ctk.CTkButton(
            row2, text="AZ", width=24, height=24,
            fg_color="transparent", hover_color="#3f3f3f",
            font=("Segoe UI", 8), corner_radius=2,
            command=self.sort_text
        ).pack(side="left", padx=1)
        
        self.symbols_btn = ctk.CTkButton(
            row2, text="¶", width=24, height=24,
            fg_color="transparent", hover_color="#3f3f3f",
            font=("Segoe UI", 12), corner_radius=2,
            command=self.toggle_symbols
        )
        self.symbols_btn.pack(side="left", padx=1)
        
        ctk.CTkButton(
            row2, text="≡", width=24, height=24,
            fg_color="transparent", hover_color="#3f3f3f",
            font=("Segoe UI", 10), corner_radius=2,
            command=lambda: self.align_text("left")
        ).pack(side="left", padx=1)
        
        ctk.CTkButton(
            row2, text="≡", width=24, height=24,
            fg_color="transparent", hover_color="#3f3f3f",
            font=("Segoe UI", 10), corner_radius=2,
            command=lambda: self.align_text("center")
        ).pack(side="left", padx=1)
        
        ctk.CTkButton(
            row2, text="≡", width=24, height=24,
            fg_color="transparent", hover_color="#3f3f3f",
            font=("Segoe UI", 10), corner_radius=2,
            command=lambda: self.align_text("right")
        ).pack(side="left", padx=1)
        
        ctk.CTkButton(
            row2, text="≡", width=24, height=24,
            fg_color="transparent", hover_color="#3f3f3f",
            font=("Segoe UI", 10), corner_radius=2,
            command=lambda: self.align_text("justify")
        ).pack(side="left", padx=1)
        
        # СТРОКА 3: Интервал и заливка
        row3 = ctk.CTkFrame(group, fg_color="transparent", height=26)
        row3.pack(fill="x", pady=(2, 0))
        row3.pack_propagate(False)
        
        ctk.CTkButton(
            row3, text="⇅", width=24, height=24,
            fg_color="transparent", hover_color="#3f3f3f",
            font=("Segoe UI", 12), corner_radius=2,
            command=self.change_line_spacing
        ).pack(side="left", padx=1)
        
        ctk.CTkButton(
            row3, text="🎨", width=24, height=24,
            fg_color="transparent", hover_color="#3f3f3f",
            font=("Segoe UI", 10), corner_radius=2,
            command=self.change_paragraph_fill
        ).pack(side="left", padx=1)
        
        ctk.CTkButton(
            row3, text="⊞", width=24, height=24,
            fg_color="transparent", hover_color="#3f3f3f",
            font=("Segoe UI", 12), corner_radius=2,
            command=self.add_borders
        ).pack(side="left", padx=1)
        
    def create_styles_group(self, parent):
        """Группа: Стили"""
        group = ctk.CTkFrame(parent, fg_color="transparent")
        group.pack(side="left", padx=3)
        
        ctk.CTkLabel(group, text="Стили", font=("Segoe UI", 8), text_color="#909090").pack(anchor="w", pady=(0, 2))
        
        styles_row = ctk.CTkFrame(group, fg_color="transparent")
        styles_row.pack()
        
        ctk.CTkButton(
            styles_row, text="Обычный", width=85, height=38,
            fg_color="#0078d4", hover_color="#1084d8",
            font=("Segoe UI", 9), corner_radius=2,
            command=lambda: self.apply_style("normal")
        ).pack(side="left", padx=2)
        
        ctk.CTkButton(
            styles_row, text="Без интервала", width=85, height=38,
            fg_color="#0078d4", hover_color="#1084d8",
            font=("Segoe UI", 8), corner_radius=2,
            command=lambda: self.apply_style("no_spacing")
        ).pack(side="left", padx=2)
        
        ctk.CTkButton(
            styles_row, text="Заголовок", width=85, height=38,
            fg_color="#0078d4", hover_color="#1084d8",
            font=("Segoe UI", 9, "bold"), corner_radius=2,
            command=lambda: self.apply_style("heading")
        ).pack(side="left", padx=2)
        
    def create_editing_group(self, parent):
        """Группа: Редактирование"""
        group = ctk.CTkFrame(parent, fg_color="transparent")
        group.pack(side="left", padx=3)
        
        ctk.CTkLabel(group, text="Редактирование", font=("Segoe UI", 8), text_color="#909090").pack(anchor="w", pady=(0, 2))
        
        ctk.CTkButton(
            group, text="🔍 Найти", width=75, height=18,
            fg_color="transparent", hover_color="#3f3f3f",
            font=("Segoe UI", 8), corner_radius=2,
            anchor="w", command=self.find_text
        ).pack(pady=(0, 1))
        
        ctk.CTkButton(
            group, text="🔄 Заменить", width=75, height=18,
            fg_color="transparent", hover_color="#3f3f3f",
            font=("Segoe UI", 8), corner_radius=2,
            anchor="w", command=self.replace_text
        ).pack(pady=1)
        
        ctk.CTkButton(
            group, text="▣ Выделить", width=75, height=18,
            fg_color="transparent", hover_color="#3f3f3f",
            font=("Segoe UI", 8), corner_radius=2,
            anchor="w", command=self.select_all
        ).pack(pady=(1, 0))
        
    def create_text_area(self):
        """Рабочая область"""
        text_container = ctk.CTkFrame(self, fg_color="#1e1e1e", corner_radius=0)
        text_container.pack(fill="both", expand=True)
        
        self.text_area = tk.Text(
            text_container, wrap="word", font=("Arial", 12),
            bg="#1e1e1e", fg="#ffffff",
            insertbackground="#ffffff",
            selectbackground="#0078d4",
            selectforeground="#ffffff",
            relief="flat", padx=80, pady=30,
            spacing1=3, spacing3=3, undo=True, maxundo=-1
        )
        self.text_area.pack(side="left", fill="both", expand=True)
        
        scrollbar = ctk.CTkScrollbar(text_container, command=self.text_area.yview)
        scrollbar.pack(side="right", fill="y", padx=(0, 1))
        self.text_area.configure(yscrollcommand=scrollbar.set)
        
        self.bind_shortcuts()
        
    def create_status_bar(self):
        """Строка состояния"""
        self.status_frame = ctk.CTkFrame(self, height=24, fg_color="#1e1e1e", corner_radius=0)
        self.status_frame.pack(fill="x", side="bottom")
        self.status_frame.pack_propagate(False)
        
        left_status = ctk.CTkFrame(self.status_frame, fg_color="transparent")
        left_status.pack(side="left", fill="y")
        
        self.page_label = ctk.CTkLabel(
            left_status, text="Страница 1 из 1    Число слов: 0    Русский",
            font=("Segoe UI", 9), text_color="#909090"
        )
        self.page_label.pack(side="left", padx=10, pady=2)
        
        right_status = ctk.CTkFrame(self.status_frame, fg_color="transparent")
        right_status.pack(side="right", fill="y", padx=5)
        
        ctk.CTkButton(
            right_status, text="📖", width=24, height=20,
            fg_color="transparent", hover_color="#3f3f3f",
            font=("Segoe UI", 10), corner_radius=2,
            command=self.reading_mode
        ).pack(side="left", padx=1)
        
        ctk.CTkButton(
            right_status, text="📄", width=24, height=20,
            fg_color="#0078d4", hover_color="#1084d8",
            font=("Segoe UI", 10), corner_radius=2,
            command=self.print_layout_mode
        ).pack(side="left", padx=1)
        
        ctk.CTkButton(
            right_status, text="🌐", width=24, height=20,
            fg_color="transparent", hover_color="#3f3f3f",
            font=("Segoe UI", 10), corner_radius=2,
            command=self.web_layout_mode
        ).pack(side="left", padx=1)
        
        ctk.CTkButton(
            right_status, text="-", width=24, height=20,
            fg_color="transparent", hover_color="#3f3f3f",
            font=("Segoe UI", 12), corner_radius=2,
            command=self.zoom_out
        ).pack(side="left", padx=(10, 2))
        
        self.zoom_slider = ctk.CTkSlider(
            right_status, from_=50, to=200, width=100, height=16,
            command=self.zoom_change
        )
        self.zoom_slider.set(100)
        self.zoom_slider.pack(side="left", padx=2)
        
        ctk.CTkButton(
            right_status, text="+", width=24, height=20,
            fg_color="transparent", hover_color="#3f3f3f",
            font=("Segoe UI", 12), corner_radius=2,
            command=self.zoom_in
        ).pack(side="left", padx=2)
        
        self.zoom_label = ctk.CTkLabel(
            right_status, text="100%", width=40,
            font=("Segoe UI", 9), text_color="#909090"
        )
        self.zoom_label.pack(side="left", padx=2)
        
        ctk.CTkButton(
            right_status, text="⬌", width=30, height=20,
            fg_color="transparent", hover_color="#3f3f3f",
            font=("Segoe UI", 10), corner_radius=2,
            command=self.fit_to_width
        ).pack(side="left", padx=2)
        
        self.text_area.bind("<KeyRelease>", self.update_status)
        
    def bind_shortcuts(self):
        """Привязка горячих клавиш"""
        self.bind("<Control-b>", lambda e: self.toggle_bold())
        self.bind("<Control-i>", lambda e: self.toggle_italic())
        self.bind("<Control-u>", lambda e: self.toggle_underline())
        self.bind("<Control-s>", lambda e: self.save_file())
        self.bind("<Control-o>", lambda e: self.open_file())
        self.bind("<Control-n>", lambda e: self.new_file())
        self.bind("<Control-f>", lambda e: self.find_text())
        self.bind("<Control-h>", lambda e: self.replace_text())
        self.bind("<Control-z>", lambda e: self.undo())
        self.bind("<Control-y>", lambda e: self.redo())
        self.bind("<Control-a>", lambda e: self.select_all())
        self.bind("<Control-p>", lambda e: self.print_document())