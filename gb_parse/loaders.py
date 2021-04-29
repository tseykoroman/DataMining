import re
from scrapy import Selector
from scrapy.loader import ItemLoader

from itemloaders.processors import TakeFirst, MapCompose


def get_specifications(itm):
    tag = Selector(text=itm)
    return {tag.xpath('//div[contains(@class, "AdvertSpecs_label")]/text()').get():
                tag.xpath('//div[contains(@class, "AdvertSpecs_data")]//text()').get()}


def get_specifications_out(data):
    result = {}
    for itm in data:
        result.update(itm)
    return result


def js_decoder_autor(text):
    re_str = re.compile(r'youlaId%22%2C%22([0-9|a-zA-Z]+)%22%2C%22avatar')
    result = re.findall(re_str, text)
    return f'https://youla.ru/user/{result[0]}' if result else None

