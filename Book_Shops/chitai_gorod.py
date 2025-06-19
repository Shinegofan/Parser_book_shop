import requests
from bs4 import BeautifulSoup
import sqlite3

class Gorod:
    def __init__(self,name):
        self.name=name
    def parser_gorod(self,page:int):
        connection = sqlite3.connect("my_database.db")
        cursor = connection.cursor()
        url=f"https://www.chitai-gorod.ru/search?phrase={self.name}&page={page}"
        headers = {"User-Agent": "Chrome/134.0.6998.179"}
        r = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(r.text, "lxml")
        product_cards = soup.find_all("article",class_="product-card")
        for product_card in product_cards:
            if product_card:
                try:
                    # Название книги
                    title = product_card.get("data-chg-product-name", "Название не указано")
                    # Автор книги
                    author_tag = product_card.find("span", class_="product-card__subtitle")
                    author = author_tag.text.strip() if author_tag else "Автор не указан"
                    # Издательство
                    pubhouse = product_card.get("data-chg-product-brand", "Издательство не указано")
                    # Цена со скидкой
                    price = product_card.get("data-chg-product-price", "Цена не указана")
                    # Ссылка на книгу
                    link_tag = product_card.find("a", class_="product-card__title")
                    link = f"https://www.chitai-gorod.ru{link_tag['href']}" if link_tag and 'href' in link_tag.attrs else "Ссылка не указана"
                    cursor.execute(f"insert into Parser (title,author,pubhouse,price,link) VALUES (?, ?, ?, ?, ?)",(title, author, pubhouse, price, link))
                    connection.commit()
                except Exception as e:
                    print(f"Ошибка при парсинге: {e}")
            else:
                print("Карточка товара не найдена.")


    def get_total_pages(self,soup):
        pagination_list = soup.find("ul", class_="chg-app-pagination__button-list")

        if pagination_list:
            page_links = pagination_list.find_all("a", class_="chg-app-pagination__item")

            # Извлекаем текст последнего элемента
            if page_links:
                last_page_text = page_links[-1].text.strip()
                try:
                    last_page_number = int(last_page_text)
                    return last_page_number
                except ValueError:
                    print("Номер последней страницы не является числом.")
                    return 1
            else:
                print("Кнопки пагинации не найдены.")
                return 1
        else:
            print("Список пагинации не найден.")
            return 1

    def full_gorod(self):
        url=f"https://www.chitai-gorod.ru/search?phrase={self.name}"
        headers = {"User-Agent": "Chrome/134.0.6998.179"}
        r = requests.get(url=url, headers=headers)
        print(r.status_code)
        soup = BeautifulSoup(r.text, "lxml")
        pages = self.get_total_pages(soup)
        for page in range(1, pages + 1):
            self.parser_gorod(page)

