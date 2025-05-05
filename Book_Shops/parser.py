from book24 import Book24
from chitai_gorod import Gorod
from Labirint import Labirint

class Parser:
    def __init__(self,name):
        self.name=name
    def parsing(self):
        lab=Labirint(self.name)
        gorod=Gorod(self.name)
        b24=Book24(self.name)
        books=[]
        books.extend(x for x in lab.full_labirint())
        books.extend(x for x in gorod.full_gorod())
        books.extend(x for x in b24.full_book24())
        return books

if __name__=="__main__":
    book=input()
    parser=Parser(book)
    p=parser.parsing()
    print(p)