import scrapy
from bookscraper.items import CasaItem


class CasaspiderSpider(scrapy.Spider):
    name = "casaspider"
    allowed_domains = ["www.laencontre.com.pe"]
    start_urls = ["https://www.laencontre.com.pe/venta/casas/arequipa-departamento/list"]

    custom_settings = {'ITEM_PIPELINES' : {
        "bookscraper.pipelines.CasascraperPipeline": 50,
        },
        'FEEDS': { 'casasdata.json': { 'format': 'json', 
                                      'overwrite' : False,}}}      

    def parse(self, response):
        casas = response.css('li.serp-snippet')
        for casa in casas:
            relative_url = casa.css('h2 a').attrib['href']
            casa_url = "https://www.laencontre.com.pe" + relative_url
            yield scrapy.Request(casa_url, callback=self.parse_casa_page)

        #nextpage***********
        
        # Obtener el número de página actual
        current_page = int(response.url.split('_')[-1]) if '_' in response.url else 1

        # URL base y número total de páginas
        base_url = "https://www.laencontre.com.pe/venta/casas/arequipa-departamento/list"
        total_pages = 9

        # Generar solicitudes para las páginas siguientes
        for page_num in range(current_page + 1, current_page + total_pages + 1):
            if page_num <= total_pages:
                next_page_url = f'{base_url}/p_{page_num}'
                yield response.follow(next_page_url, callback=self.parse)
            else:
                break  # Detener el crawling si se alcanza el número total de páginas


    def parse_casa_page(self, response):
        #depa = response.css('li.serp-snippet')[0]

        '''yield{
            'titulo' : response.css('h1 ::text').get(),
            'precio' : response.css('div.price h2 ::text').get(),
            'longitud_x' : response.css('button.see-map').attrib['data-x'],
            'tamaño_m2' : response.css('li.dimensions ::text').get(),
            'habitaciones' : response.css('li.bedrooms ::text').get(),
            'banios' : response.css('li.bathrooms ::text').get(),
            'direccion' : response.css('span.location_info  ::text').get(),
            'descripcion' : response.css('p.long_text  ::text').extract(),
            'caracteristicas' : response.css('ul.list ::text').extract() ,
            'url' : response.url
        }'''

        casa_item = CasaItem()
        casa_item['titulo'] = response.css('h1 ::text').get()
        casa_item['precio'] = response.css('div.price h2 ::text').get()
        casa_item['longitud_x'] = response.css('button.see-map').attrib['data-x']
        casa_item['latitud_y'] = response.css('button.see-map').attrib['data-y']
        casa_item['tamaño_m2'] = response.css('li.dimensions ::text').get()
        casa_item['habitaciones'] = response.css('li.bedrooms ::text').get()
        casa_item['banios'] = response.css('li.bathrooms ::text').get()
        casa_item['direccion'] = response.css('span.location_info  ::text').get()
        casa_item['descripcion'] = response.css('p.long_text  ::text').extract()
        casa_item['caracteristicas'] = response.css('ul.list ::text').extract() 
        casa_item['url'] = response.url

        yield casa_item
