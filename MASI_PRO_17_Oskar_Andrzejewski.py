import tkinter as tk
from tkinter import Toplevel, Label, Entry, Button, StringVar, OptionMenu, Menu, Spinbox
from tkinter import font
from supabase import create_client, Client

class DatabaseHandler:
    def __init__(self):
        self.supabase_url = "https://lxrnycgqiejbhjfbdxcz.supabase.co"
        self.supabase_key = ("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imx4cm55Y2dxaWVqYmhqZmJkeGN6Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0Mjc5OTQzNywiZXhwIjoyMDU4Mzc1NDM3fQ.pXO3pWzzeU8VOk7RPXNozduuWz2lAdm4-l0fgk2PIuM")
        self.client: Client = create_client(self.supabase_url, self.supabase_key)

    def insert_operation(self, data: dict):
        print("Dane przesyłane:", data)
        result = self.client.table('Operacje').insert(data).execute()
        return result

class Menu_Modal:
    def __init__(self, root, main_window):
        self.root = root
        self.main_window = main_window

    def open_confirmation_dialog(self):
        modal = Toplevel(self.root)
        modal.title("Podstaw")
        modal.geometry("400x100")
        Label(modal, text="Za który uniterm chcesz podstawić operację zrównoleglenia?").pack(pady=10)

        def uni_1():
            self.main_window.handle_dialog(True)
            modal.destroy()

        def uni_2():
            self.main_window.handle_dialog(False)
            modal.destroy()

        def on_cancel():
            print("Anulowano")
            modal.destroy()

        button_frame = tk.Frame(modal)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="1 uniterm", command=uni_1).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="2 uniterm", command=uni_2).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Anuluj", command=on_cancel).pack(side=tk.LEFT, padx=5)

class ModalWindow:
    def __init__(self, root, mode, callback):
        self.root = root
        self.mode = mode
        self.callback = callback
        self.entries = []
        self.separator_var = StringVar()
        self.separator_var.set(";")
        self.create_modal()

    def create_modal(self):
        modal = Toplevel(self.root)
        modal.title(self.mode.capitalize())

        num_entries = 3 if self.mode == "eliminacja" else 2
        for i in range(num_entries):
            Label(modal, text=f"Tekst {i + 1}:").grid(row=i, column=0)
            entry = Entry(modal)
            entry.grid(row=i, column=1)
            self.entries.append(entry)

        Label(modal, text="Separator:").grid(row=num_entries, column=0)
        separator_menu = OptionMenu(modal, self.separator_var, ";", ",")
        separator_menu.grid(row=num_entries, column=1)

        Button(modal, text="OK", command=lambda: self.on_ok(modal)).grid(row=num_entries + 1, columnspan=2, pady=10)

    def on_ok(self, modal):
        parts = [entry.get() for entry in self.entries if entry.get()]
        separator = self.separator_var.get()
        self.callback(self.mode, parts, separator)
        modal.destroy()

