import scrapy

from hh_parse.loaders import HHLoader, HHEmployerLoader
from hh_parse.spiders.xpaths import HH_PAGE_XPATH, HH_VACANCY_XPATH, HH_EMPLOYER_XPATH


class HhSpider(scrapy.Spider):
    name = "hh"
    allowed_domains = ["hh.ru"]
    start_urls = [
        "https://hh.ru/search/vacancy?schedule=remote&L_profession_id=0&area=113"
    ]

    def _get_follow_xpath(self, response, xpath, callback):
        for url in response.xpath(xpath):
            yield response.follow(url, callback=callback)

    def parse(self, response):
        callbacks = {"pagination": self.parse, "vacancy": self.vacancy_parse}

        for key, xpath in HH_PAGE_XPATH.items():
            yield from self._get_follow_xpath(response, xpath, callbacks[key])

    def vacancy_parse(self, response):
        loader = HHLoader(response=response)
        loader.add_value("url", response.url)
        for key, xpath in HH_VACANCY_XPATH.items():
            loader.add_xpath(key, xpath)

        yield loader.load_item()
        yield from self._get_follow_xpath(response, HH_VACANCY_XPATH["author"], self.employer_parse)

    def employer_parse(self, response):
        loader = HHEmployerLoader(response=response)
        loader.add_value("url", response.url)
        for key, xpath in HH_EMPLOYER_XPATH.items():
            loader.add_xpath(key, xpath)

        yield loader.load_item()
        if response.xpath(xpath):
            yield from self._get_follow_xpath(response, HH_EMPLOYER_XPATH["vacancies"], self.parse)
        #TODO custom employer template