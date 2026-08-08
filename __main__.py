import sys
import json
import os
import customtkinter as ctk
from ui_builder import UI

SAVE_FILE = "saved_parts.json"

LANG = {
    "ru": {
        "app_title": "3D PRINT.CALC",
        "sidebar_title": "Мои Расчеты",
        "revenue": "Выручка",
        "socials_btn": "🌐 Создатель",
        "lang_btn": "Switch to English",
        "home_title": "3D PRINT.CALC",
        "home_desc": (
            "Добро пожаловать!"
        ),
        "new_part_btn": "➕ Рассчитать новую деталь",
        "form_title": "Параметры печати детали",
        "ph_name": "Название (например: Брелок)",
        "ph_weight": "Вес детали в граммах (например: 12)",
        "ph_time": "Время печати в часах (например: 1.5)",
        "ph_op": "Время работы оператора (часы, можно 0)",
        "type_label": "Выберите тип детали:",
        "type1": "1. Мелочёвка (до 250₽)",
        "type2": "2. Стандартная",
        "type3": "3. Художественная",
        "calc_save_btn": "Рассчитать и сохранить",
        "cancel_btn": "Отмена",
        "error_msg": "Ошибка: проверьте правильность введенных данных!",
        "home_btn": "🏠 На главную",
        "del_btn": "🗑 Удалить проект",
        "socials_title": "Информация о создании",
        "socials_text": "Создатель: Senzy\nTelegram: @Senzy_the_novabeast\nDiscord: @Senzy_nova_40316",
        "close_btn": "Закрыть",
        "weight_lbl": "Вес",
        "time_lbl": "Время печати",
        "type_lbl_res": "Тип детали",
        "mult_lbl": "Множитель веса",
        "mat_lbl": "Материал",
        "final_lbl": "ИТОГОВАЯ ЦЕНА",
        "themes": {"dark": "🌙 Тёмная", "light": "☀️ Светлая", "ficsit": "⚙️ Ficsit.corp"}
    },
    "en": {
        "app_title": "3D PRINT.CALC",
        "sidebar_title": "My Calculations",
        "revenue": "Revenue",
        "socials_btn": "🌐 Creator",
        "lang_btn": "Русский язык",
        "home_title": "3D PRINT.CALC",
        "home_desc": (
            "Welcome!"
        ),
        "new_part_btn": "➕ Calculate New Part",
        "form_title": "Part Printing Parameters",
        "ph_name": "Name (e.g., Keychain)",
        "ph_weight": "Weight in grams (e.g., 12)",
        "ph_time": "Print time in hours (e.g., 1.5)",
        "ph_op": "Operator time (hours, can be 0)",
        "type_label": "Select part type:",
        "type1": "1. Small part (up to 250₽)",
        "type2": "2. Standard",
        "type3": "3. Artistic",
        "calc_save_btn": "Calculate & Save",
        "cancel_btn": "Cancel",
        "error_msg": "Error: check entered data!",
        "home_btn": "🏠 Home",
        "del_btn": "🗑 Delete Project",
        "socials_title": "Creator Info",
        "socials_text": "Creator: Senzy\nTelegram: @Senzy_the_novabeast\nDiscord: @Senzy_nova_40316",
        "close_btn": "Close",
        "weight_lbl": "Weight",
        "time_lbl": "Print time",
        "type_lbl_res": "Part type",
        "mult_lbl": "Weight multiplier",
        "mat_lbl": "Material",
        "final_lbl": "FINAL PRICE",
        "themes": {"dark": "🌙 Dark", "light": "☀️ Light", "ficsit": "⚙️ Ficsit.corp"}
    }
}

