import scrapy
import re
from avito_parse.loaders import AvitoAdvertismentLoader
from avito_parse.spiders.xpaths import AVITO_RUBRICS_XPATH, AVITO_PAGE_XPATH, AVITO_ADVERTISMENT_XPATH


class AvitoSpider(scrapy.Spider):
    name = "avito"
    allowed_domains = ["www.avito.ru"]
    start_urls = [
        "https://www.avito.ru/krasnodar/nedvizhimost?cd=1"
    ]

    def _get_follow_xpath(self, response, xpath, callback, rubric_url):
        if (rubric_url != None):
            p = re.compile('&p=\d*')
            rubric_url = p.sub('', rubric_url)
            for page_number in (page_number for page_number in response.xpath(xpath) if page_number.get() != "..."):
                yield response.follow(rubric_url+'&p='+page_number.get(), callback=callback)
        else:
            for url in response.xpath(xpath):
                yield response.follow(url, callback=callback)

    def parse(self, response):
        yield from self._get_follow_xpath(response, AVITO_RUBRICS_XPATH["rubrics"], self.rubric_parse, None)

    def rubric_parse(self, response):
        yield from self._get_follow_xpath(response, AVITO_PAGE_XPATH["pagination"], self.page_parse, response.url)

    def page_parse(self, response):
        callbacks = {"pagination": self.page_parse, "advertisement": self.advertisement_parse}

        for key, xpath in AVITO_PAGE_XPATH.items():
            yield from self._get_follow_xpath(response, xpath, callbacks[key], rubric_url=response.url if key == "pagination" else None)

    def advertisement_parse(self, response):
        loader = AvitoAdvertismentLoader(response=response)
        loader.add_value("url", response.url)
        for key, xpath in AVITO_ADVERTISMENT_XPATH.items():
            loader.add_xpath(key, xpath)

        yield loader.load_item()