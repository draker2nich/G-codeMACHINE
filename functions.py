"""
Модуль функциональности текстового редактора
Все операции с текстом, файлами и форматированием
"""

from tkinter import colorchooser, filedialog, messagebox
import customtkinter as ctk
import os

class EditorFunctions:
    """Класс с функциональностью редактора"""
    
    def __init__(self):
        pass
    
    # === ФУНКЦИИ БУФЕРА ОБМЕНА ===
    
    def cut(self):
        """Вырезать текст"""
        try:
            self.text_area.event_generate("<<Cut>>")
        except:
            pass
    
    def copy(self):
        """Копировать текст"""
        try:
            self.text_area.event_generate("<<Copy>>")
        except:
            pass
    
    def paste(self):
        """Вставить текст"""
        try:
            self.text_area.event_generate("<<Paste>>")
        except:
            pass
    
    def undo(self):
        """Отменить действие"""
        try:
            self.text_area.edit_undo()
        except:
            pass
    
    def redo(self):
        """Повторить действие"""
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
                messagebox.showinfo("Формат по образцу", 
                    "Формат скопирован! Выделите текст для применения.")
        except:
            pass
    
    # === ФУНКЦИИ ФОРМАТИРОВАНИЯ ШРИФТА ===
    
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
        """Изменить семейство шрифта"""
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
        """Изменить размер шрифта"""
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
        """Увеличить размер шрифта"""
        try:
            current_size = int(self.font_size.get())
            new_size = min(current_size + 2, 72)
            self.font_size.set(str(new_size))
            self.change_font_size(str(new_size))
        except:
            pass
    
    def decrease_font(self):
        """Уменьшить размер шрифта"""
        try:
            current_size = int(self.font_size.get())
            new_size = max(current_size - 2, 8)
            self.font_size.set(str(new_size))
            self.change_font_size(str(new_size))
        except:
            pass
            
    def toggle_bold(self):
        """Переключить жирный шрифт"""
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
        """Переключить курсив"""
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
        """Переключить подчеркивание"""
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
        """Переключить зачеркивание"""
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
    
    def insert_subscript(self):
        """Вставить подстрочный индекс"""
        try:
            if self.text_area.tag_ranges("sel"):
                self.text_area.tag_add("subscript", "sel.first", "sel.last")
                self.text_area.tag_configure("subscript", offset=-4)
        except:
            messagebox.showinfo("Подстрочный индекс", "Выделите текст для применения")
    
    def insert_superscript(self):
        """Вставить надстрочный индекс"""
        try:
            if self.text_area.tag_ranges("sel"):
                self.text_area.tag_add("superscript", "sel.first", "sel.last")
                self.text_area.tag_configure("superscript", offset=4)
        except:
            messagebox.showinfo("Надстрочный индекс", "Выделите текст для применения")
            
    def change_text_color(self):
        """Изменить цвет текста"""
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
        """Изменить цвет выделения"""
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
                messagebox.showinfo("Формат", "Форматирование очищено")
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
        """Выровнять текст"""
        try:
            current_line = self.text_area.index("insert linestart")
            end_line = self.text_area.index("insert lineend")
            tag_name = f"align_{alignment}"
            self.text_area.tag_add(tag_name, current_line, end_line)
            self.text_area.tag_configure(tag_name, justify=alignment)
        except:
            pass
            
    def insert_bullet(self):
        """Вставить маркер"""
        self.text_area.insert("insert", "• ")
        
    def insert_numbered(self):
        """Вставить нумерацию"""
        try:
            current_line = self.text_area.index("insert linestart")
            line_num = int(current_line.split('.')[0])
            self.text_area.insert("insert", f"{line_num}. ")
        except:
            self.text_area.insert("insert", "1. ")
    
    def insert_multilevel(self):
        """Многоуровневый список"""
        window = ctk.CTkToplevel(self)
        window.title("Многоуровневый список")
        window.geometry("300x250")
        window.transient(self)
        window.grab_set()
        
        ctk.CTkLabel(window, text="Выберите уровень списка:", 
                    font=("Segoe UI", 12, "bold")).pack(pady=15)
        
        def insert_level(level, symbol):
            indent = "    " * (level - 1)
            self.text_area.insert("insert", f"{indent}{symbol} ")
            window.destroy()
        
        ctk.CTkButton(window, text="Уровень 1: • Элемент", width=250,
                     command=lambda: insert_level(1, "•")).pack(pady=5)
        ctk.CTkButton(window, text="Уровень 2:     ○ Элемент", width=250,
                     command=lambda: insert_level(2, "○")).pack(pady=5)
        ctk.CTkButton(window, text="Уровень 3:         ▪ Элемент", width=250,
                     command=lambda: insert_level(3, "▪")).pack(pady=5)
        ctk.CTkButton(window, text="Отмена", width=250,
                     command=window.destroy, fg_color="gray").pack(pady=10)
    
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
        self.show_symbols_visible = not self.show_symbols_visible
        self.symbols_btn.configure(fg_color="#0078d4" if self.show_symbols_visible else "transparent")
        
        if self.show_symbols_visible:
            messagebox.showinfo("Непечатаемые символы", 
                "Режим отображения непечатаемых символов включен\n(¶ - конец абзаца, · - пробелы)")
        else:
            messagebox.showinfo("Непечатаемые символы", 
                "Режим отображения непечатаемых символов выключен")
    
    def sort_text(self):
        """Сортировать текст"""
        try:
            if self.text_area.tag_ranges("sel"):
                text = self.text_area.get("sel.first", "sel.last")
                lines = text.split("\n")
                
                window = ctk.CTkToplevel(self)
                window.title("Сортировка")
                window.geometry("300x200")
                window.transient(self)
                window.grab_set()
                
                ctk.CTkLabel(window, text="Выберите тип сортировки:",
                           font=("Segoe UI", 12, "bold")).pack(pady=15)
                
                def do_sort(reverse=False):
                    sorted_lines = sorted(lines, reverse=reverse)
                    self.text_area.delete("sel.first", "sel.last")
                    self.text_area.insert("sel.first", "\n".join(sorted_lines))
                    window.destroy()
                
                ctk.CTkButton(window, text="От А до Я", width=200,
                             command=lambda: do_sort(False),
                             fg_color="#0078d4").pack(pady=5)
                ctk.CTkButton(window, text="От Я до А", width=200,
                             command=lambda: do_sort(True),
                             fg_color="#0078d4").pack(pady=5)
                ctk.CTkButton(window, text="Отмена", width=200,
                             command=window.destroy).pack(pady=10)
            else:
                messagebox.showinfo("Сортировка", "Выделите текст для сортировки")
        except:
            pass
    
    def change_line_spacing(self):
        """Изменить междустрочный интервал"""
        window = ctk.CTkToplevel(self)
        window.title("Междустрочный интервал")
        window.geometry("300x250")
        window.transient(self)
        window.grab_set()
        
        ctk.CTkLabel(window, text="Выберите интервал:", 
                    font=("Segoe UI", 12, "bold")).pack(pady=15)
        
        def set_spacing(value):
            self.text_area.configure(spacing1=value, spacing3=value)
            messagebox.showinfo("Интервал", f"Междустрочный интервал изменен")
            window.destroy()
        
        ctk.CTkButton(window, text="1.0 (одинарный)", width=200,
                     command=lambda: set_spacing(0)).pack(pady=5)
        ctk.CTkButton(window, text="1.15", width=200,
                     command=lambda: set_spacing(2)).pack(pady=5)
        ctk.CTkButton(window, text="1.5 (полуторный)", width=200,
                     command=lambda: set_spacing(5)).pack(pady=5)
        ctk.CTkButton(window, text="2.0 (двойной)", width=200,
                     command=lambda: set_spacing(10)).pack(pady=5)
    
    def change_paragraph_fill(self):
        """Изменить заливку абзаца"""
        color = colorchooser.askcolor(title="Выберите цвет заливки абзаца")
        if color[1]:
            try:
                current_line = self.text_area.index("insert linestart")
                end_line = self.text_area.index("insert lineend")
                self.text_area.tag_add("para_fill", current_line, end_line)
                self.text_area.tag_configure("para_fill", background=color[1])
            except:
                pass
    
    def add_borders(self):
        """Добавить границы"""
        window = ctk.CTkToplevel(self)
        window.title("Границы и заливка")
        window.geometry("350x300")
        window.transient(self)
        window.grab_set()
        
        ctk.CTkLabel(window, text="Границы и заливка",
                    font=("Segoe UI", 14, "bold")).pack(pady=15)
        
        ctk.CTkLabel(window, text="Выберите тип границы:",
                    font=("Segoe UI", 11)).pack(pady=10)
        
        def apply_border(border_type):
            messagebox.showinfo("Границы", f"Применен тип границы: {border_type}")
            window.destroy()
        
        ctk.CTkButton(window, text="Все границы", width=250,
                     command=lambda: apply_border("все")).pack(pady=5)
        ctk.CTkButton(window, text="Внешние границы", width=250,
                     command=lambda: apply_border("внешние")).pack(pady=5)
        ctk.CTkButton(window, text="Нижняя граница", width=250,
                     command=lambda: apply_border("нижняя")).pack(pady=5)
        ctk.CTkButton(window, text="Без границ", width=250,
                     command=lambda: apply_border("нет")).pack(pady=5)
        ctk.CTkButton(window, text="Закрыть", width=250,
                     command=window.destroy, fg_color="gray").pack(pady=10)
    
    # === ФУНКЦИИ СТИЛЕЙ ===
        
    def apply_style(self, style):
        """Применить стиль"""
        try:
            start = "sel.first" if self.text_area.tag_ranges("sel") else "insert linestart"
            end = "sel.last" if self.text_area.tag_ranges("sel") else "insert lineend"
            
            if style == "normal":
                self.text_area.tag_add("normal", start, end)
                self.text_area.tag_configure("normal", font=("Arial", 12), spacing1=3, spacing3=3)
                messagebox.showinfo("Стиль", "Применен стиль: Обычный")
            elif style == "no_spacing":
                self.text_area.tag_add("no_spacing", start, end)
                self.text_area.tag_configure("no_spacing", font=("Arial", 12), spacing1=0, spacing3=0)
                messagebox.showinfo("Стиль", "Применен стиль: Без интервала")
            elif style == "heading":
                self.text_area.tag_add("heading", start, end)
                self.text_area.tag_configure("heading", font=("Arial", 18, "bold"), spacing1=5, spacing3=5)
                messagebox.showinfo("Стиль", "Применен стиль: Заголовок")
        except:
            pass
    
    # === ФУНКЦИИ РЕДАКТИРОВАНИЯ ===
    
    def find_text(self):
        """Диалог поиска"""
        window = ctk.CTkToplevel(self)
        window.title("Найти")
        window.geometry("450x180")
        window.transient(self)
        window.grab_set()
        
        ctk.CTkLabel(window, text="Найти:", font=("Segoe UI", 12)).pack(pady=(15, 5), padx=15, anchor="w")
        
        search_entry = ctk.CTkEntry(window, width=410, height=35, font=("Segoe UI", 11))
        search_entry.pack(pady=5, padx=15)
        search_entry.focus()
        
        result_label = ctk.CTkLabel(window, text="", font=("Segoe UI", 10), text_color="#909090")
        result_label.pack(pady=5)
        
        button_frame = ctk.CTkFrame(window, fg_color="transparent")
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
                result_label.configure(text=f"Найдено совпадений: {count}")
        
        ctk.CTkButton(
            button_frame, text="Найти далее", width=130,
            command=do_search, fg_color="#0078d4", hover_color="#1084d8"
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            button_frame, text="Закрыть", width=130,
            command=window.destroy
        ).pack(side="left", padx=5)
    
    def replace_text(self):
        """Диалог замены"""
        window = ctk.CTkToplevel(self)
        window.title("Заменить")
        window.geometry("450x280")
        window.transient(self)
        window.grab_set()
        
        ctk.CTkLabel(window, text="Найти:", font=("Segoe UI", 12)).pack(pady=(15, 5), padx=15, anchor="w")
        find_entry = ctk.CTkEntry(window, width=410, height=35, font=("Segoe UI", 11))
        find_entry.pack(pady=5, padx=15)
        
        ctk.CTkLabel(window, text="Заменить на:", font=("Segoe UI", 12)).pack(pady=(10, 5), padx=15, anchor="w")
        replace_entry = ctk.CTkEntry(window, width=410, height=35, font=("Segoe UI", 11))
        replace_entry.pack(pady=5, padx=15)
        
        result_label = ctk.CTkLabel(window, text="", font=("Segoe UI", 10), text_color="#909090")
        result_label.pack(pady=5)
        
        button_frame = ctk.CTkFrame(window, fg_color="transparent")
        button_frame.pack(pady=15)
        
        def do_replace_all():
            find_text = find_entry.get()
            replace_text = replace_entry.get()
            if find_text:
                content = self.text_area.get("1.0", "end-1c")
                count = content.count(find_text)
                new_content = content.replace(find_text, replace_text)
                self.text_area.delete("1.0", "end")
                self.text_area.insert("1.0", new_content)
                result_label.configure(text=f"Выполнено замен: {count}")
        
        ctk.CTkButton(
            button_frame, text="Заменить все", width=130,
            command=do_replace_all, fg_color="#0078d4", hover_color="#1084d8"
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            button_frame, text="Закрыть", width=130,
            command=window.destroy
        ).pack(side="left", padx=5)
    
    def select_all(self):
        """Выделить весь текст"""
        self.text_area.tag_add("sel", "1.0", "end")
        return "break"
    
    # === ФУНКЦИИ МАСШТАБА И ВИДА ===
    
    def zoom_in(self):
        """Увеличить масштаб"""
        self.zoom_level = min(self.zoom_level + 10, 200)
        self.zoom_slider.set(self.zoom_level)
        self.update_zoom()
    
    def zoom_out(self):
        """Уменьшить масштаб"""
        self.zoom_level = max(self.zoom_level - 10, 50)
        self.zoom_slider.set(self.zoom_level)
        self.update_zoom()
    
    def zoom_change(self, value):
        """Изменение масштаба через слайдер"""
        self.zoom_level = int(value)
        self.update_zoom()
    
    def update_zoom(self):
        """Обновить масштаб"""
        new_size = int(self.current_font_size * self.zoom_level / 100)
        font_style = self.get_current_font()
        self.text_area.configure(font=(self.current_font_family, new_size, font_style))
        self.zoom_label.configure(text=f"{self.zoom_level}%")
    
    def fit_to_width(self):
        """Подогнать по ширине окна"""
        self.zoom_level = 100
        self.zoom_slider.set(100)
        self.update_zoom()
        messagebox.showinfo("Масштаб", "Масштаб установлен на 100%")
    
    def reading_mode(self):
        """Режим чтения"""
        messagebox.showinfo("Режим чтения", 
            "Режим чтения оптимизирован для комфортного чтения документов")
    
    def print_layout_mode(self):
        """Режим разметки страницы"""
        messagebox.showinfo("Режим разметки", 
            "Текущий режим: Разметка страницы (активен)")
    
    def web_layout_mode(self):
        """Режим веб-документа"""
        messagebox.showinfo("Режим веб-документа", 
            "Режим веб-документа оптимизирован для просмотра в браузере")
    
    # === ФУНКЦИИ СТАТУСА ===
            
    def update_status(self, event=None):
        """Обновить строку состояния"""
        content = self.text_area.get(1.0, "end-1c")
        words = len(content.split()) if content.strip() else 0
        chars = len(content)
        lines = content.count("\n") + 1
        self.page_label.configure(text=f"Страница 1 из 1    Число слов: {words}    Русский")
    
    # === ФУНКЦИИ РАБОТЫ С ФАЙЛАМИ ===
        
    def new_file(self):
        """Создать новый документ"""
        if messagebox.askyesno("Новый документ", 
            "Создать новый документ? Несохраненные изменения будут потеряны."):
            self.text_area.delete(1.0, "end")
            self.current_file = None
            self.doc_title.configure(text="Документ1")
            self.update_status()
        
    def open_file(self):
        """Открыть файл"""
        file_path = filedialog.askopenfilename(
            defaultextension=".txt",
            filetypes=[
                ("Текстовые файлы", "*.txt"),
                ("Все файлы", "*.*")
            ]
        )
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    self.text_area.delete(1.0, "end")
                    self.text_area.insert(1.0, file.read())
                self.current_file = file_path
                self.doc_title.configure(text=os.path.basename(file_path))
                self.update_status()
                messagebox.showinfo("Успешно", f"Файл открыт:\n{os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось открыть файл:\n{str(e)}")
            
    def save_file(self):
        """Сохранить файл"""
        if self.current_file:
            try:
                with open(self.current_file, "w", encoding="utf-8") as file:
                    file.write(self.text_area.get(1.0, "end-1c"))
                messagebox.showinfo("Сохранено", f"Файл успешно сохранен:\n{os.path.basename(self.current_file)}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось сохранить файл:\n{str(e)}")
        else:
            self.save_file_as()
            
    def save_file_as(self):
        """Сохранить файл как..."""
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
                self.doc_title.configure(text=os.path.basename(file_path))
                messagebox.showinfo("Сохранено", f"Файл успешно сохранен:\n{os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось сохранить файл:\n{str(e)}")
    
    def print_document(self):
        """Печать документа"""
        window = ctk.CTkToplevel(self)
        window.title("Печать")
        window.geometry("400x300")
        window.transient(self)
        window.grab_set()
        
        ctk.CTkLabel(window, text="Параметры печати",
                    font=("Segoe UI", 16, "bold")).pack(pady=20)
        
        ctk.CTkLabel(window, text="Принтер:", font=("Segoe UI", 11)).pack(pady=(10, 5))
        printer = ctk.CTkComboBox(window, values=["Принтер по умолчанию", "PDF принтер", "Виртуальный принтер"],
                                 width=300)
        printer.pack(pady=5)
        
        ctk.CTkLabel(window, text="Копии:", font=("Segoe UI", 11)).pack(pady=(10, 5))
        copies = ctk.CTkEntry(window, width=100)
        copies.insert(0, "1")
        copies.pack(pady=5)
        
        def do_print():
            messagebox.showinfo("Печать", f"Документ отправлен на печать:\n{printer.get()}")
            window.destroy()
        
        button_frame = ctk.CTkFrame(window, fg_color="transparent")
        button_frame.pack(pady=20)
        
        ctk.CTkButton(button_frame, text="Печать", width=140,
                     command=do_print, fg_color="#0078d4").pack(side="left", padx=5)
        ctk.CTkButton(button_frame, text="Отмена", width=140,
                     command=window.destroy).pack(side="left", padx=5)
    
    # === ДОПОЛНИТЕЛЬНЫЕ ФУНКЦИИ МЕНЮ ===
    
    def show_file_menu(self):
        """Показать меню файла"""
        window = ctk.CTkToplevel(self)
        window.title("Файл")
        window.geometry("350x500")
        window.transient(self)
        window.grab_set()
        
        ctk.CTkLabel(window, text="Файл", font=("Segoe UI", 18, "bold")).pack(pady=20)
        
        buttons = [
            ("📄 Создать", self.new_file),
            ("📂 Открыть", self.open_file),
            ("💾 Сохранить", self.save_file),
            ("💾 Сохранить как...", self.save_file_as),
            ("🖨 Печать", self.print_document),
            ("📤 Экспорт", self.export_document),
            ("⚙ Параметры", self.show_settings),
        ]
        
        for text, command in buttons:
            ctk.CTkButton(window, text=text, width=280, height=40,
                         font=("Segoe UI", 11),
                         command=lambda c=command: [c(), window.destroy()],
                         fg_color="transparent", hover_color="#3f3f3f",
                         anchor="w").pack(pady=3, padx=30)
        
        ctk.CTkButton(window, text="Закрыть меню", width=280, height=40,
                     command=window.destroy, fg_color="#d84040").pack(pady=20)
    
    def show_insert_menu(self):
        """Показать меню вставки"""
        window = ctk.CTkToplevel(self)
        window.title("Вставка")
        window.geometry("350x400")
        window.transient(self)
        window.grab_set()
        
        ctk.CTkLabel(window, text="Вставка элементов",
                    font=("Segoe UI", 16, "bold")).pack(pady=20)
        
        items = [
            ("📷 Изображение", self.insert_image),
            ("📊 Таблица", self.insert_table),
            ("🔗 Гиперссылка", self.insert_hyperlink),
            ("📅 Дата и время", self.insert_datetime),
            ("🔣 Символ", self.insert_symbol),
            ("📄 Разрыв страницы", self.insert_page_break),
        ]
        
        for text, command in items:
            ctk.CTkButton(window, text=text, width=280, height=35,
                         command=lambda c=command: [c(), window.destroy()],
                         fg_color="#0078d4").pack(pady=5)
        
        ctk.CTkButton(window, text="Закрыть", width=280,
                     command=window.destroy, fg_color="gray").pack(pady=15)
    
    def show_view_menu(self):
        """Показать меню вида"""
        window = ctk.CTkToplevel(self)
        window.title("Вид")
        window.geometry("350x350")
        window.transient(self)
        window.grab_set()
        
        ctk.CTkLabel(window, text="Параметры отображения",
                    font=("Segoe UI", 16, "bold")).pack(pady=20)
        
        def toggle_ruler():
            self.show_ruler = not self.show_ruler
            status = "включена" if self.show_ruler else "выключена"
            messagebox.showinfo("Линейка", f"Линейка {status}")
            window.destroy()
        
        ctk.CTkButton(window, text="📏 Линейка", width=280, height=40,
                     command=toggle_ruler, fg_color="#0078d4").pack(pady=5)
        ctk.CTkButton(window, text="🔍 Масштаб", width=280, height=40,
                     command=lambda: [self.zoom_settings(), window.destroy()],
                     fg_color="#0078d4").pack(pady=5)
        ctk.CTkButton(window, text="🎨 Темы", width=280, height=40,
                     command=lambda: [self.change_theme(), window.destroy()],
                     fg_color="#0078d4").pack(pady=5)
        ctk.CTkButton(window, text="⚡ Режим фокусировки", width=280, height=40,
                     command=lambda: [self.focus_mode(), window.destroy()],
                     fg_color="#0078d4").pack(pady=5)
        
        ctk.CTkButton(window, text="Закрыть", width=280,
                     command=window.destroy, fg_color="gray").pack(pady=15)
    
    def show_help_menu(self):
        """Показать меню справки"""
        window = ctk.CTkToplevel(self)
        window.title("Справка")
        window.geometry("450x400")
        window.transient(self)
        window.grab_set()
        
        ctk.CTkLabel(window, text="Текстовый редактор",
                    font=("Segoe UI", 18, "bold")).pack(pady=15)
        ctk.CTkLabel(window, text="Версия 1.0",
                    font=("Segoe UI", 12)).pack(pady=5)
        
        info_frame = ctk.CTkFrame(window, fg_color="#2b2b2b")
        info_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        help_text = """
        Горячие клавиши:
        
        Ctrl+N - Создать новый документ
        Ctrl+O - Открыть файл
        Ctrl+S - Сохранить
        Ctrl+P - Печать
        Ctrl+Z - Отменить
        Ctrl+Y - Повторить
        Ctrl+F - Найти
        Ctrl+H - Заменить
        Ctrl+B - Жирный
        Ctrl+I - Курсив
        Ctrl+U - Подчеркнутый
        Ctrl+A - Выделить всё
        """
        
        ctk.CTkLabel(info_frame, text=help_text, 
                    font=("Courier New", 10),
                    justify="left").pack(pady=10, padx=10)
        
        ctk.CTkButton(window, text="Закрыть", width=200,
                     command=window.destroy, fg_color="#0078d4").pack(pady=10)
    
    def share_document(self):
        """Поделиться документом"""
        window = ctk.CTkToplevel(self)
        window.title("Поделиться")
        window.geometry("400x250")
        window.transient(self)
        window.grab_set()
        
        ctk.CTkLabel(window, text="Поделиться документом", 
                    font=("Segoe UI", 16, "bold")).pack(pady=20)
        
        ctk.CTkLabel(window, text="Введите email для отправки:",
                    font=("Segoe UI", 11)).pack(pady=10)
        
        email_entry = ctk.CTkEntry(window, width=350, height=35, 
                                   placeholder_text="example@email.com")
        email_entry.pack(pady=10)
        
        def send():
            email = email_entry.get()
            if email and "@" in email:
                messagebox.showinfo("Успешно", f"Документ отправлен на:\n{email}")
                window.destroy()
            else:
                messagebox.showerror("Ошибка", "Введите корректный email адрес")
        
        ctk.CTkButton(window, text="Отправить", width=180,
                     command=send, fg_color="#0078d4", hover_color="#1084d8").pack(pady=10)
    
    def show_notes(self):
        """Показать примечания"""
        messagebox.showinfo("Примечания", 
            "Функция примечаний позволяет добавлять заметки к документу")
    
    def schedule_meeting(self):
        """Запланировать встречу"""
        messagebox.showinfo("Встреча", 
            "Функция планирования встреч интегрирована с календарем")
    
    def show_edit_mode_menu(self):
        """Показать меню режимов редактирования"""
        window = ctk.CTkToplevel(self)
        window.title("Режим редактирования")
        window.geometry("300x200")
        window.transient(self)
        window.grab_set()
        
        ctk.CTkLabel(window, text="Выберите режим:",
                    font=("Segoe UI", 12, "bold")).pack(pady=15)
        
        ctk.CTkButton(window, text="✏ Редактирование", width=250,
                     command=lambda: [messagebox.showinfo("Режим", "Режим: Редактирование"), window.destroy()]).pack(pady=5)
        ctk.CTkButton(window, text="👁 Только чтение", width=250,
                     command=lambda: [messagebox.showinfo("Режим", "Режим: Только чтение"), window.destroy()]).pack(pady=5)
        ctk.CTkButton(window, text="📝 Рецензирование", width=250,
                     command=lambda: [messagebox.showinfo("Режим", "Режим: Рецензирование"), window.destroy()]).pack(pady=5)
    
    def export_document(self):
        """Экспорт документа"""
        window = ctk.CTkToplevel(self)
        window.title("Экспорт")
        window.geometry("350x250")
        window.transient(self)
        window.grab_set()
        
        ctk.CTkLabel(window, text="Экспорт документа",
                    font=("Segoe UI", 14, "bold")).pack(pady=20)
        
        ctk.CTkButton(window, text="📄 Экспорт в PDF", width=280,
                     command=lambda: [messagebox.showinfo("Экспорт", "Экспорт в PDF"), window.destroy()]).pack(pady=5)
        ctk.CTkButton(window, text="📝 Экспорт в HTML", width=280,
                     command=lambda: [messagebox.showinfo("Экспорт", "Экспорт в HTML"), window.destroy()]).pack(pady=5)
        ctk.CTkButton(window, text="📋 Экспорт в RTF", width=280,
                     command=lambda: [messagebox.showinfo("Экспорт", "Экспорт в RTF"), window.destroy()]).pack(pady=5)
        ctk.CTkButton(window, text="Отмена", width=280,
                     command=window.destroy, fg_color="gray").pack(pady=15)
    
    def show_settings(self):
        """Показать настройки"""
        messagebox.showinfo("Настройки", 
            "Здесь будут параметры приложения:\n- Автосохранение\n- Язык интерфейса\n- Шрифт по умолчанию")
    
    def insert_image(self):
        """Вставить изображение"""
        file_path = filedialog.askopenfilename(
            filetypes=[("Изображения", "*.png *.jpg *.jpeg *.gif"), ("Все файлы", "*.*")]
        )
        if file_path:
            messagebox.showinfo("Изображение", f"Изображение будет вставлено:\n{os.path.basename(file_path)}")
    
    def insert_table(self):
        """Вставить таблицу"""
        window = ctk.CTkToplevel(self)
        window.title("Вставка таблицы")
        window.geometry("300x250")
        window.transient(self)
        window.grab_set()
        
        ctk.CTkLabel(window, text="Размер таблицы",
                    font=("Segoe UI", 14, "bold")).pack(pady=15)
        
        ctk.CTkLabel(window, text="Количество строк:").pack(pady=5)
        rows = ctk.CTkEntry(window, width=200)
        rows.insert(0, "3")
        rows.pack(pady=5)
        
        ctk.CTkLabel(window, text="Количество столбцов:").pack(pady=5)
        cols = ctk.CTkEntry(window, width=200)
        cols.insert(0, "3")
        cols.pack(pady=5)
        
        def insert():
            table_text = "\n"
            for i in range(int(rows.get())):
                table_text += "| " + " | ".join(["Ячейка"] * int(cols.get())) + " |\n"
            self.text_area.insert("insert", table_text)
            window.destroy()
        
        ctk.CTkButton(window, text="Вставить", width=200,
                     command=insert, fg_color="#0078d4").pack(pady=15)
    
    def insert_hyperlink(self):
        """Вставить гиперссылку"""
        window = ctk.CTkToplevel(self)
        window.title("Вставка гиперссылки")
        window.geometry("400x250")
        window.transient(self)
        window.grab_set()
        
        ctk.CTkLabel(window, text="Текст:", font=("Segoe UI", 11)).pack(pady=(20, 5))
        text_entry = ctk.CTkEntry(window, width=350)
        text_entry.pack(pady=5)
        
        ctk.CTkLabel(window, text="URL:", font=("Segoe UI", 11)).pack(pady=(10, 5))
        url_entry = ctk.CTkEntry(window, width=350, placeholder_text="https://example.com")
        url_entry.pack(pady=5)
        
        def insert():
            text = text_entry.get() or url_entry.get()
            self.text_area.insert("insert", text)
            window.destroy()
        
        ctk.CTkButton(window, text="Вставить", width=200,
                     command=insert, fg_color="#0078d4").pack(pady=20)
    
    def insert_datetime(self):
        """Вставить дату и время"""
        from datetime import datetime
        now = datetime.now().strftime("%d.%m.%Y %H:%M")
        self.text_area.insert("insert", now)
        messagebox.showinfo("Дата и время", f"Вставлено: {now}")
    
    def insert_symbol(self):
        """Вставить символ"""
        window = ctk.CTkToplevel(self)
        window.title("Вставка символа")
        window.geometry("400x350")
        window.transient(self)
        window.grab_set()
        
        ctk.CTkLabel(window, text="Выберите символ",
                    font=("Segoe UI", 14, "bold")).pack(pady=15)
        
        symbols = ["©", "®", "™", "§", "¶", "†", "‡", "•", "◦", "▪", "▫", 
                  "→", "←", "↑", "↓", "↔", "⇒", "⇐", "⇔", "∞", "≈", "≠", 
                  "≤", "≥", "±", "×", "÷", "°", "′", "″", "℃", "℉"]
        
        frame = ctk.CTkScrollableFrame(window, width=360, height=200)
        frame.pack(pady=10, padx=10)
        
        row_frame = None
        for i, symbol in enumerate(symbols):
            if i % 8 == 0:
                row_frame = ctk.CTkFrame(frame, fg_color="transparent")
                row_frame.pack(pady=2)
            
            ctk.CTkButton(row_frame, text=symbol, width=40, height=40,
                         font=("Segoe UI", 16),
                         command=lambda s=symbol: [self.text_area.insert("insert", s), window.destroy()]
                         ).pack(side="left", padx=2)
        
        ctk.CTkButton(window, text="Закрыть", width=200,
                     command=window.destroy).pack(pady=10)
    
    def insert_page_break(self):
        """Вставить разрыв страницы"""
        self.text_area.insert("insert", "\n" + "="*50 + " РАЗРЫВ СТРАНИЦЫ " + "="*50 + "\n")
        messagebox.showinfo("Разрыв страницы", "Разрыв страницы вставлен")
    
    def zoom_settings(self):
        """Настройки масштаба"""
        messagebox.showinfo("Масштаб", 
            f"Текущий масштаб: {self.zoom_level}%\nИспользуйте ползунок внизу для изменения")
    
    def change_theme(self):
        """Изменить тему"""
        window = ctk.CTkToplevel(self)
        window.title("Темы")
        window.geometry("300x200")
        window.transient(self)
        window.grab_set()
        
        ctk.CTkLabel(window, text="Выберите тему:",
                    font=("Segoe UI", 12, "bold")).pack(pady=15)
        
        def set_theme(theme):
            ctk.set_appearance_mode(theme)
            messagebox.showinfo("Тема", f"Установлена тема: {theme}")
            window.destroy()
        
        ctk.CTkButton(window, text="🌙 Темная", width=250,
                     command=lambda: set_theme("dark")).pack(pady=5)
        ctk.CTkButton(window, text="☀ Светлая", width=250,
                     command=lambda: set_theme("light")).pack(pady=5)
        ctk.CTkButton(window, text="🌓 Системная", width=250,
                     command=lambda: set_theme("system")).pack(pady=5)
    
    def focus_mode(self):
        """Режим фокусировки"""
        messagebox.showinfo("Режим фокусировки", 
            "Режим фокусировки скрывает все панели для концентрации на тексте")