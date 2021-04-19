AVITO_RUBRICS_XPATH = {
    "rubrics": '//div[@data-marker="rubricator"]//ul[@data-marker="rubricator/list"]//ul//a/@href'
}

AVITO_PAGE_XPATH = {
    "pagination": '//div[@data-marker="pagination-button"]//span[contains(@data-marker,"page")]//text()',
    "advertisement": '//div[@data-marker="catalog-serp"]//div[@data-marker="item"]//a[@data-marker="item-title"]/@href'
}

AVITO_ADVERTISMENT_XPATH = {
    "title": '//h1[@class="title-info-title"]//span[@class="title-info-title-text"]/text()',
    "price": '//div[@class="item-price"]//span[@class="js-item-price"]/@content',
    "address": '//div[@class="item-map-location"]//span[@class="item-address__string"]/text()',
    "parameters": '//ul[@class="item-params-list"]//li[@class="item-params-list-item"]',
    "author_url": '//div[@class="seller-info  js-seller-info "]//div[@class="seller-info-value"]//a/@href',
    "author_phone": '//a[@data-qa="vacancy-company-name"]/@href'
}