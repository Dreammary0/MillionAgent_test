import requests
import pandas as pd
import json

data = {'data': [], 'error': []}
products = []
page_number = 1
while True:
    # URL для получения данных из API мобильного приложения
    url = f"https://4lapy.ru/api/goods_list_cached/?category_id=32&count=10&page={page_number}&sign=a793d334aa5bf059b73f1c18c2db20f7&sort=popular&token=7998cc7b5a58d8583214cc17a4a247a7"
    print(page_number, end=" " )
    response = requests.get(url)
    data = response.content.decode("cp1251")  # указываем правильную кодировку
    data = json.loads(data)
    if data['error'] != []:
        break
    page_number += 1
    # Создаем список словарей с необходимыми данными
    for item in data["data"]["goods"]:
        if item["availability"] == 'В наличии':
            if item["price"]["basePrice"] != item["price"]["subscribe"]:
              sale = 'True'
            else:
                sale = 'False'
            product = {
                "id": item["id"],
                "name": item["title"],
                "brand": item["brand_name"],
                "link": item["webpage"],
                "regular_price": item["price"]["basePrice"],
                "promo_price": item["price"]["subscribe"],
                "sale": sale
            }
            products.append(product)

# Создаем DataFrame из списка словарей и выгружаем в XLSX формат
df = pd.DataFrame(products)
df.to_excel("products.xlsx", index=False)

