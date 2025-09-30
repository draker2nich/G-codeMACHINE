import customtkinter as ctk
from tkinter import font as tkfont
import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox

class WordClone(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Текстовый редактор")
        self.geometry("1400x850")
        
        ctk.set_appearance_mode("dark")
        
        self.current_file = None
        self.zoom_level = 100
        self.current_font_family = "Arial"
        self.current_font_size = 12
        self.is_bold = False
        self.is_italic = False
        self.is_underline = False
        
        self.create_title_bar()
        self.create_menu_bar()
        self.create_ribbon()
        self.create_text_area()
        self.create_status_bar()
        
    def create_title_bar(self):
        title_frame = ctk.CTkFrame(self, height=35, fg_color="#2b2b2b", corner_radius=0)
        title_frame.pack(fill="x")
        title_frame.pack_propagate(False)
        
        left_section = ctk.CTkFrame(title_frame, fg_color="transparent")
        left_section.pack(side="left", fill="y", padx=5)
        
        icon_label = ctk.CTkLabel(left_section, text="📄", font=("Segoe UI", 14))
        icon_label.pack(side="left", padx=(0, 8))
        
        save_btn = ctk.CTkButton(
            left_section, text="💾", width=28, height=28,
            fg_color="transparent", hover_color="#3f3f3f",
            font=("Segoe UI", 14), corner_radius=2,
            command=self.save_file
        )
        save_btn.pack(side="left", padx=1)
        
        undo_btn = ctk.CTkButton(
            left_section, text="↶", width=28, height=28,
            fg_color="transparent", hover_color="#3f3f3f",
            font=("Segoe UI", 14), corner_radius=2,
            command=self.undo
        )
        undo_btn.pack(side="left", padx=1)
        
        redo_btn = ctk.CTkButton(
            left_section, text="↷", width=28, height=28,
            fg_color="transparent", hover_color="#3f3f3f",
            font=("Segoe UI", 14), corner_radius=2,
            command=self.redo
        )
        redo_btn.pack(side="left", padx=1)
        
        center_section = ctk.CTkFrame(title_frame, fg_color="transparent")
        center_section.pack(side="left", expand=True, fill="both")
        
        self.doc_title = ctk.CTkLabel(
            center_section, text="Документ1",
            font=("Segoe UI", 11), text_color="#ffffff"
        )
        self.doc_title.pack(expand=True)
        
        right_section = ctk.CTkFrame(title_frame, fg_color="transparent")
        right_section.pack(side="right", fill="y", padx=5)
        
        notes_btn = ctk.CTkButton(
            right_section, text="Примечания", width=90, height=28,
            fg_color="transparent", hover_color="#3f3f3f",
            font=("Segoe UI", 9), corner_radius=2
        )
        notes_btn.pack(side="left", padx=2)
        
        meeting_btn = ctk.CTkButton(
            right_section, text="Встреча", width=70, height=28,
            fg_color="transparent", hover_color="#3f3f3f",
            font=("Segoe UI", 9), corner_radius=2
        )
        meeting_btn.pack(side="left", padx=2)
        
        edit_menu = ctk.CTkButton(
            right_section, text="Редактирование ▼", width=110, height=28,
            fg_color="transparent", hover_color="#3f3f3f",
            font=("Segoe UI", 10), corner_radius=2
        )
        edit_menu.pack(side="left", padx=2)
        
        share_btn = ctk.CTkButton(
            right_section, text="📤", width=28, height=28,
            fg_color="#0078d4", hover_color="#1084d8",
            font=("Segoe UI", 12), corner_radius=2,
            command=self.share_document
        )
        share_btn.pack(side="left", padx=2)
        
    def create_menu_bar(self):
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
        self.menu_buttons[self.active_tab].configure(fg_color="transparent")
        self.active_tab = tab_name
        self.menu_buttons[tab_name].configure(fg_color="#3f3f3f")
        
        if tab_name == "Файл":
            self.show_file_menu()
        
    def show_file_menu(self):
        """Показать меню файла"""
        file_window = ctk.CTkToplevel(self)
        file_window.title("Файл")
        file_window.geometry("300x400")
        file_window.transient(self)
        file_window.grab_set()
        
        title = ctk.CTkLabel(file_window, text="Файл", font=("Segoe UI", 16, "bold"))
        title.pack(pady=20)
        
        ctk.CTkButton(file_window, text="Создать", width=200, height=35,
                     command=lambda: [self.new_file(), file_window.destroy()]).pack(pady=5)
        
        ctk.CTkButton(file_window, text="Открыть", width=200, height=35,
                     command=lambda: [self.open_file(), file_window.destroy()]).pack(pady=5)
        
        ctk.CTkButton(file_window, text="Сохранить", width=200, height=35,
                     command=lambda: [self.save_file(), file_window.destroy()]).pack(pady=5)
        
        ctk.CTkButton(file_window, text="Сохранить как...", width=200, height=35,
                     command=lambda: [self.save_file_as(), file_window.destroy()]).pack(pady=5)
        
        ctk.CTkButton(file_window, text="Печать", width=200, height=35,
                     command=lambda: [self.print_document(), file_window.destroy()]).pack(pady=5)
        
        ctk.CTkButton(file_window, text="Закрыть", width=200, height=35,
                     command=file_window.destroy).pack(pady=20)
        
    def create_ribbon(self):
        self.ribbon_frame = ctk.CTkFrame(self, height=105, fg_color="#2b2b2b", corner_radius=0)
        self.ribbon_frame.pack(fill="x")
        self.ribbon_frame.pack_propagate(False)
        
        main_container = ctk.CTkFrame(self.ribbon_frame, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=6, pady=5)
        
        self.create_clipboard_group(main_container)
        
        sep1 = ctk.CTkFrame(main_container, width=1, fg_color="#404040")
        sep1.pack(side="left", fill="y", padx=6, pady=8)
        
        self.create_font_group(main_container)
        
        sep2 = ctk.CTkFrame(main_container, width=1, fg_color="#404040")
        sep2.pack(side="left", fill="y", padx=6, pady=8)
        
        self.create_paragraph_group(main_container)
        
        sep3 = ctk.CTkFrame(main_container, width=1, fg_color="#404040")
        sep3.pack(side="left", fill="y", padx=6, pady=8)
        
        self.create_styles_group(main_container)
        
        sep4 = ctk.CTkFrame(main_container, width=1, fg_color="#404040")
        sep4.pack(side="left", fill="y", padx=6, pady=8)
        
        self.create_editing_group(main_container)
        
    def create_clipboard_group(self, parent):
        group = ctk.CTkFrame(parent, fg_color="transparent")
        group.pack(side="left", padx=3)
        
        paste_btn = ctk.CTkButton(
            group, text="📋\nВставить", width=45, height=60,
            fg_color="#0078d4", hover_color="#1084d8",
            font=("Segoe UI", 9), corner_radius=2,
            command=self.paste
        )
        paste_btn.pack(side="left", padx=(0, 2))
        
        right_col = ctk.CTkFrame(group, fg_color="transparent")
        right_col.pack(side="left")
        
        cut_btn = ctk.CTkButton(
            right_col, text="✂ Вырезать", width=75, height=18,
            fg_color="transparent", hover_color="#3f3f3f",
            font=("Segoe UI", 8), corner_radius=2,
            anchor="w", command=self.cut
        )
        cut_btn.pack(pady=(0, 1))
        
        copy_btn = ctk.CTkButton(
            right_col, text="📄 Копировать", width=75, height=18,
            fg_color="transparent", hover_color="#3f3f3f",
            font=("Segoe UI", 8), corner_radius=2,
            anchor="w", command=self.copy
        )
        copy_btn.pack(pady=1)
        
        format_btn = ctk.CTkButton(
            right_col, text="🖌 Формат", width=75, height=18,
            fg_color="transparent", hover_color="#3f3f3f",
            font=("Segoe UI", 8), corner_radius=2,
            anchor="w", command=self.format_painter
        )
        format_btn.pack(pady=(1, 0))
        
    def create_font_group(self, parent):
        group = ctk.CTkFrame(parent, fg_color="transparent")
        group.pack(side="left", padx=3)
        
        row1 = ctk.CTkFrame(group, fg_color="transparent", height=26)
        row1.pack(fill="x", pady=(0, 2))
        row1.pack_propagate(False)
        
        self.font_family = ctk.CTkComboBox(
            row1, values=["Arial", "Calibri", "Aptos", "Times New Roman", "Courier New"],
            width=130, height=24, font=("Segoe UI", 9),
            command=self.change_font_family, corner_radius=2,
            border_width=1, border_color="#555555",
            button_color="#0078d4", fg_color="#3a3a3a"
        )
        self.font_family.set("Arial")
        self.font_family.pack(side="left", padx=(0, 2))
        
        self.font_size = ctk.CTkComboBox(
            row1, values=["8", "9", "10", "11", "12", "14", "16", "18", "20", "24", "28", "32", "36"],
            width=50, height=24, font=("Segoe UI", 9),
            command=self.change_font_size, corner_radius=2,
            border_width=1, border_color="#555555",
            button_color="#0078d4", fg_color="#3a3a3a"
        )
        self.font_size.set("12")
        self.font_size.pack(side="left", padx=2)
        
        increase_btn = ctk.CTkButton(
            row1, text="▲", width=24, height=24,
            fg_color="transparent", hover_color="#3f3f3f",
            font=("Segoe UI", 8), corner_radius=2,
            command=self.increase_font
        )
        increase_btn.pack(side="left", padx=1)
        
        decrease_btn = ctk.CTkButton(
            row1, text="▼", width=24, height=24,
            fg_color="transparent", hover_color="#3f3f3f",
            font=("Segoe UI", 8), corner_radius=2,
            command=self.decrease_font
        )
        decrease_btn.pack(side="left", padx=1)
        
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
        
        strike_btn = ctk.CTkButton(
            row2, text="abc", width=24, height=24,
            fg_color="transparent", hover_color="#3f3f3f",
            font=("Segoe UI", 10, "overstrike"), corner_radius=2,
            command=self.toggle_strikethrough
        )
        strike_btn.pack(side="left", padx=1)
        
        sub_btn = ctk.CTkButton(
            row2, text="x₂", width=24, height=24,
            fg_color="transparent", hover_color="#3f3f3f",
            font=("Segoe UI", 10), corner_radius=2
        )
        sub_btn.pack(side="left", padx=1)
        
        sup_btn = ctk.CTkButton(
            row2, text="x²", width=24, height=24,
            fg_color="transparent", hover_color="#3f3f3f",
            font=("Segoe UI", 10), corner_radius=2
        )
        sup_btn.pack(side="left", padx=1)
        
        row3 = ctk.CTkFrame(group, fg_color="transparent", height=26)
        row3.pack(fill="x", pady=(2, 0))
        row3.pack_propagate(False)
        
        case_btn = ctk.CTkButton(
            row3, text="Aa", width=24, height=24,
            fg_color="transparent", hover_color="#3f3f3f",
            font=("Segoe UI", 10), corner_radius=2,
            command=self.change_case
        )
        case_btn.pack(side="left", padx=1)
        
        clear_btn = ctk.CTkButton(
            row3, text="A", width=24, height=24,
            fg_color="transparent", hover_color="#3f3f3f",
            font=("Segoe UI", 10), corner_radius=2,
            command=self.clear_format
        )
        clear_btn.pack(side="left", padx=1)
        
        highlight_btn = ctk.CTkButton(
            row3, text="🖍", width=24, height=24,
            fg_color="transparent", hover_color="#3f3f3f",
            font=("Segoe UI", 10), corner_radius=2,
            command=self.change_bg_color
        )
        highlight_btn.pack(side="left", padx=1)
        
        self.text_color_btn = ctk.CTkButton(
            row3, text="А", width=24, height=24,
            fg_color="#c83232", hover_color="#d84040",
            font=("Segoe UI", 11, "bold"), corner_radius=2,
            command=self.change_text_color
        )
        self.text_color_btn.pack(side="left", padx=1)
        
    def create_paragraph_group(self, parent):
        group = ctk.CTkFrame(parent, fg_color="transparent")
        group.pack(side="left", padx=3)
        
        row1 = ctk.CTkFrame(group, fg_color="transparent", height=26)
        row1.pack(fill="x", pady=(0, 2))
        row1.pack_propagate(False)
        
        bullet_btn = ctk.CTkButton(
            row1, text="• ▼", width=32, height=24,
            fg_color="transparent", hover_color="#3f3f3f",
            font=("Segoe UI", 9), corner_radius=2,
            command=self.insert_bullet
        )
        bullet_btn.pack(side="left", padx=1)
        
        number_btn = ctk.CTkButton(
            row1, text="1. ▼", width=32, height=24,
            fg_color="transparent", hover_color="#3f3f3f",
            font=("Segoe UI", 9), corner_radius=2,
            command=self.insert_numbered
        )
        number_btn.pack(side="left", padx=1)
        
        multi_btn = ctk.CTkButton(
            row1, text="≡ ▼", width=32, height=24,
            fg_color="transparent", hover_color="#3f3f3f",
            font=("Segoe UI", 9), corner_radius=2
        )
        multi_btn.pack(side="left", padx=1)
        
        indent_dec = ctk.CTkButton(
            row1, text="◁", width=24, height=24,
            fg_color="transparent", hover_color="#3f3f3f",
            font=("Segoe UI", 10), corner_radius=2,
            command=self.decrease_indent
        )
        indent_dec.pack(side="left", padx=1)
        
        indent_inc = ctk.CTkButton(
            row1, text="▷", width=24, height=24,
            fg_color="transparent", hover_color="#3f3f3f",
            font=("Segoe UI", 10), corner_radius=2,
            command=self.increase_indent
        )
        indent_inc.pack(side="left", padx=1)
        
        row2 = ctk.CTkFrame(group, fg_color="transparent", height=26)
        row2.pack(fill="x", pady=2)
        row2.pack_propagate(False)
        
        sort_btn = ctk.CTkButton(
            row2, text="AZ", width=24, height=24,
            fg_color="transparent", hover_color="#3f3f3f",
            font=("Segoe UI", 8), corner_radius=2,
            command=self.sort_text
        )
        sort_btn.pack(side="left", padx=1)
        
        symbols_btn = ctk.CTkButton(
            row2, text="¶", width=24, height=24,
            fg_color="transparent", hover_color="#3f3f3f",
            font=("Segoe UI", 12), corner_radius=2,
            command=self.toggle_symbols
        )
        symbols_btn.pack(side="left", padx=1)
        
        align_left = ctk.CTkButton(
            row2, text="≡", width=24, height=24,
            fg_color="transparent", hover_color="#3f3f3f",
            font=("Segoe UI", 10), corner_radius=2,
            command=lambda: self.align_text("left")
        )
        align_left.pack(side="left", padx=1)
        
        align_center = ctk.CTkButton(
            row2, text="≡", width=24, height=24,
            fg_color="transparent", hover_color="#3f3f3f",
            font=("Segoe UI", 10), corner_radius=2,
            command=lambda: self.align_text("center")
        )
        align_center.pack(side="left", padx=1)
        
        align_right = ctk.CTkButton(
            row2, text="≡", width=24, height=24,
            fg_color="transparent", hover_color="#3f3f3f",
            font=("Segoe UI", 10), corner_radius=2,
            command=lambda: self.align_text("right")
        )
        align_right.pack(side="left", padx=1)
        
        align_justify = ctk.CTkButton(
            row2, text="≡", width=24, height=24,
            fg_color="transparent", hover_color="#3f3f3f",
            font=("Segoe UI", 10), corner_radius=2,
            command=lambda: self.align_text("justify")
        )
        align_justify.pack(side="left", padx=1)
        
        row3 = ctk.CTkFrame(group, fg_color="transparent", height=26)
        row3.pack(fill="x", pady=(2, 0))
        row3.pack_propagate(False)
        
        spacing_btn = ctk.CTkButton(
            row3, text="⇅", width=24, height=24,
            fg_color="transparent", hover_color="#3f3f3f",
            font=("Segoe UI", 12), corner_radius=2,
            command=self.change_line_spacing
        )
        spacing_btn.pack(side="left", padx=1)
        
        fill_btn = ctk.CTkButton(
            row3, text="🎨", width=24, height=24,
            fg_color="transparent", hover_color="#3f3f3f",
            font=("Segoe UI", 10), corner_radius=2,
            command=self.change_bg_color
        )
        fill_btn.pack(side="left", padx=1)
        
        border_btn = ctk.CTkButton(
            row3, text="⊞", width=24, height=24,
            fg_color="transparent", hover_color="#3f3f3f",
            font=("Segoe UI", 12), corner_radius=2
        )
        border_btn.pack(side="left", padx=1)
        
    def create_styles_group(self, parent):
        group = ctk.CTkFrame(parent, fg_color="transparent")
        group.pack(side="left", padx=3)
        
        label = ctk.CTkLabel(group, text="Стили", font=("Segoe UI", 8), text_color="#909090")
        label.pack(anchor="w", pady=(0, 2))
        
        styles_row = ctk.CTkFrame(group, fg_color="transparent")
        styles_row.pack()
        
        normal_btn = ctk.CTkButton(
            styles_row, text="Обычный", width=85, height=38,
            fg_color="#0078d4", hover_color="#1084d8",
            font=("Segoe UI", 9), corner_radius=2,
            command=lambda: self.apply_style("normal")
        )
        normal_btn.pack(side="left", padx=2)
        
        no_space_btn = ctk.CTkButton(
            styles_row, text="Без интервала", width=85, height=38,
            fg_color="#0078d4", hover_color="#1084d8",
            font=("Segoe UI", 8), corner_radius=2,
            command=lambda: self.apply_style("no_spacing")
        )
        no_space_btn.pack(side="left", padx=2)
        
        heading_btn = ctk.CTkButton(
            styles_row, text="Заголовок", width=85, height=38,
            fg_color="#0078d4", hover_color="#1084d8",
            font=("Segoe UI", 9, "bold"), corner_radius=2,
            command=lambda: self.apply_style("heading")
        )
        heading_btn.pack(side="left", padx=2)
        
    def create_editing_group(self, parent):
        group = ctk.CTkFrame(parent, fg_color="transparent")
        group.pack(side="left", padx=3)
        
        label = ctk.CTkLabel(group, text="Редактирование", font=("Segoe UI", 8), text_color="#909090")
        label.pack(anchor="w", pady=(0, 2))
        
        find_btn = ctk.CTkButton(
            group, text="🔍 Найти", width=75, height=18,
            fg_color="transparent", hover_color="#3f3f3f",
            font=("Segoe UI", 8), corner_radius=2,
            anchor="w", command=self.find_text
        )
        find_btn.pack(pady=(0, 1))
        
        replace_btn = ctk.CTkButton(
            group, text="🔄 Заменить", width=75, height=18,
            fg_color="transparent", hover_color="#3f3f3f",
            font=("Segoe UI", 8), corner_radius=2,
            anchor="w", command=self.replace_text
        )
        replace_btn.pack(pady=1)
        
        select_btn = ctk.CTkButton(
            group, text="▣ Выделить", width=75, height=18,
            fg_color="transparent", hover_color="#3f3f3f",
            font=("Segoe UI", 8), corner_radius=2,
            anchor="w", command=self.select_all
        )
        select_btn.pack(pady=(1, 0))
        
    def create_text_area(self):
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
        
        view_btn1 = ctk.CTkButton(
            right_status, text="📖", width=24, height=20,
            fg_color="transparent", hover_color="#3f3f3f",
            font=("Segoe UI", 10), corner_radius=2
        )
        view_btn1.pack(side="left", padx=1)
        
        view_btn2 = ctk.CTkButton(
            right_status, text="📄", width=24, height=20,
            fg_color="#0078d4", hover_color="#1084d8",
            font=("Segoe UI", 10), corner_radius=2
        )
        view_btn2.pack(side="left", padx=1)
        
        view_btn3 = ctk.CTkButton(
            right_status, text="🌐", width=24, height=20,
            fg_color="transparent", hover_color="#3f3f3f",
            font=("Segoe UI", 10), corner_radius=2
        )
        view_btn3.pack(side="left", padx=1)
        
        zoom_minus = ctk.CTkButton(
            right_status, text="-", width=24, height=20,
            fg_color="transparent", hover_color="#3f3f3f",
            font=("Segoe UI", 12), corner_radius=2,
            command=self.zoom_out
        )
        zoom_minus.pack(side="left", padx=(10, 2))
        
        self.zoom_slider = ctk.CTkSlider(
            right_status, from_=50, to=200, width=100, height=16,
            command=self.zoom_change
        )
        self.zoom_slider.set(100)
        self.zoom_slider.pack(side="left", padx=2)
        
        zoom_plus = ctk.CTkButton(
            right_status, text="+", width=24, height=20,
            fg_color="transparent", hover_color="#3f3f3f",
            font=("Segoe UI", 12), corner_radius=2,
            command=self.zoom_in
        )
        zoom_plus.pack(side="left", padx=2)
        
        self.zoom_label = ctk.CTkLabel(
            right_status, text="100%", width=40,
            font=("Segoe UI", 9), text_color="#909090"
        )
        self.zoom_label.pack(side="left", padx=2)
        
        fit_btn = ctk.CTkButton(
            right_status, text="⬌", width=30, height=20,
            fg_color="transparent", hover_color="#3f3f3f",
            font=("Segoe UI", 10), corner_radius=2
        )
        fit_btn.pack(side="left", padx=2)
        
        self.text_area.bind("<KeyRelease>", self.update_status)
        
    def bind_shortcuts(self):
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
        
    # === ФУНКЦИИ БУФЕРА ОБМЕНА ===
    
    def cut(self):
        try:
            self.text_area.event_generate("<<Cut>>")
        except:
            pass
    
    def copy(self):
        try:
            self.text_area.event_generate("<<Copy>>")
        except:
            pass
    
    def paste(self):
        try:
            self.text_area.event_generate("<<Paste>>")
        except:
            pass
    
    def undo(self):
        try:
            self.text_area.edit_undo()
        except:
            pass
    
    def redo(self):
        try:
            self.text_area.edit_redo()
        except:
            pass
    
    def format_painter(self):
        """Копировать формат"""
        try:
            if self.text_area.tag_ranges("sel"):
                tags = self.text_area.tag_names("sel.first")
                self.copied_format = [tag for tag in tags if tag not in ("sel",)]
                messagebox.showinfo("Формат по образцу", "Формат скопирован! Выделите текст для применения.")
        except:
            pass
    
    # === ФУНКЦИИ ФОРМАТИРОВАНИЯ ===
    
    def get_current_font(self):
        """Получить текущий стиль шрифта"""
        style = []
        if self.is_bold:
            style.append("bold")
        if self.is_italic:
            style.append("italic")
        return " ".join(style) if style else "normal"
    
    def update_text_font(self):
        """Обновить шрифт в текстовой области"""
        font_style = self.get_current_font()
        self.text_area.configure(font=(self.current_font_family, self.current_font_size, font_style))
    
    def change_font_family(self, choice):
        self.current_font_family = choice
        try:
            if self.text_area.tag_ranges("sel"):
                tag_name = f"font_{choice}"
                self.text_area.tag_add(tag_name, "sel.first", "sel.last")
                self.text_area.tag_configure(tag_name, font=(choice, self.current_font_size))
            else:
                self.update_text_font()
        except:
            self.update_text_font()
            
    def change_font_size(self, choice):
        try:
            size = int(choice)
            self.current_font_size = size
            if self.text_area.tag_ranges("sel"):
                tag_name = f"size_{size}"
                self.text_area.tag_add(tag_name, "sel.first", "sel.last")
                self.text_area.tag_configure(tag_name, font=(self.current_font_family, size))
            else:
                self.update_text_font()
        except:
            pass
    
    def increase_font(self):
        try:
            current_size = int(self.font_size.get())
            new_size = min(current_size + 2, 72)
            self.font_size.set(str(new_size))
            self.change_font_size(str(new_size))
        except:
            pass
    
    def decrease_font(self):
        try:
            current_size = int(self.font_size.get())
            new_size = max(current_size - 2, 8)
            self.font_size.set(str(new_size))
            self.change_font_size(str(new_size))
        except:
            pass
            
    def toggle_bold(self):
        self.is_bold = not self.is_bold
        self.bold_btn.configure(fg_color="#0078d4" if self.is_bold else "transparent")
        
        try:
            if self.text_area.tag_ranges("sel"):
                if self.is_bold:
                    self.text_area.tag_add("bold", "sel.first", "sel.last")
                    self.text_area.tag_configure("bold", font=(self.current_font_family, self.current_font_size, "bold"))
                else:
                    self.text_area.tag_remove("bold", "sel.first", "sel.last")
            else:
                self.update_text_font()
        except:
            self.update_text_font()
            
    def toggle_italic(self):
        self.is_italic = not self.is_italic
        self.italic_btn.configure(fg_color="#0078d4" if self.is_italic else "transparent")
        
        try:
            if self.text_area.tag_ranges("sel"):
                if self.is_italic:
                    self.text_area.tag_add("italic", "sel.first", "sel.last")
                    self.text_area.tag_configure("italic", font=(self.current_font_family, self.current_font_size, "italic"))
                else:
                    self.text_area.tag_remove("italic", "sel.first", "sel.last")
            else:
                self.update_text_font()
        except:
            self.update_text_font()
            
    def toggle_underline(self):
        self.is_underline = not self.is_underline
        self.underline_btn.configure(fg_color="#0078d4" if self.is_underline else "transparent")
        
        try:
            if self.text_area.tag_ranges("sel"):
                if self.is_underline:
                    self.text_area.tag_add("underline", "sel.first", "sel.last")
                    self.text_area.tag_configure("underline", underline=True)
                else:
                    self.text_area.tag_remove("underline", "sel.first", "sel.last")
        except:
            pass
            
    def toggle_strikethrough(self):
        try:
            if self.text_area.tag_ranges("sel"):
                current_tags = self.text_area.tag_names("sel.first")
                if "strikethrough" in current_tags:
                    self.text_area.tag_remove("strikethrough", "sel.first", "sel.last")
                else:
                    self.text_area.tag_add("strikethrough", "sel.first", "sel.last")
                    self.text_area.tag_configure("strikethrough", overstrike=True)
        except:
            pass
            
    def change_text_color(self):
        color = colorchooser.askcolor(title="Выберите цвет текста")
        if color[1]:
            try:
                if self.text_area.tag_ranges("sel"):
                    self.text_area.tag_add("color", "sel.first", "sel.last")
                    self.text_area.tag_configure("color", foreground=color[1])
                    self.text_color_btn.configure(fg_color=color[1])
            except:
                pass
                
    def change_bg_color(self):
        color = colorchooser.askcolor(title="Выберите цвет выделения")
        if color[1]:
            try:
                if self.text_area.tag_ranges("sel"):
                    self.text_area.tag_add("bgcolor", "sel.first", "sel.last")
                    self.text_area.tag_configure("bgcolor", background=color[1])
            except:
                pass
    
    def clear_format(self):
        """Очистить форматирование"""
        try:
            if self.text_area.tag_ranges("sel"):
                for tag in self.text_area.tag_names("sel.first"):
                    if tag != "sel":
                        self.text_area.tag_remove(tag, "sel.first", "sel.last")
        except:
            pass
    
    def change_case(self):
        """Изменить регистр"""
        try:
            if self.text_area.tag_ranges("sel"):
                text = self.text_area.get("sel.first", "sel.last")
                if text.isupper():
                    new_text = text.lower()
                elif text.islower():
                    new_text = text.title()
                else:
                    new_text = text.upper()
                self.text_area.delete("sel.first", "sel.last")
                self.text_area.insert("sel.first", new_text)
        except:
            pass
    
    # === ФУНКЦИИ АБЗАЦА ===
                
    def align_text(self, alignment):
        try:
            current_line = self.text_area.index("insert linestart")
            end_line = self.text_area.index("insert lineend")
            tag_name = f"align_{alignment}"
            self.text_area.tag_add(tag_name, current_line, end_line)
            self.text_area.tag_configure(tag_name, justify=alignment)
        except:
            pass
            
    def insert_bullet(self):
        self.text_area.insert("insert", "• ")
        
    def insert_numbered(self):
        self.text_area.insert("insert", "1. ")
    
    def increase_indent(self):
        """Увеличить отступ"""
        try:
            current_line = self.text_area.index("insert linestart")
            self.text_area.insert(current_line, "    ")
        except:
            pass
    
    def decrease_indent(self):
        """Уменьшить отступ"""
        try:
            current_line = self.text_area.index("insert linestart")
            line_text = self.text_area.get(current_line, "insert lineend")
            if line_text.startswith("    "):
                self.text_area.delete(current_line, f"{current_line}+4c")
        except:
            pass
    
    def toggle_symbols(self):
        """Показать/скрыть непечатаемые символы"""
        messagebox.showinfo("Непечатаемые символы", "Функция отображения непечатаемых символов")
    
    def sort_text(self):
        """Сортировать текст"""
        try:
            if self.text_area.tag_ranges("sel"):
                text = self.text_area.get("sel.first", "sel.last")
                lines = text.split("\n")
                sorted_lines = sorted(lines)
                self.text_area.delete("sel.first", "sel.last")
                self.text_area.insert("sel.first", "\n".join(sorted_lines))
        except:
            pass
    
    def change_line_spacing(self):
        """Изменить междустрочный интервал"""
        spacing_window = ctk.CTkToplevel(self)
        spacing_window.title("Междустрочный интервал")
        spacing_window.geometry("250x200")
        spacing_window.transient(self)
        spacing_window.grab_set()
        
        ctk.CTkLabel(spacing_window, text="Выберите интервал:", font=("Segoe UI", 11)).pack(pady=10)
        
        def set_spacing(value):
            self.text_area.configure(spacing1=value, spacing3=value)
            spacing_window.destroy()
        
        ctk.CTkButton(spacing_window, text="1.0", width=150, command=lambda: set_spacing(0)).pack(pady=5)
        ctk.CTkButton(spacing_window, text="1.15", width=150, command=lambda: set_spacing(2)).pack(pady=5)
        ctk.CTkButton(spacing_window, text="1.5", width=150, command=lambda: set_spacing(5)).pack(pady=5)
        ctk.CTkButton(spacing_window, text="2.0", width=150, command=lambda: set_spacing(10)).pack(pady=5)
    
    # === ФУНКЦИИ СТИЛЕЙ ===
        
    def apply_style(self, style):
        try:
            start = "sel.first" if self.text_area.tag_ranges("sel") else "insert linestart"
            end = "sel.last" if self.text_area.tag_ranges("sel") else "insert lineend"
            
            if style == "normal":
                self.text_area.tag_add("normal", start, end)
                self.text_area.tag_configure("normal", font=("Arial", 12), spacing1=3, spacing3=3)
            elif style == "no_spacing":
                self.text_area.tag_add("no_spacing", start, end)
                self.text_area.tag_configure("no_spacing", font=("Arial", 12), spacing1=0, spacing3=0)
            elif style == "heading":
                self.text_area.tag_add("heading", start, end)
                self.text_area.tag_configure("heading", font=("Arial", 18, "bold"), spacing1=5, spacing3=5)
        except:
            pass
    
    # === ФУНКЦИИ РЕДАКТИРОВАНИЯ ===
    
    def find_text(self):
        """Диалог поиска"""
        search_window = ctk.CTkToplevel(self)
        search_window.title("Найти")
        search_window.geometry("400x150")
        search_window.transient(self)
        search_window.grab_set()
        
        ctk.CTkLabel(search_window, text="Найти:", font=("Segoe UI", 11)).pack(pady=(15, 5), padx=15, anchor="w")
        
        search_entry = ctk.CTkEntry(search_window, width=360, height=35, font=("Segoe UI", 11))
        search_entry.pack(pady=5, padx=15)
        search_entry.focus()
        
        button_frame = ctk.CTkFrame(search_window, fg_color="transparent")
        button_frame.pack(pady=10)
        
        def do_search():
            query = search_entry.get()
            if query:
                self.text_area.tag_remove("search", "1.0", "end")
                start_pos = "1.0"
                count = 0
                while True:
                    start_pos = self.text_area.search(query, start_pos, stopindex="end", nocase=True)
                    if not start_pos:
                        break
                    end_pos = f"{start_pos}+{len(query)}c"
                    self.text_area.tag_add("search", start_pos, end_pos)
                    count += 1
                    start_pos = end_pos
                self.text_area.tag_configure("search", background="#ffff00", foreground="#000000")
                messagebox.showinfo("Результат", f"Найдено совпадений: {count}")
        
        ctk.CTkButton(
            button_frame, text="Найти далее", width=120,
            command=do_search, fg_color="#0078d4", hover_color="#1084d8"
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            button_frame, text="Закрыть", width=120,
            command=search_window.destroy
        ).pack(side="left", padx=5)
    
    def replace_text(self):
        """Диалог замены"""
        replace_window = ctk.CTkToplevel(self)
        replace_window.title("Заменить")
        replace_window.geometry("400x220")
        replace_window.transient(self)
        replace_window.grab_set()
        
        ctk.CTkLabel(replace_window, text="Найти:", font=("Segoe UI", 11)).pack(pady=(15, 5), padx=15, anchor="w")
        find_entry = ctk.CTkEntry(replace_window, width=360, height=35, font=("Segoe UI", 11))
        find_entry.pack(pady=5, padx=15)
        
        ctk.CTkLabel(replace_window, text="Заменить на:", font=("Segoe UI", 11)).pack(pady=(10, 5), padx=15, anchor="w")
        replace_entry = ctk.CTkEntry(replace_window, width=360, height=35, font=("Segoe UI", 11))
        replace_entry.pack(pady=5, padx=15)
        
        button_frame = ctk.CTkFrame(replace_window, fg_color="transparent")
        button_frame.pack(pady=15)
        
        def do_replace_all():
            find_text = find_entry.get()
            replace_text = replace_entry.get()
            if find_text:
                content = self.text_area.get("1.0", "end-1c")
                new_content = content.replace(find_text, replace_text)
                self.text_area.delete("1.0", "end")
                self.text_area.insert("1.0", new_content)
                messagebox.showinfo("Готово", "Замена выполнена")
        
        ctk.CTkButton(
            button_frame, text="Заменить все", width=120,
            command=do_replace_all, fg_color="#0078d4", hover_color="#1084d8"
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            button_frame, text="Закрыть", width=120,
            command=replace_window.destroy
        ).pack(side="left", padx=5)
    
    def select_all(self):
        """Выделить весь текст"""
        self.text_area.tag_add("sel", "1.0", "end")
        return "break"
    
    # === ФУНКЦИИ МАСШТАБА ===
    
    def zoom_in(self):
        self.zoom_level = min(self.zoom_level + 10, 200)
        self.zoom_slider.set(self.zoom_level)
        self.update_zoom()
    
    def zoom_out(self):
        self.zoom_level = max(self.zoom_level - 10, 50)
        self.zoom_slider.set(self.zoom_level)
        self.update_zoom()
    
    def zoom_change(self, value):
        self.zoom_level = int(value)
        self.update_zoom()
    
    def update_zoom(self):
        new_size = int(self.current_font_size * self.zoom_level / 100)
        font_style = self.get_current_font()
        self.text_area.configure(font=(self.current_font_family, new_size, font_style))
        self.zoom_label.configure(text=f"{self.zoom_level}%")
    
    # === ФУНКЦИИ СТАТУСА ===
            
    def update_status(self, event=None):
        content = self.text_area.get(1.0, "end-1c")
        words = len(content.split()) if content.strip() else 0
        chars = len(content)
        lines = content.count("\n") + 1
        self.page_label.configure(text=f"Страница 1 из 1    Число слов: {words}    Русский")
    
    # === ФУНКЦИИ РАБОТЫ С ФАЙЛАМИ ===
        
    def new_file(self):
        if messagebox.askyesno("Новый документ", "Создать новый документ? Несохраненные изменения будут потеряны."):
            self.text_area.delete(1.0, "end")
            self.current_file = None
            self.doc_title.configure(text="Документ1")
            self.update_status()
        
    def open_file(self):
        file_path = filedialog.askopenfilename(
            defaultextension=".txt",
            filetypes=[
                ("Текстовые файлы", "*.txt"),
                ("Документы Word", "*.docx"),
                ("Все файлы", "*.*")
            ]
        )
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    self.text_area.delete(1.0, "end")
                    self.text_area.insert(1.0, file.read())
                self.current_file = file_path
                import os
                self.doc_title.configure(text=os.path.basename(file_path))
                self.update_status()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось открыть файл:\n{str(e)}")
            
    def save_file(self):
        if self.current_file:
            try:
                with open(self.current_file, "w", encoding="utf-8") as file:
                    file.write(self.text_area.get(1.0, "end-1c"))
                messagebox.showinfo("Сохранено", "Файл успешно сохранен")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось сохранить файл:\n{str(e)}")
        else:
            self.save_file_as()
            
    def save_file_as(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[
                ("Текстовые файлы", "*.txt"),
                ("Все файлы", "*.*")
            ]
        )
        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(self.text_area.get(1.0, "end-1c"))
                self.current_file = file_path
                import os
                self.doc_title.configure(text=os.path.basename(file_path))
                messagebox.showinfo("Сохранено", "Файл успешно сохранен")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось сохранить файл:\n{str(e)}")
    
    def print_document(self):
        """Печать документа"""
        messagebox.showinfo("Печать", "Функция печати будет доступна в следующей версии")
    
    def share_document(self):
        """Поделиться документом"""
        share_window = ctk.CTkToplevel(self)
        share_window.title("Поделиться")
        share_window.geometry("350x200")
        share_window.transient(self)
        share_window.grab_set()
        
        ctk.CTkLabel(share_window, text="Поделиться документом", 
                    font=("Segoe UI", 14, "bold")).pack(pady=20)
        
        ctk.CTkLabel(share_window, text="Введите email для отправки:",
                    font=("Segoe UI", 11)).pack(pady=10)
        
        email_entry = ctk.CTkEntry(share_window, width=300, height=35)
        email_entry.pack(pady=10)
        
        def send():
            email = email_entry.get()
            if email:
                messagebox.showinfo("Успешно", f"Документ отправлен на {email}")
                share_window.destroy()
        
        ctk.CTkButton(share_window, text="Отправить", width=150,
                     command=send, fg_color="#0078d4", hover_color="#1084d8").pack(pady=10)

if __name__ == "__main__":
    app = WordClone()
    app.mainloop()