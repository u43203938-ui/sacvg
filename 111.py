import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

class WeatherDiaryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Diary")
        self.data_file = "data/weather_data.json"
        self.records = []
        self.load_data()

        # --- Интерфейс ---
        # Поля ввода
        ttk.Label(root, text="Дата (ГГГГ-ММ-ДД):").grid(row=0, column=0, padx=5, pady=5)
        self.date_entry = ttk.Entry(root)
        self.date_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(root, text="Температура (°C):").grid(row=1, column=0, padx=5, pady=5)
        self.temp_entry = ttk.Entry(root)
        self.temp_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(root, text="Описание:").grid(row=2, column=0, padx=5, pady=5)
        self.desc_entry = ttk.Entry(root)
        self.desc_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(root, text="Осадки (да/нет):").grid(row=3, column=0, padx=5, pady=5)
        self.precip_var = tk.StringVar(value="нет")
        ttk.Radiobutton(root, text="Да", variable=self.precip_var, value="да").grid(row=3, column=1)
        ttk.Radiobutton(root, text="Нет", variable=self.precip_var, value="нет").grid(row=3, column=2)

        # Кнопка добавления записи
        ttk.Button(root, text="Добавить запись", command=self.add_record).grid(row=4, column=0, columnspan=3, pady=10)

        # Таблица для отображения записей
        self.tree = ttk.Treeview(root, columns=("date", "temp", "desc", "precip"), show='headings')
        self.tree.heading("date", text="Дата")
        self.tree.heading("temp", text="Температура")
        self.tree.heading("desc", text="Описание")
        self.tree.heading("precip", text="Осадки")
        self.tree.grid(row=5, column=0, columnspan=3, padx=5, pady=5)

        # Фильтрация по дате
        ttk.Label(root, text="Фильтр по дате:").grid(row=6, column=0, padx=5, pady=5)
        self.filter_date = ttk.Entry(root)
        self.filter_date.grid(row=6, column=1, padx=5, pady=5)
        ttk.Button(root, text="Фильтровать", command=self.filter_by_date).grid(row=6, column=2, padx=5, pady=5)

        # Фильтрация по температуре
        ttk.Label(root, text="Фильтр по температуре (>):").grid(row=7, column=0, padx=5, pady=5)
        self.filter_temp = ttk.Entry(root)
        self.filter_temp.grid(row=7, column=1, padx=5, pady=5)
        ttk.Button(root, text="Фильтровать", command=self.filter_by_temp).grid(row=7, column=2, padx=5, pady=5)

    def add_record(self):
        date = self.date_entry.get()
        temp = self.temp_entry.get()
        desc = self.desc_entry.get()
        precip = self.precip_var.get()

        # Валидация ввода
        if not date or not temp or not desc:
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены!")
            return
        try:
            temp = float(temp)
            # Проверка формата даты (простейшая)
            year, month, day = map(int, date.split('-'))
            if len(date) != 10 or date[4] != '-' or date[7] != '-':
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Некорректный формат даты или температуры!")
            return

        record = {"date": date, "temp": temp, "desc": desc, "precip": precip}
        self.records.append(record)
        self.save_data()
        self.update_tree()

    def update_tree(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for rec in self.records:
            self.tree.insert("", "end", values=(rec["date"], rec["temp"], rec["desc"], rec["precip"]))

    def filter_by_date(self):
        filter_date = self.filter_date.get()
        filtered = [r for r in self.records if r["date"] == filter_date]
        for i in self.tree.get_children():
            self.tree.delete(i)
        for rec in filtered:
            self.tree.insert("", "end", values=(rec["date"], rec["temp"], rec["desc"], rec["precip"]))

    def filter_by_temp(self):
        try:
            temp_val = float(self.filter_temp.get())
            filtered = [r for r in self.records if r["temp"] > temp_val]
            for i in self.tree.get_children():
                self.tree.delete(i)
            for rec in filtered:
                self.tree.insert("", "end", values=(rec["date"], rec["temp"], rec["desc"], rec["precip"]))
        except ValueError:
            messagebox.showerror("Ошибка", "Введите число для температуры!")

    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r', encoding='utf-8') as f:
                self.records = json.load(f)

    def save_data(self):
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.records, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherDiaryApp(root)
    root.mainloop()
