from urllib.parse import urlencode
import scrapy

API_KEY = '8145da15-1f70-420e-99e7-cb1b7f7f0097'

def get_proxy_url(url):
    payload = {'api_key': API_KEY, 'url': url}
    proxy_url = 'https://proxy.scrapeops.io/v1/?' + urlencode(payload)
    return proxy_url

class AdondespiderSpider(scrapy.Spider):
    name = "adondespider"
    allowed_domains = ["www.urbania.pe"]
    start_urls = ["https://urbania.pe/buscar/venta-de-departamentos-en-arequipa"]

    def parse(self, response):
        pass
