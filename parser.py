import requests
import re
import csv
from models import Items

class Parse:
    def __init__(self, url: str):
        self.brand_id = self.__get_id(url)

    @staticmethod
    def __get_id(url: str):
        regex = "(?<=brands/).+(?=-)"
        brand_id = re.search(regex, url)[0]
        return brand_id

    def parse(self):
        i = 1
        self.__create_csv()
        while True:
            params = {
                'appType': '1',
                'brand': f'{self.brand_id}',
                'curr': 'rub',
                'dest': '-1257786',
                'page': f'{i}',
                'sort': 'popular',
                'spp': '30',
            }
            response = requests.get('https://catalog.wb.ru/brands/a/catalog', params=params)
            info = Items.parse_obj(response.json()["data"])
            if not info.products:
                break
            self.__save_csv(info)
            i += 1

    def __create_csv(self):
        with open("data.csv", mode="w", encoding="utf-8", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(['id', 'название', 'цена', 'бренд', 'продаж', 'рейтинг', 'в наличии'])

    def __save_csv(self, items):
        with open("data.csv", mode="a", encoding="utf-8", newline="") as file:
            writer = csv.writer(file)
            for article in items.products:
                writer.writerow([article.id,
                                 article.name,
                                 article.salePriceU,
                                 article.brand,
                                 article.sale,
                                 article.rating,
                                 article.volume])

if __name__ == "__main__":
    Parse("https://www.wildberries.ru/brands/9292-a4tech").parse()
