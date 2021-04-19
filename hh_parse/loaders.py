from urllib.parse import urljoin

from scrapy.loader import ItemLoader
from itemloaders.processors import MapCompose, TakeFirst


def flat_text(items):
    return "\n".join(items)


def split_text(value):
    return value.lower().split(sep=',')


def hh_user_url(user_id):
    return urljoin("https://hh.ru/", user_id)


class HHLoader(ItemLoader):
    default_item_class = dict
    url_out = TakeFirst()
    title_out = TakeFirst()
    salary_out = flat_text
    #description_in = flat_text
    description_out = flat_text
    author_in = MapCompose(hh_user_url)
    author_out = TakeFirst()

class HHEmployerLoader(ItemLoader):
    default_item_class = dict
    name_out = TakeFirst()
    site_url_out = TakeFirst()
    description_out = flat_text
    profAreas_out = MapCompose(split_text)
