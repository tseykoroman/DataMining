import requests
from urllib.parse import urljoin
import bs4
import pymongo
from requests.exceptions import HTTPError
import datetime as dt
from itertools import repeat

MONTHS = {
    "янв": 1,
    "фев": 2,
    "мар": 3,
    "апр": 4,
    "май": 5,
    "мая": 5,
    "июн": 6,
    "июл": 7,
    "авг": 8,
    "сен": 9,
    "окт": 10,
    "ноя": 11,
    "дек": 12,
}


class MagnitParse:
    def __init__(self, start_url, db_client):
        self.start_url = start_url
        db = db_client["gb_data_mining_29_03_21"]
        self.collection = db["magnit"]

    def _get_response(self, url, *args, **kwargs):
        try:
            response = requests.get(url, *args, **kwargs)
            response.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'Other error occurred: {err}')
        else:
            return response

    def _get_soup(self, url, *args, **kwargs):
        try:
            return bs4.BeautifulSoup(self._get_response(url, *args, **kwargs).text, "lxml")
        except Exception as err:
            print(f'Error occurred: {err}')


    def run(self):
        for product in self._parse(self.start_url):
            self._save(product)

    @property
    def _template(self):
        return {
            "url": lambda tag: urljoin(self.start_url, tag.attrs.get("href", "")),
            "promo_name": lambda tag: tag.find("div", attrs={"class": "card-sale__header"}).text,
            "product_name": lambda tag: tag.find("div", attrs={"class": "card-sale__title"}).text,
            "old_price": lambda tag: float(
                ".".join(
                        itm for itm in tag.find("div", attrs={"class": "label__price_old"}).text.split()
                )
            ),
            "new_price": lambda tag: float(
                ".".join(
                    itm for itm in tag.find("div", attrs={"class": "label__price_new"}).text.split()
                )
            ),
            "image_url": lambda tag: urljoin(self.start_url, tag.find("img")['data-src']),
            "date_from": lambda a: self.__get_date(
                a.find("div", attrs={"class": "card-sale__date"}).text
            )[0],
            "date_to": lambda a: self.__get_date(
                a.find("div", attrs={"class": "card-sale__date"}).text
            )[1]
        }

    def __get_date(self, date_string) -> list:
        date_list = date_string.replace("с ", "", 1).replace("\n", "").split("до") if "Только" not in date_string \
            else [x for item in [date_string.replace("Только ", "", 1)] for x in repeat(item, 2)]
        result = []
        for date in date_list:
            temp_date = date.split()
            result.append(
                dt.datetime(
                    year=dt.datetime.now().year,
                    day=int(temp_date[0]),
                    month=MONTHS[temp_date[1][:3]],
                )
            )
        return result

    def _parse(self, url):
        soup = self._get_soup(url)
        catalog_main = soup.find("div", attrs={"class": "сatalogue__main"})
        product_tags = catalog_main.find_all("a", recursive=False)
        for product_tag in product_tags:
            product = {}
            for key, funk in self._template.items():
                try:
                    product[key] = funk(product_tag)
                except (AttributeError, IndexError, ValueError):
                    product[key] = None
            yield product

    def _save(self, data):
        self.collection.insert_one(data)


if __name__ == "__main__":
    url = "https://magnit.ru/promo/?geo=moskva"
    db_client = pymongo.MongoClient("mongodb://localhost:27017")
    parser = MagnitParse(url, db_client)
    parser.run()
