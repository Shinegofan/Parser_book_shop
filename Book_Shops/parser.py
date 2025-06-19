from book24 import Book24
from chitai_gorod import Gorod
from Labirint import Labirint
import sqlite3

class Parser:
    def __init__(self,name):
        self.name=name
    def parsing(self):
        connection = sqlite3.connect('my_database.db')
        cursor = connection.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Parser (
        title TEXT,
        author TEXT,
        pubhouse TEXT,
        price REAL,
        link TEXT

        )
        ''')
        lab=Labirint(self.name)
        gorod=Gorod(self.name)
        b24=Book24(self.name)
        lab.full_labirint()
        gorod.full_gorod()
        b24.full_book24()

