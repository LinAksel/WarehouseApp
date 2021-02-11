import json

availability_values = {
    "<AVAILABILITY>\n  <CODE>200</CODE>\n  <INSTOCKVALUE>INSTOCK</INSTOCKVALUE>\n</AVAILABILITY>": ["In stock","green"],
    "<AVAILABILITY>\n  <CODE>200</CODE>\n  <INSTOCKVALUE>OUTOFSTOCK</INSTOCKVALUE>\n</AVAILABILITY>": ["Out of stock","red"],
    "<AVAILABILITY>\n  <CODE>200</CODE>\n  <INSTOCKVALUE>LESSTHAN10</INSTOCKVALUE>\n</AVAILABILITY>": ["Less than 10","yellow"]
}

def create(category, availabilities):
    available_dict = {}
    to_json = []
    for i in availabilities:
        for j in i['response']:
            id = str(j['id']).lower()
            available_dict[id] = availability_values[j['DATAPAYLOAD']]
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
