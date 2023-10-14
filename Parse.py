import pandas as pd

class Parse:
    def __init__(self, id, name, brand, link, regular_price, promo_price, sale=None):
        self.id = id
        self.name = name
        self.brand = brand
        self.link = link
        self.regular_price = regular_price
        self.promo_price = promo_price
        self.sale = sale

    @staticmethod
    def from_json(data):
        if data["price"]["basePrice"] != data["price"]["actual"]:
            sale = 'True'
        else:
            sale = 'False'
        return Parse(
            id=data["id"],
            name=data["title"],
            brand=data["brand_name"],
            link=data["webpage"],
            regular_price=data["price"]["basePrice"],
            promo_price=data["price"]["actual"],
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
