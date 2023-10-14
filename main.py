import requests
import pandas as pd
import json


class Parse:
    def __init__(self, id, name, brand, link, regular_price, promo_price, sale = None):
        self.id = id
        self.name = name
        self.brand = brand
        self.link = link
        self.regular_price = regular_price
        self.promo_price = promo_price
        self.sale = sale
    @staticmethod
    def from_json(data):
        if data["price"]["basePrice"] != data["price"]["subscribe"]:
            sale = 'True'
        else:
            sale = 'False'
        return Parse(
            id=data["id"],
            name=data["title"],
            brand=data["brand_name"],
            link=data["webpage"],
            regular_price=data["price"]["basePrice"],
            promo_price=data["price"]["subscribe"],
            sale=sale
        )
    @staticmethod
    def to_df(parse_list):
        data = {
            'id': [p.id for p in parse_list],
            'name': [p.name for p in parse_list],
            'brand': [p.brand for p in parse_list],
            'link': [p.link for p in parse_list],
            'regular_price': [p.regular_price for p in parse_list],
            'promo_price': [p.promo_price for p in parse_list],
            'sale': [p.sale for p in parse_list]
        }
        return pd.DataFrame(data)

data = {'data': [], 'error': []}
productList = []
page_number = 1
while True:
    # URL для получения данных из API мобильного приложения
    url = f"https://4lapy.ru/api/goods_list_cached/?category_id=32&count=10&page={page_number}&sign=a793d334aa5bf059b73f1c18c2db20f7&sort=popular&token=7998cc7b5a58d8583214cc17a4a247a7"
    print(page_number, end=" ")
    try:
        response = requests.get(url)
        data = response.json()
        if "error" in data and data["error"] != []:
            break
        page_number += 1
        # Создаем список словарей с необходимыми данными
        for item in data["data"]["goods"]:
            if "availability" in item and item["availability"] == 'В наличии':
                if "price" in item and "basePrice" in item["price"] and "subscribe" in item["price"]:
                    productList.append(Parse.from_json(item))
    except Exception as e:
        print("Ошибка:", e)
        continue


df = Parse.to_df(productList)
df.to_excel("products.xlsx", index=False)
