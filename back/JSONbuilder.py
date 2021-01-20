import json
import lxml
import time
import re
from bs4 import BeautifulSoup


def create(category, availabilities):
    available_dict = {}
    to_json = []
    for i in availabilities:
        for j in i['response']:
            id = str(j['id']).lower()
            available = BeautifulSoup(j['DATAPAYLOAD'], 'lxml').find('instockvalue').string
            if available == 'OUTOFSTOCK':
                available_dict[id] = ["Out of stock", "red"]
            elif available != 'INSTOCK':
                available_dict[id] = ["Less than 10", "yellow"]
            else:
                available_dict[id] = ["In stock", "green"]
    for product in category:
        name = product['name']
        id = str(product['id']).lower()
        availability = available_dict[id]
        color = product['color'][0]
        price = product['price']
        manufacturer = product['manufacturer']
        new_product = {"name": name, "availability": availability[0], "availability_color": availability[1], "color": color, "price": price, "manufacturer": manufacturer}
        to_json.append(new_product)
    return to_json
