from items import DrogasilItem
from math import ceil
import scrapy

class DrogasilspiderSpider(scrapy.Spider):
    name = "DrogasilSpider"
    allowed_domains = ["www.drogasil.com.br"]

    def start_requests(self):

        endpoints = ["https://www.drogasil.com.br/beleza/cuidados-com-a-pele/protetor-solar.html"]

        for endpoint in endpoints:
            yield scrapy.Request(endpoint, callback = self.parse_page, meta = {'endpoint' : endpoint,
                                                                               'page' : 1})

    def parse_page(self, response):
        page = response.meta['page']
        endpoint = response.meta['endpoint']

        product_urls = response \
            .xpath('//h2/a[starts-with(@class, "LinkNextstyles__LinkNextStyles")]/@href').getall()

        for product_url in product_urls:

            yield scrapy.Request(product_url, callback = self.parse_product)

        if page == 1:

            total_results =  int(response.xpath(
                '//*[starts-with(@class, "Found__FoundStyles")]/p/text()'
                ).get())
            number_pages = ceil(total_results / 48) # 48 itens são exibidos por página por padrão

            for page_num in range(2, number_pages):

                new_page = f"{endpoint}?p={page_num}"
                yield scrapy.Request(new_page, callback = self.parse_page, meta = {'endpoint' : endpoint,
                                                                                      'page' : page_num})

    def parse_product(self, response):
        pass