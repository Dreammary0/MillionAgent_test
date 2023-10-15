import pandas as pd
from hashlib import md5
from requests import Session

class Product:
    def __init__(self, id, name, brand, link, regular_price, promo_price, sale=None, city = None):
        self.id = id
        self.name = name
        self.brand = brand
        self.link = link
        self.regular_price = regular_price
        self.promo_price = promo_price
        self.sale = sale
        self.city = city

    @staticmethod
    def from_json(data, city):
        if data["price"]["basePrice"] != data["price"]["actual"]:
            sale = 'True'
        else:
            sale = 'False'
        return Product(
            id=data["id"],
            name=data["title"],
            brand=data["brand_name"],
            link=data["webpage"],
            regular_price=data["price"]["basePrice"],
            promo_price=data["price"]["actual"],
            sale=sale,
            city = city
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
            'sale': [p.sale for p in parse_list],
            'city': [p.city for p in parse_list]

        }
        return pd.DataFrame(data)

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

