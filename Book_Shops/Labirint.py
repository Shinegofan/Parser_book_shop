import requests
from bs4 import BeautifulSoup
import csv
from model import Book

class Labirint:
    def __init__(self,name):
        self.name=name

    def parser_labirint(self, page: int):
        url = f"https://www.labirint.ru/search/{self.name}/?stype=0&page={page}"
        list_books = []
        headers = {"User-Agent": "Chrome/134.0.6998.179"}
        r = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(r.text, "lxml")
        product_cards = soup.find_all("div", class_="product-card")
        for product_card in product_cards:
            if product_card:
                try:
                    # Название книги
                    title = product_card.get("data-name", "Название не указано")

                    # Автор книги
                    author_tag = product_card.find("div", class_="product-card__author")
                    author = author_tag.text.strip() if author_tag else "Автор не указан"

                    # Издательство
                    pubhouse_tag = product_card.find("div", class_="product-card__info").find("a", title=True)
                    pubhouse = pubhouse_tag.text.strip() if pubhouse_tag else "Издательство не указано"

                    # Цена со скидкой
                    discount_price = product_card.get("data-discount-price", "Цена не указана")
                    price = f"{discount_price} ₽" if discount_price != "Цена не указана" else "Цена не указана"

                    # Ссылка на книгу
                    link_tag = product_card.find("a", class_="product-card__name")
                    link = f"https://www.labirint.ru{link_tag['href']}" if link_tag and 'href' in link_tag.attrs else "Ссылка не указана"
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
        script_tags = soup.find_all("script")
        for script in script_tags:
            if "var count_pages" in script.text:
                try:
                    total_pages = int(script.text.split("var count_pages = ")[1].split(";")[0])
                    return total_pages
                except Exception as e:
                    print(f"Ошибка при определении количества страниц: {e}")
                    return 1
        return 1

    def full_labirint(self):
        full_list_books=[]
        url = f"https://www.labirint.ru/search/{self.name}/?stype=0"
        headers = {"User-Agent": "Chrome/134.0.6998.179"}
        r = requests.get(url=url, headers=headers)
        print(r.status_code)
        soup = BeautifulSoup(r.text, "lxml")
        pages=self.get_total_pages(soup)
        for page in range(1,pages+1):
            full_list_books.extend(x for x in self.parser_labirint(page))
        return full_list_books

