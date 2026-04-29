import tkinter as tk
from tkinter import messagebox, ttk
import random
import json
import os

# --- Конфигурация ---
HISTORY_FILE = "quotes.json"

# Предопределенный список цитат (база данных)
DEFAULT_QUOTES = [
    {"text": "Быть или не быть, вот в чём вопрос.", "author": "Уильям Шекспир", "theme": "Философия"},
    {"text": "В человеке всё должно быть прекрасно: и лицо, и одежда, и душа, и мысли.", "author": "Антон Чехов", "theme": "Красота"},
    {"text": "Успех — это способность идти от поражения к поражению, не теряя энтузиазма.", "author": "Уинстон Черчилль", "theme": "Мотивация"},
    {"text": "Единственный способ делать великие дела — любить то, что ты делаешь.", "author": "Стив Джобс", "theme": "Работа"},
    {"text": "Счастье — это не цель, а побочный продукт.", "author": "Элеонора Рузвельт", "theme": "Счастье"}
]

class QuoteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Генератор случайных цитат")
        self.root.geometry("600x500")
        
        # Загружаем историю из файла или создаем пустой список
        self.history = self.load_history()
        # Общий список для генерации (история + база)
        self.all_quotes = self.history + DEFAULT_QUOTES

        # --- Основной фрейм для цитаты ---
        main_frame = tk.Frame(self.root)
        main_frame.pack(pady=10)

        self.quote_label = tk.Label(
            main_frame,
            text="Нажмите кнопку для генерации цитаты",
            wraplength=450,
            font=('Arial', 12),
            justify="center"
        )
        self.quote_label.pack(pady=10)

        self.generate_btn = tk.Button(
            main_frame,
            text="Сгенерировать цитату",
            command=self.generate_quote,
            font=('Arial', 10, 'bold')
        )
        self.generate_btn.pack(pady=5)

        # --- Фрейм для фильтров ---
        filter_frame = tk.LabelFrame(self.root, text="Фильтрация", padx=10, pady=10)
        filter_frame.pack(pady=10, fill="x", padx=20)

        # Переменные для хранения значений фильтров
        self.author_var = tk.StringVar()
        self.theme_var = tk.StringVar()

        ttk.Label(filter_frame, text="Автор:").grid(row=0, column=0, sticky="e")
        self.author_entry = ttk.Entry(filter_frame, textvariable=self.author_var, width=30)
        self.author_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(filter_frame, text="Тема:").grid(row=1, column=0, sticky="e")
        self.theme_entry = ttk.Entry(filter_frame, textvariable=self.theme_var, width=30)
        self.theme_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(filter_frame, text="Применить фильтр", command=self.apply_filter).grid(row=2, column=0, columnspan=2, pady=10)

        # --- Фрейм для истории ---
        history_frame = tk.LabelFrame(self.root, text="История сгенерированных цитат", padx=10, pady=10)
        history_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.history_listbox = tk.Listbox(
            history_frame,
            width=75,
            height=12,
            font=('Arial', 10),
            activestyle="none"
        )
        self.history_listbox.pack(side="left", fill="both", expand=True)

        # Полоса прокрутки для списка истории
        scrollbar = ttk.Scrollbar(history_frame, command=self.history_listbox.yview)
        scrollbar.pack(side="right", fill="y")
        
        self.history_listbox.config(yscrollcommand=scrollbar.set)
        
        # Заполняем список истории при запуске
        self.update_history_list()

    def generate_quote(self):
        """Генерирует случайную цитату из общего списка."""
        if not self.all_quotes:
            messagebox.showwarning("Ошибка", "Список цитат пуст. Невозможно сгенерировать.")
            return

        quote = random.choice(self.all_quotes)
        
        # Формируем текст для отображения
        display_text = f'"{quote["text"]}"\n— {quote["author"]} ({quote["theme"]})'
        
        self.quote_label.config(text=display_text)
        
        # Добавляем в историю только если её там еще нет (уникальность по тексту и автору)
        is_duplicate = any(
            q["text"] == quote["text"] and q["author"] == quote["author"]
            for q in self.history
        )
        
        if not is_duplicate:
            self.history.append(quote)
            self.save_history()
            self.update_history_list()

    def apply_filter(self):
        """Применяет фильтры по автору и теме к общему списку."""
        author_filter = self.author_var.get().strip().lower()
        theme_filter = self.theme_var.get().strip().lower()
        
        filtered_quotes = []
        
        for quote in self.all_quotes:
            author_match = (author_filter == "" or author_filter in quote["author"].lower())
            theme_match = (theme_filter == "" or theme_filter in quote["theme"].lower())
            
            if author_match and theme_match:
                filtered_quotes.append(quote)
        
        if not filtered_quotes:
            messagebox.showinfo("Фильтр", "По вашему запросу ничего не найдено.")
            return

        quote = random.choice(filtered_quotes)
        
         # Формируем текст для отображения
        display_text = f'"{quote["text"]}"\n— {quote["author"]} ({quote["theme"]})'
        
        self.quote_label.config(text=display_text)
        
        # Добавляем в историю (проверка на дубликат)
        is_duplicate = any(
            q["text"] == quote["text"] and q["author"] == quote["author"]
            for q in self.history
        )
        
        if not is_duplicate:
            self.history.append(quote)
            self.save_history()
            self.update_history_list()


    def load_history(self):
         """Загружает историю из файла JSON. Возвращает пустой список при ошибке."""
         if os.path.exists(HISTORY_FILE):
             try:
                 with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                     return json.load(f)
             except (json.JSONDecodeError, Exception) as e:
                 print(f"Ошибка при загрузке истории: {e}")
                 return []
         return []

    def save_history(self):
         """Сохраняет текущую историю в файл JSON."""
         try:
             with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
                 json.dump(self.history, f, ensure_ascii=False, indent=2)
         except Exception as e:
             messagebox.showerror("Ошибка сохранения", f"Не удалось сохранить историю:\n{str(e)}")


    def update_history_list(self):
         """Обновляет виджет Listbox данными из истории."""
         self.history_listbox.delete(0, tk.END)
         for i, quote in enumerate(self.history, 1):
             line = f'{i}. "{quote["text"]}" — {quote["author"]} ({quote["theme"]})'
             self.history_listbox.insert(tk.END, line)


if __name__ == "__main__":
     root = tk.Tk()
     app = QuoteApp(root)
     root.mainloop()
