import tkinter as tk
import webbrowser
from tkinter import ttk, messagebox
from parser import Parser

def open_link(event):
    selected_item = tree.selection()
    if selected_item:
        # Получаем данные строки
        item = tree.item(selected_item)
        link = item["values"][4]  # Ссылка находится в пятой колонке
        webbrowser.open(link)  # Открываем ссылку в браузере


def search_book():
    query=search.get().strip()
    par = Parser(query)
    books=par.parsing()
    # Очистка таблицы перед новым запросом
    for row in tree.get_children():
        tree.delete(row)
    # Вывод полученных данных в таблицу
    for book in books:
        tree.insert("", "end", values=(book.title,book.author,book.pubhouse,book.price,book.link))


root= tk.Tk()
root.title("Book_price")
root.geometry("1200x700")
# Поисковик
search=ttk.Entry()
search.pack(fill="x",anchor="ne", padx=40, pady=20)
# Кнопка поиска
search_btn=ttk.Button(text="Поиск",command=search_book)
search_btn.pack(anchor="ne", padx=40, pady=5)
# Фрейм для таблицы и скролбара
table_frame = ttk.Frame(root)
table_frame.pack(pady=10, fill=tk.BOTH, expand=True)
# Скролбар
scrollbar = ttk.Scrollbar(table_frame)
scrollbar.pack(side="right", fill="y")
# Таблица
columns=("title","author","pubhouse","price","link")
tree = ttk.Treeview(table_frame,columns=columns, show="headings",yscrollcommand=scrollbar.set)
tree.pack(fill="both", expand=1,padx=20, pady=10)
tree.heading("title",text="Название")
tree.heading("author",text="Автор")
tree.heading("pubhouse",text="Издательство")
tree.heading("price",text="Цена")
tree.heading("link",text="Ссылка")
scrollbar.config(command=tree.yview)
tree.bind("<Double-1>", open_link)
root.mainloop()