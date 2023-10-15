import requests
import pandas as pd
import json
from Product import Product, generation_fingerprint, get_sign
import concurrent.futures

def fetch_city(city):
    sess, token, headers, cookies = None, None, None, None
    products = []
    page_namber = 1
    while True:
        if not sess:
            sess, token, headers, cookies = generation_fingerprint(cities[city])
        params = {
            'sort': 'popular',
            'category_id': 32,
            'page': page_namber,
            'count': 10,
            'token': token,
        }
        params['sign'] = get_sign(params)
        try:
            response = sess.get('https://4lapy.ru/api/goods_list_cached/', params=params, cookies=cookies,
                                headers=headers).json()

            for item in response["data"]["goods"]:
                if item["availability"] == 'В наличии':
                    products.append(Product.from_json(item, city))
            page_namber += 1
            if page_namber > int(response['data']['total_pages']) :
                break
        except Exception as e:
            print("Ошибка:", e)
            continue
    return Product.to_df(products)

cities = {
    'Москва': ('0000073738', 55.755819, 37.617644),
    'Санкт-Петербург': ('0000103664', 59.939095, 30.315868)
}
def start():
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(executor.map(fetch_city, cities))
    result = pd.concat(results)
    result.to_excel("products.xlsx", index=False)
start()