# -*- coding: utf-8 -*-
import scrapy


class OlxSpider(scrapy.Spider):
    name = 'OLX'
    #allowed_domains = ['https://sc.olx.com.br/esportes-e-lazer']
    start_urls = ['https://sc.olx.com.br/esportes-e-lazer/']

    def parse(self, response):
       items = response.xpath(
           '//ul[@id="main-ad-list"]/li[not(contains(@class, "item yap-loaded")) '
           'and not(contains(@class, "item list_native"))]'
       )

       for item in items:
           url = item.xpath('./a/@href').extract_first()
           yield scrapy.Request(url=url, callback=self.parse_detail)

       next_page = response.xpath('//div[contains(@class, "module_pagination")]//a[@rel="next"]/@href')
       if next_page:
           yield  scrapy.Request(
               url=next_page.extract_first(), callback=self.parse
               )

    def parse_detail(self, response):
        title = response.xpath('//h1[@id="ad_title"]').extract_first()
        price = response.xpath('//span[@class="actual-price"]').extract_first()
        description = response.xpath('//div[@class="OLXad-description mb30px"]/p').extract_first()
        yield{
            'titulo': title,
            'preco': price,
            'descricao': description,
            }
    