class MASI_PRO:
    def __init__(self, root):
        self.root = root
        self.root.title("MASI_PRO_17_OA")
    
        main_area = tk.Frame(root)
        main_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
        self.canvas = tk.Canvas(main_area, width=400, height=400)
        self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    
        self.text_eliminacja = ""
        self.text_zrownoleglenia = ""
    
        self.separator_eliminacja = ""
        self.separator_zrownoleglenia = ""
    
        self.parts_eliminacja = []
        self.original_parts_eliminacja = []
        self.parts_zrownoleglenia = []
    
        self.current_font_family = "Arial"
        self.current_font_size = 20
    
        self.font_frame = tk.Frame(root)
        self.font_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)
    
        Label(self.font_frame, text="Rodzaj czcionki:").pack(pady=5)
        font_families = list(font.families())
        self.font_family_var = StringVar()
        self.font_family_var.set(self.current_font_family)
        font_menu = OptionMenu(self.font_frame, self.font_family_var, *sorted(font_families), command=self.update_font)
        font_menu.pack()
    
        Label(self.font_frame, text="Rozmiar czcionki:").pack(pady=5)
        self.font_size_var = tk.IntVar()
        self.font_size_var.set(self.current_font_size)
        font_size_spinbox = Spinbox(self.font_frame, from_=8, to=72, textvariable=self.font_size_var, command=self.update_font)
        font_size_spinbox.pack()
    
        self.modal = Menu_Modal(self.root, self)
        self.create_menu()
    
        self.button_frame = tk.Frame(main_area)
        self.button_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
    
        center_frame = tk.Frame(self.button_frame)
        center_frame.pack()
        
        self.eliminacja_button = tk.Button(center_frame, text="Eliminacja", command=lambda: self.open_modal("eliminacja"))
        self.eliminacja_button.pack(side=tk.LEFT, padx=10)
    
        self.zrownoleglenia_button = tk.Button(center_frame, text="Zrównoleglenie", command=lambda: self.open_modal("zrownoleglenia"))
        self.zrownoleglenia_button.pack(side=tk.LEFT, padx=10)
    
        self.clear_button = tk.Button(center_frame, text="Wyczyść", command=self.clear_canvas)
        self.clear_button.pack(side=tk.LEFT, padx=10)
    
        self.db_handler = DatabaseHandler()
        self.modal_win = ""


    def create_menu(self):
        menubar = Menu(self.root)
        file_menu = Menu(menubar, tearoff=0)
        file_menu.add_command(label="Połącz", command=self.modal.open_confirmation_dialog)
        menubar.add_cascade(label="File", menu=file_menu)
        self.root.config(menu=menubar)

    def clear_canvas(self):
        self.canvas.delete("all")
        self.text_eliminacja = ""
        self.text_zrownoleglenia = ""
        self.parts_eliminacja = []
        self.original_parts_eliminacja = []
        self.parts_zrownoleglenia = []

    def open_modal(self, mode):
        self.modal_win = ModalWindow(self.root, mode, self.handle_modal_response)

    def handle_modal_response(self, mode, parts, separator):
        text = separator.join(parts)
        if mode == "eliminacja":
            self.text_eliminacja = text
            self.parts_eliminacja = parts[:]
            self.original_parts_eliminacja = parts[:]
            self.separator_eliminacja = separator
        else:
            self.text_zrownoleglenia = text
            self.parts_zrownoleglenia = parts
            self.separator_zrownoleglenia = separator
        self.draw_uniterm()

    def handle_dialog(self, option):
        odp = option

        if option:
            if self.parts_eliminacja and self.parts_zrownoleglenia:
                self.parts_eliminacja = self.original_parts_eliminacja[:]
                self.parts_eliminacja[0] = self.text_zrownoleglenia
                self.text_eliminacja = self.separator_eliminacja.join(self.parts_eliminacja)
                self.draw_uniterm(copy_line=True)
        else:
            if len(self.parts_eliminacja) > 1 and self.parts_zrownoleglenia:
                self.parts_eliminacja = self.original_parts_eliminacja[:]
                self.parts_eliminacja[1] = self.text_zrownoleglenia
                self.text_eliminacja = self.separator_eliminacja.join(self.parts_eliminacja)
                self.draw_uniterm(copy_line=True, shift_line=True)
                odp = False

        text_teliminacja_ori = self.separator_eliminacja.join(self.original_parts_eliminacja)
        data = {
            'created_at': 'now()',
            'eliminacja': text_teliminacja_ori,
            'zrownoleglenie': self.text_zrownoleglenia,
            'polaczenie': odp,
            'wynik': self.text_eliminacja,
        }

        self.db_handler.insert_operation(data)

    def draw_uniterm(self, copy_line=False, shift_line=False):
        self.canvas.delete("all")
        x_start = 50
        y_text = 80
        shift_amount = 0
        separator_width = 10

        selected_font = (self.current_font_family, self.current_font_size, "bold")

        if self.text_eliminacja:
            text_id = self.canvas.create_text(x_start, y_text, text=self.text_eliminacja, anchor="w", font=selected_font)
            bbox = self.canvas.bbox(text_id)
            if bbox:
                text_width = bbox[2] - bbox[0]
                y_line = bbox[1] - 13
                self.canvas.create_line(x_start - 5, y_line, x_start + text_width + 5, y_line, width=4)
                self.canvas.create_line(x_start - 5, y_line - 5, x_start - 5, y_line + 5, width=4)
                self.canvas.create_line(x_start + text_width + 5, y_line - 5, x_start + text_width + 5, y_line + 5, width=4)

                if shift_line and self.original_parts_eliminacja:
                    text_id = self.canvas.create_text(x_start, y_text, text=self.original_parts_eliminacja[0], anchor="w", font=selected_font)
                    bbox = self.canvas.bbox(text_id)
                    if bbox:
                        shift_amount = bbox[2] - bbox[0] + separator_width

        if self.text_zrownoleglenia:
            y_text = 130
            text_id = self.canvas.create_text(x_start, y_text, text=self.text_zrownoleglenia, anchor="w", font=selected_font)
            bbox = self.canvas.bbox(text_id)
            if bbox:
                text_width = bbox[2] - bbox[0]
                y_line = bbox[1] - 10
                self.canvas.create_line(x_start - 5, y_line, x_start + text_width + 5, y_line, width=4)
                self.canvas.create_line(x_start - 5, y_line - 2, x_start - 5, y_line + 15, width=4)
                self.canvas.create_line(x_start + text_width + 5, y_line - 2, x_start + text_width + 5, y_line + 15, width=4)

                if copy_line:
                    self.canvas.create_line(x_start - 2 + shift_amount, 57, x_start + text_width + 2 + shift_amount, 57, width=4)
                    self.canvas.create_line(x_start - 2 + shift_amount, 55, x_start - 2 + shift_amount, 72, width=4)
                    self.canvas.create_line(x_start + text_width + 2 + shift_amount, 55, x_start + text_width + 2 + shift_amount, 72, width=4)

    def update_font(self, *_):
        self.current_font_family = self.font_family_var.get()
        self.current_font_size = self.font_size_var.get()
        self.draw_uniterm()

if __name__ == "__main__":
    root = tk.Tk()
    app = MASI_PRO(root)
    root.mainloop()