class SocialsModal(ctk.CTkToplevel):
    def __init__(self, parent, lang_code):
        super().__init__(parent)
        t = LANG[lang_code]
        c = UI.get_colors()
        
        self.title("Creator")
        self.geometry("380x260")
        self.resizable(False, False)
        
        self.transient(parent)
        self.grab_set()
        
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (380 // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (260 // 2)
        self.geometry(f"+{x}+{y}")
        
        self.configure(fg_color=c["BG_DARK"])
        
        UI.title(self, text=t["socials_title"]).pack(pady=(20, 10))
        UI.text(self, text=t["socials_text"], muted=False, justify="center").pack(pady=10)
        
        ctk.CTkButton(
            self, text=t["close_btn"], width=120, height=34,
            fg_color=c["BORDER_COLOR"], hover_color=c["ACCENT"], text_color=c["TEXT_MAIN"],
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            command=self.destroy
        ).pack(pady=15)


class PrintCalculatorApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        UI.setup()
        
        self.current_lang = "ru"
        self.current_theme_key = "dark"
        
        c = UI.get_colors()
        self.title(LANG[self.current_lang]["app_title"])
        self.geometry("980x660")
        self.configure(fg_color=c["BG_DARK"])
        
        self.saved_parts = {}
        self.load_data()
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        self.sidebar = ctk.CTkScrollableFrame(self, width=250, corner_radius=0, fg_color=c["BG_DARK"])
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        self.sidebar_header = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.sidebar_header.pack(fill="x", padx=15, pady=20)
        
        self.sidebar_title_lbl = ctk.CTkLabel(
            self.sidebar_header, text="", 
            font=ctk.CTkFont(family="Segoe UI", size=18, weight="bold")
        )
        self.sidebar_title_lbl.pack(anchor="w")
        
        self.total_revenue_label = ctk.CTkLabel(
            self.sidebar_header, text="", 
            font=ctk.CTkFont(family="Consolas", size=13, weight="bold"),
            text_color=c["CYAN"]
        )
        self.total_revenue_label.pack(anchor="w", pady=(5, 0))
        
        self.parts_list = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.parts_list.pack(fill="both", expand=True)
        
        sidebar_footer = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        sidebar_footer.pack(fill="x", padx=15, pady=15)
        
        self.socials_btn = UI.button(
            sidebar_footer, text="", width=220, height=36,
            command=self.open_socials
        )
        self.socials_btn.pack(pady=(0, 8))
        
        t_dict = LANG[self.current_lang]["themes"]
        self.theme_menu = ctk.CTkOptionMenu(
            sidebar_footer, values=list(t_dict.values()), width=220, height=32,
            command=self.change_theme,
            fg_color=c["BORDER_COLOR"], button_color=c["ACCENT"], button_hover_color=c["ACCENT_HOVER"]
        )
        self.theme_menu.set(t_dict["dark"])
        self.theme_menu.pack(pady=(0, 8))
        
        self.lang_btn = ctk.CTkButton(
            sidebar_footer, text="", width=220, height=32,
            fg_color=c["BORDER_COLOR"], hover_color=c["ACCENT"], text_color=c["TEXT_MUTED"],
            font=ctk.CTkFont(family="Segoe UI", size=12),
            command=self.toggle_language
        )
        self.lang_btn.pack()
        
        self.main_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        self.update_ui_texts()
        self.refresh_sidebar_parts()
        self.show_home()

    def change_theme(self, choice):
        t_dict_themes = LANG[self.current_lang]["themes"]
        for key, val in t_dict_themes.items():
            if val == choice:
                self.current_theme_key = key
                UI.set_theme(key)
                break
        
        c = UI.get_colors()
        self.configure(fg_color=c["BG_DARK"])
        self.sidebar.configure(fg_color=c["BG_DARK"])
        self.total_revenue_label.configure(text_color=c["CYAN"])
        
        self.theme_menu.configure(fg_color=c["BORDER_COLOR"], button_color=c["ACCENT"], button_hover_color=c["ACCENT_HOVER"])
        self.lang_btn.configure(fg_color=c["BORDER_COLOR"], hover_color=c["ACCENT"], text_color=c["TEXT_MUTED"])
        
        self.refresh_sidebar_parts()
        if hasattr(self, "current_view_func") and self.current_view_func:
            self.current_view_func()
        else:
            self.show_home()

    def toggle_language(self):
        self.current_lang = "en" if self.current_lang == "ru" else "ru"
        
        t_dict_themes = LANG[self.current_lang]["themes"]
        current_translated_theme = t_dict_themes[self.current_theme_key]
        self.theme_menu.configure(values=list(t_dict_themes.values()))
        self.theme_menu.set(current_translated_theme)
        
        self.update_ui_texts()
        self.refresh_sidebar_parts()
        
        if hasattr(self, "current_view_func") and self.current_view_func:
            self.current_view_func()
        else:
            self.show_home()

    def update_ui_texts(self):
        t = LANG[self.current_lang]
        self.title(t["app_title"])
        self.sidebar_title_lbl.configure(text=t["sidebar_title"])
        self.socials_btn.configure(text=t["socials_btn"])
        self.lang_btn.configure(text=t["lang_btn"])
        self.update_revenue_counter()

    def load_data(self):
        if os.path.exists(SAVE_FILE):
            try:
                with open(SAVE_FILE, "r", encoding="utf-8") as f:
                    self.saved_parts = json.load(f)
            except Exception:
                self.saved_parts = {}

    def save_data(self):
        try:
            with open(SAVE_FILE, "w", encoding="utf-8") as f:
                json.dump(self.saved_parts, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Ошибка сохранения: {e}")

    def update_revenue_counter(self):
        t = LANG[self.current_lang]
        total = 0.0
        for data in self.saved_parts.values():
            try:
                price_str = data["raw_price"]
                total += float(price_str)
            except (ValueError, KeyError):
                pass
        self.total_revenue_label.configure(text=f"{t['revenue']}: {total:.2f} ₽")

    def refresh_sidebar_parts(self):
        for widget in self.parts_list.winfo_children():
            widget.destroy()
            
        for name in self.saved_parts.keys():
            UI.button(
                self.parts_list, text=name, width=220, height=36, 
                command=lambda n=name: self.show_part(n)
            ).pack(pady=4, fill="x")
            
        self.update_revenue_counter()

    def open_socials(self):
        SocialsModal(self, self.current_lang)

    def clear_main(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def show_home(self):
        self.clear_main()
        self.current_view_func = self.show_home
        t = LANG[self.current_lang]
        
        UI.title(self.main_frame, text=t["home_title"]).pack(pady=30)
        UI.text(self.main_frame, text=t["home_desc"], muted=True, justify="left").pack(pady=10)
        
        UI.button(
            self.main_frame, text=t["new_part_btn"], 
            accent=True, width=280, height=48, 
            command=self.show_form
        ).pack(pady=40)

    def show_form(self):
        self.clear_main()
        self.current_view_func = self.show_form
        t = LANG[self.current_lang]
        
        UI.title(self.main_frame, text=t["form_title"]).pack(pady=15)
        
        self.entry_name = UI.entry(self.main_frame, placeholder=t["ph_name"])
        self.entry_name.pack(pady=8)
        
        self.entry_weight = UI.entry(self.main_frame, placeholder=t["ph_weight"])
        self.entry_weight.pack(pady=8)
        
        self.entry_time = UI.entry(self.main_frame, placeholder=t["ph_time"])
        self.entry_time.pack(pady=8)
        
        self.entry_op = UI.entry(self.main_frame, placeholder=t["ph_op"])
        self.entry_op.pack(pady=8)
        
        UI.text(self.main_frame, text=t["type_label"]).pack(pady=(10, 0))
        
        self.type_var = ctk.StringVar(value="2")
        t_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        t_frame.pack(pady=5)
        
        ctk.CTkRadioButton(t_frame, text=t["type1"], variable=self.type_var, value="1").pack(side="left", padx=10)
        ctk.CTkRadioButton(t_frame, text=t["type2"], variable=self.type_var, value="2").pack(side="left", padx=10)
        ctk.CTkRadioButton(t_frame, text=t["type3"], variable=self.type_var, value="3").pack(side="left", padx=10)
        
        self.error_label = ctk.CTkLabel(self.main_frame, text="", text_color="red")
        self.error_label.pack(pady=5)
        
        b_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        b_frame.pack(pady=20)
        
        UI.button(b_frame, text=t["calc_save_btn"], accent=True, width=180, command=self.process).grid(row=0, column=0, padx=10)
        UI.button(b_frame, text=t["cancel_btn"], width=120, command=self.show_home).grid(row=0, column=1, padx=10)

    def process(self):
        t_dict = LANG[self.current_lang]
        name = self.entry_name.get().strip() or f"Part #{len(self.saved_parts) + 1}"
            
        try:
            w = float(self.entry_weight.get().replace(',', '.'))
            t = float(self.entry_time.get().replace(',', '.'))
            op_input = self.entry_op.get().strip()
            op = float(op_input.replace(',', '.')) if op_input else 0.0
            d_type = int(self.type_var.get())
            
            mat_cost = w * 3.0
            rate = 400 if d_type == 3 else 350
            op_cost = 50 if op == 0 else op * 600
            base = mat_cost + (t * rate) + op_cost
            
            if w < 10: mult = 0.75
            elif w < 25: mult = 0.85
            elif w < 60: mult = 1.00
            elif w < 120: mult = 1.10
            else: mult = 1.20
                
            adj = base * mult
            final = min(250, adj) if d_type == 1 else adj
                
            self.saved_parts[name] = {
                "raw_price": final,
                t_dict["weight_lbl"]: f"{w} g",
                t_dict["time_lbl"]: f"{t} h",
                t_dict["type_lbl_res"]: f"Type {d_type}",
                t_dict["mult_lbl"]: f"x{mult:.2f}",
                t_dict["mat_lbl"]: f"{mat_cost:.2f} ₽",
                t_dict["final_lbl"]: f"{final:.2f} ₽"
            }
            
            self.save_data()
            self.refresh_sidebar_parts()
            self.show_part(name)
            
        except ValueError:
            self.error_label.configure(text=t_dict["error_msg"])

    def show_part(self, name):
        self.clear_main()
        self.current_view_func = lambda: self.show_part(name)
        t = LANG[self.current_lang]
        
        if name not in self.saved_parts:
            self.show_home()
            return
            
        data = self.saved_parts[name]
        
        UI.title(self.main_frame, text=f"Part: {name}" if self.current_lang == "en" else f"Деталь: {name}").pack(pady=20)
        
        card = UI.card(self.main_frame)
        card.pack(pady=10, padx=20, fill="x")
        
        for k, v in data.items():
            if k == "raw_price":
                continue
            row = ctk.CTkFrame(card, fg_color="transparent")
            row.pack(fill="x", padx=20, pady=8)
            
            UI.text(row, text=k, font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold")).pack(side="left")
            
            if k == t["final_lbl"]:
                UI.price(row, text=v).pack(side="right")
            else:
                UI.text(row, text=v, muted=True).pack(side="right")
            
        btn_action_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        btn_action_frame.pack(pady=30)
        
        UI.button(btn_action_frame, text=t["home_btn"], width=180, command=self.show_home).grid(row=0, column=0, padx=10)
        
        c = UI.get_colors()
        del_btn = ctk.CTkButton(
            btn_action_frame, text=t["del_btn"], width=160, height=42,
            fg_color="#B7094C", hover_color="#C9184A", text_color=c["TEXT_MAIN"],
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            command=lambda: self.delete_part(name)
        )
        del_btn.grid(row=0, column=1, padx=10)

    def delete_part(self, name):
        if name in self.saved_parts:
            del self.saved_parts[name]
            self.save_data()
            self.refresh_sidebar_parts()
            self.show_home()


if __name__ == "__main__":
    app = PrintCalculatorApp()
    app.mainloop()