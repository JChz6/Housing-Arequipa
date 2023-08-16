# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import re

class BookscraperPipeline:
    def process_item(self, item, spider):
        
        adapter = ItemAdapter(item)

        #Quitar los whitespaces
        field_names = adapter.field_names()
        for field_name in field_names:
            if field_name != 'description':
                value = adapter.get(field_name)
                adapter[field_name] = value.strip()

        #Cambiar a minúsculas:
        lowercase_keys = ['category', 'product_type']
        for lowercase_key in lowercase_keys:
            value = adapter.get(lowercase_key)
            adapter[lowercase_key] = value.lower()


        #Convertir el precio a float:
        price_keys = ['price', 'price_excl_tax', 'price_incl_tax', 'tax']
        for price_key in price_keys:
            value = adapter.get(price_key)
            value = value.replace('£', '')
            adapter[price_key] = float(value)

        #Elminar el texto que sobra en Availability:
        availability_string = adapter.get('availability')
        split_string_array = availability_string.split('(') 
        if len(split_string_array) < 2:
            adapter['availability']= 0
        else:
            availability_array = split_string_array[1].split(' ')
            adapter['availability'] = int(availability_array[0])

        #Convertir los reviews a numero
        num_reviews_string = adapter.get('num_reviews')
        adapter['num_reviews'] = int(num_reviews_string)

        #Convertir las estrellas a int:
        stars_string = adapter.get('stars')
        split_stars_array = stars_string.split(' ')
        stars_text_value = split_stars_array[1].lower()
        if stars_text_value == "zero":
            adapter['stars'] = 0
        elif stars_text_value == "one":
            adapter['stars'] = 1
        elif stars_text_value == "two":
            adapter['stars'] = 2
        elif stars_text_value == "three":
            adapter['stars'] = 3
        elif stars_text_value == "four":
            adapter['stars'] = 4
        elif stars_text_value == "five":
            adapter['stars'] = 5

        return item



class PruebascraperPipeline:
    def process_item(self, item, spider):

        adapter = ItemAdapter(item)


        #Limpiar el precio y convertirlo a flotante
        precios = ['precio']
        for precio in precios:
            value = adapter.get(precio)
            if value is not None:
                adapter[precio] = float(re.sub(r'[^\d.]', '', value))

        #Limpiar el tamaño y convertirlo a flotante
        tamaños = ['tamaño_m2']
        for tamaño in tamaños:
            value = adapter.get(tamaño)
            if value is not None:
                adapter[tamaño] = float(value.replace('m2', ''))

        #Limpiar los baños y habitaciones y convertirlo a int
        habitaciones = ['habitaciones']
        for cantidad in habitaciones:
            value = adapter.get(cantidad)
            if value is not None:
                adapter[cantidad] = int(value.replace(' Habitaciones', ''))
        
        banios = ['banios']
        for num in banios:
            value = adapter.get(num)
            if value is not None:
                adapter[num] = int(value.replace(' Baños', ''))

        #Limpiar las características, quitarle los caracteres especiales y espacios
        caracteristicas = ['caracteristicas']
        
        for caract in caracteristicas:
            value = adapter.get(caract)
            if value is not None:
                cleaned_value = ''.join(value)
                cleaned_value = re.sub(r'\n\s+', ' ', cleaned_value).strip()
                adapter[caract] = cleaned_value
        
        return item
    
class CasascraperPipeline:
    def process_item(self, item, spider):

        adapter = ItemAdapter(item)


        #Limpiar el precio y convertirlo a flotante
        precios = ['precio']
        for precio in precios:
            value = adapter.get(precio)
            if value is not None:
                adapter[precio] = float(re.sub(r'[^\d.]', '', value))

        #Limpiar el tamaño y convertirlo a flotante
        tamaños = ['tamaño_m2']
        for tamaño in tamaños:
            value = adapter.get(tamaño)
            if value is not None:
                adapter[tamaño] = float(value.replace('m2', ''))

        #Limpiar los baños y habitaciones y convertirlo a int
        habitaciones = ['habitaciones']
        for cantidad in habitaciones:
            value = adapter.get(cantidad)
            if value is not None:
                adapter[cantidad] = int(value.replace(' Habitaciones', ''))
        
        banios = ['banios']
        for num in banios:
            value = adapter.get(num)
            if value is not None:
                adapter[num] = int(value.replace(' Baños', ''))

        #Limpiar las características, quitarle los caracteres especiales y espacios
        caracteristicas = ['caracteristicas']
        
        for caract in caracteristicas:
            value = adapter.get(caract)
            if value is not None:
                cleaned_value = ''.join(value)
                cleaned_value = re.sub(r'\n\s+', ' ', cleaned_value).strip()
                adapter[caract] = cleaned_value
        
        return item