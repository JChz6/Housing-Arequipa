import scrapy
from bookscraper.items import DepaItem


class PruebaspiderSpider(scrapy.Spider):
    name = "pruebaspider"
    allowed_domains = ["laencontre.com.pe"]
    start_urls = ["https://www.laencontre.com.pe/venta/departamentos/arequipa"]

    custom_settings = {'ITEM_PIPELINES' : {
        "bookscraper.pipelines.PruebascraperPipeline": 100,
        },
        'FEEDS': { 'depasdata.json': { 'format': 'json',
                                       'overwrite':False}}}      

    def parse(self, response):
        depas = response.css('li.serp-snippet')
        for depa in depas:
            relative_url = depa.css('h2 a').attrib['href']
            depa_url = "https://laencontre.com.pe" + relative_url
            yield scrapy.Request(depa_url, callback=self.parse_depa_page)

        #nextpage***********
        
        # Obtener el número de página actual
        current_page = int(response.url.split('_')[-1]) if '_' in response.url else 1

        # URL base y número total de páginas
        base_url = 'https://www.laencontre.com.pe/venta/departamentos/arequipa'
        total_pages = 13

        # Generar solicitudes para las páginas siguientes
        for page_num in range(current_page + 1, current_page + total_pages + 1):
            if page_num <= total_pages:
                next_page_url = f'{base_url}/p_{page_num}'
                yield response.follow(next_page_url, callback=self.parse)
            else:
                break  # Detener el crawling si se alcanza el número total de páginas


    def parse_depa_page(self, response):
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

        depa_item = DepaItem()
        depa_item['titulo'] = response.css('h1 ::text').get()
        depa_item['precio'] = response.css('div.price h2 ::text').get()
        depa_item['longitud_x'] = response.css('button.see-map').attrib['data-x']
        depa_item['latitud_y'] = response.css('button.see-map').attrib['data-y']
        depa_item['tamaño_m2'] = response.css('li.dimensions ::text').get()
        depa_item['habitaciones'] = response.css('li.bedrooms ::text').get()
        depa_item['banios'] = response.css('li.bathrooms ::text').get()
        depa_item['direccion'] = response.css('span.location_info  ::text').get()
        depa_item['descripcion'] = response.css('p.long_text  ::text').extract()
        depa_item['caracteristicas'] = response.css('ul.list ::text').extract() 
        depa_item['url'] = response.url
        yield depa_item


# precio = depa1.css('div.price::text').get()
# nombre = depa1.css('h2 a::text').get()
# URL = depa1.css('h2 a').attrib['href']    

#titulo depa = response.css('h1 ::text').get()
#preciodepa = response.css('div.price h2 ::text').get()
#tamaño = response.css('li.dimensions ::text').get()
#habitaciones = response.css('li.bedrooms ::text').get()
#baños = response.css('li.bathrooms ::text').get()
#direccion = response.css('span.location_info  ::text').get()
#descripcion = response.css('p.long_text  ::text').extract()
#caracteristicas y entorno = response.css('ul.list ::text').extract()
#longitud x = response.css('button.see-map').attrib['data-x']
#latitud y = response.css('button.see-map').attrib['data-y']
