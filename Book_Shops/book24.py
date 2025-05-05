import requests
from bs4 import BeautifulSoup
from model import Book
import re

class Book24:
    def __init__(self,name):
        self.name=name
    def parser_book24(self,page:int):
        url = f"https://book24.ru/search/page-{page}/?q={self.name}"
        list_books = []
        headers = {"User-Agent": "Chrome/134.0.6998.179"}
        r = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(r.text, "lxml")
        product_cards = soup.find_all("article", class_="product-card")
        for product_card in product_cards:
            if product_card:
                try:
                    # Название книги
                    title = product_card.get("data-b24-name", "Название не указано")
                    # Автор книги
                    author_tag = product_card.find("a", class_="author-list__item")
                    author = author_tag.text.strip() if author_tag else "Автор не указан"
                    # Издательство
                    pubhouse = product_card.get("data-b24-brand", "Издательство не указано")
                    # Цена со скидкой
                    price = product_card.get("data-b24-price", "Цена не указана")
                    # Ссылка на книгу
                    link_tag = product_card.find("a", class_="product-card__name")
                    link = f"https://book24.ru{link_tag['href']}" if link_tag and 'href' in link_tag.attrs else "Ссылка не указана"
                    list_books.append(Book(title=title,
                                           author=author,
                                           pubhouse=pubhouse,
                                           price=price,
                                           link=link))
                except Exception as e:
                    print(f"Ошибка при парсинге: {e}")
            else:
                print("Карточка товара не найдена.")
        return list_books

    def get_total_pages(self,soup):
        desc_div = soup.find("div", class_="search-page__desc")
        total_products=0
        if desc_div:
            # Извлекаем текст элемента
            desc_text = desc_div.text.strip()

            # Используем регулярное выражение для поиска числа
            match = re.search(r"найдено (\d+) това", desc_text)
            if match:
                total_products = int(match.group(1))
            else:
                print("Количество товаров не найдено.")
                return 1
        else:
            print("Описание не найдено.")
            return 1
        pages=total_products//30
        if total_products%30!=0 or pages==0:
            pages+=1
        return pages

    def full_book24(self):
        full_list_books = []
        url = f"https://book24.ru/search/?q={self.name}"
        headers = {"User-Agent": "Chrome/134.0.6998.179"}
        r = requests.get(url=url, headers=headers)
        print(r.status_code)
        soup = BeautifulSoup(r.text, "lxml")
        pages = self.get_total_pages(soup)
        for page in range(1, pages + 1):
            full_list_books.extend(x for x in self.parser_book24(page))
        return full_list_books

