HH_PAGE_XPATH = {
    #"pagination": '//div[@data-qa="pager-block"]//a[@data-qa="pager-page"]/@href',
    "pagination": '//div[@data-qa="pager-block"]//a[@class="bloko-button"]/@href',
    "vacancy": '//div[contains(@data-qa, "vacancy-serp__vacancy")]//'
    'a[@data-qa="vacancy-serp__vacancy-title"]/@href',
}

HH_VACANCY_XPATH = {
    "title": '//h1[@data-qa="vacancy-title"]/text()',
    "salary": '//p[@class="vacancy-salary"]/span/text()',
    "description": '//div[@data-qa="vacancy-description"]//text()',
    "skills": '//div[@class="bloko-tag-list"]//'
    'div[contains(@data-qa, "skills-element")]/'
    'span[@data-qa="bloko-tag__text"]/text()',
    "author": '//a[@data-qa="vacancy-company-name"]/@href',
}


HH_EMPLOYER_XPATH = {
    "name": '//div[@class="company-header"]//span[@data-qa="company-header-title-name"]/text()',
    "site_url": '//div[@class="employer-sidebar-content"]//a[@data-qa="sidebar-company-site"]/@href',
    "profAreas": '//div[@data-qa="sidebar-header-color" and contains(text(),"Сферы деятельности")]/following-sibling::p/text()',
    "description": '//div[@class="company-description"]//div[@class="g-user-content"]//text()',
    "vacancies": '//a[@data-qa="employer-page__employer-vacancies-link"]/@href'
}
