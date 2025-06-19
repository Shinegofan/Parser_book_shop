import tkinter as tk
import webbrowser
from tkinter import ttk
from parser import Parser
import customtkinter as ctk
import sqlite3

def open_link(event):
    selected_item = tree.selection()
    if selected_item:
        # Получаем данные строки
        item = tree.item(selected_item)
        link = item["values"][4]  # Ссылка находится в пятой колонке
        webbrowser.open(link)  # Открываем ссылку в браузере


def search_book():
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    cursor.execute("DELETE FROM Parser")
    connection.commit()
    query=search.get().strip()
    par = Parser(query)
    par.parsing()

    # Очистка таблицы перед новым запросом
    for row in tree.get_children():
        tree.delete(row)

    # Вывод полученных данных в таблицу
    cursor.execute("SELECT * FROM Parser")
    for item in cursor.fetchall():
        tree.insert("", "end", values=(item[0],item[1],item[2],item[3],item[4]))
    count_items()
    connection.close()

def sort_low():
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    cursor.execute("select * from Parser ORDER BY CAST(price AS REAL)")
    for row in tree.get_children():
        tree.delete(row)

    for item in cursor.fetchall():
        tree.insert("", "end", values=(item[0],item[1],item[2],item[3],item[4]))
    connection.close()

def sort_high():
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    cursor.execute("select * from Parser ORDER BY CAST(price AS REAL) DESC")
    for row in tree.get_children():
        tree.delete(row)

    for item in cursor.fetchall():
        tree.insert("", "end", values=(item[0],item[1],item[2],item[3],item[4]))
    connection.close()

def sort_price():
    global current_function
    if current_function == sort_high:
        sort_high()
        current_function = sort_low
    else:
        sort_low()
        current_function = sort_high

def count_items():
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM Parser")
    count = cursor.fetchone()[0]
    connection.close()
    label.configure(text=f"Количество записей: {count}")


current_function=None
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("dark-blue")
root= ctk.CTk()
root.title("Bookshop prices")
root.geometry("1200x700")

# === Увеличиваем шрифт в заголовках ===
style = ttk.Style()
style.configure("Treeview.Heading", font=("Arial", 16, "bold"))  # Меняется шрифт заголовков
style.configure("Treeview",
                font=("Arial", 14),       # Шрифт и размер для ячеек
                rowheight=30)

# Поисковик
search=ctk.CTkEntry(master=root,placeholder_text="Поиск")
search.pack(fill="x",anchor="ne", padx=40, pady=20)
# Количество товара
label = ctk.CTkLabel(root, text="Количество товара: --",font=("Arial", 16))
label.pack(anchor="nw",padx=40, pady=5)
# Кнопка поиска
search_btn=ctk.CTkButton(master=root,text="Поиск",command=search_book)
search_btn.pack(anchor="ne", padx=40, pady=5)

# Кнопка сортировки
sort_button=ctk.CTkButton(master=root,text="Сортировка",command=sort_price)
sort_button.pack(anchor="ne", padx=40, pady=5)

# Фрейм для таблицы и скролбара
table_frame = ctk.CTkFrame(master=root)
table_frame.pack(pady=10, fill=tk.BOTH, expand=True)
# Скролбар
scrollbar = ttk.Scrollbar(table_frame)
scrollbar.pack(side="right", fill="y")
# Таблица
columns=("title","author","pubhouse","price","link")
tree = ttk.Treeview(table_frame,columns=columns, show="headings",yscrollcommand=scrollbar.set)
tree.pack(fill="both", expand=1,padx=40, pady=10)
tree.heading("title",text="Название")
tree.column("title",minwidth=200, width=200)
tree.heading("author",text="Автор")
tree.column("author",minwidth=200, width=200)
tree.heading("pubhouse",text="Издательство")
tree.column("pubhouse",minwidth=200, width=200)
tree.heading("price",text="Цена")
tree.column("price",minwidth=200, width=200)
tree.heading("link",text="Ссылка")
tree.column("link",minwidth=200, width=200)
scrollbar.config(command=tree.yview)
tree.bind("<Double-1>", open_link)
root.mainloop()