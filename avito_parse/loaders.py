from scrapy import Selector
from scrapy.loader import ItemLoader
from itemloaders.processors import MapCompose, TakeFirst


def clear_address(value):
    return value.replace('\n', '')

def get_parameter(item: str) -> dict:
    selector = Selector(text=item)
    data = {
        "name": selector.xpath(
            '//span[@class="item-params-label"]/text()'
        ).extract_first(),
        "value": selector.xpath(
            '//text()[2]'
        ).extract_first(),
    }
    return data


class AvitoAdvertismentLoader(ItemLoader):
    default_item_class = dict
    title_out = TakeFirst()
    price_out = TakeFirst()
    address_in = MapCompose(clear_address)
    address_out = TakeFirst()
    parameters_in = MapCompose(get_parameter)
    author_url_out = TakeFirst()
    #author_phone_out = TakeFirst()