import requests
import pandas as pd
import json
from Product import Product
import concurrent.futures
from hashlib import md5
from requests import Session

cities = {
    'Москва': ('0000073738', 55.755819, 37.617644),
    'Санкт-Петербург': ('0000103664', 59.939095, 30.315868)
}
def generation_fingerprint(city):
    sess = Session()
    cookies = {
        'selected_city_code': city[0],
    }
    headers = {
        'Host': '4lapy.ru',
        'User-Agent': 'lapy 3.0.0 (iPhone; IOS 17.0.3; Scale/3.00)',
        'Version-Build': '3.0.0',
        'Authorization': 'Basic NGxhcHltb2JpbGU6eEo5dzFRMyhy',
        'X-Apps-Build': '3.0.0',
        'X-Apps-Os': '17.0.3',
        'X-Apps-Screen': '2778x1284',
        'X-Apps-Device': 'iPhone14,3',
        'X-Apps-Location': f'lat:{city[1]},lon:{city[2]}',
        'X-Apps-Additionally': '404',
        'Connection': 'close',
    }
    token = sess.get('https://4lapy.ru/api/start/', headers=headers, cookies=cookies)
    return sess, token.json()['data']['token'], headers, cookies

def get_sign(data):
    elements = [md5(str(i).encode()).hexdigest() for i in data.values()]
    elements.sort()
    return md5(('bnbgvfcdxz' + ''.join(elements)).encode()).hexdigest()

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

def start():
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(executor.map(fetch_city, cities))
    result = pd.concat(results)
    result.to_excel("products.xlsx", index=False)
start()