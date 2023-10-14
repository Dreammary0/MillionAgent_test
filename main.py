import pandas as pd
from Parse import Parse
# import multiprocessing
import time
import asyncio
import aiohttp

start_time = time.time()
async def process_url(session, url, page_number):
    print(page_number)
    productList = []
    try:
        async with session.get(url.format(page_number)) as resp:
            resp.raise_for_status()
            data = await resp.json()
            goods_data = data.get("data", {}).get("goods", [])
            for item in goods_data:
                if item["availability"] == 'В наличии':
                    productList.append(Parse.from_json(item))
            return productList
    except aiohttp.ClientError as e:
        print("Ошибка:", e)
        return []

async def main():
    async with aiohttp.ClientSession() as session:
        url = "https://4lapy.ru/api/goods_list_cached/?&category_id=32&count=10&page={}&sign=e16816f878c65a77949913e9510d4568&sort=popular&token=7998cc7b5a58d8583214cc17a4a247a7"
        async with session.get(url.format(1)) as resp:
            data = await resp.json()
            max_pages = data['data']['total_pages']

        tasks = []
        for page_number in range(1,max_pages+1):
            task = asyncio.create_task(process_url(session, url, page_number))
            tasks.append(task)

        results = await asyncio.gather(*tasks)
        productList = []
        for result in results:
            productList.extend(result)
        df = Parse.to_df(productList)
        df.to_excel("products.xlsx", index=False)

asyncio.run(main())
print("--- %s seconds ---" % (time.time() - start_time))




# def process_url(url, cookies):
#     productList = []
#     page_number = 1
#     while True:
#         try:
#             response = requests.get(url.format(page_number))
#             response.raise_for_status()
#             data = response.json()
#             goods_data = data.get("data", {}).get("goods", [])
#             for item in goods_data:
#                 if item["availability"] == 'В наличии':
#                     productList.append(Parse.from_json(item))
#             if page_number == data["data"]["total_pages"]:
#                 break
#             page_number += 1
#         except requests.exceptions.RequestException as e:
#             print("Ошибка:", e)
#             continue
#     return Parse.to_df(productList)
#
# def process_url_wrapper(args):
#     return process_url(*args)
#
# if __name__ == '__main__':
#     url1 = "https://4lapy.ru/api/goods_list_cached/?&category_id=32&count=10&page={}&sign=e16816f878c65a77949913e9510d4568&sort=popular&token=7998cc7b5a58d8583214cc17a4a247a7"
#     url2 = "https://4lapy.ru/api/goods_list_cached/?category_id=32&count=10&page={}&sign=a793d334aa5bf059b73f1c18c2db20f7&sort=popular&token=7998cc7b5a58d8583214cc17a4a247a7"
#     cookies1 = {'selected_city_code': '0000073738'}
#     cookies2 = {'selected_city_code': '0000103664'}
#
#     with multiprocessing.Pool(processes=2) as pool:
#         results = pool.map(process_url_wrapper, [(url1, cookies1), (url2, cookies2)])
#
#     df1 = results[0]
#     df2 = results[1]
#     df3 = pd.merge(df1, df2, on=['id', 'name', 'brand', 'link', 'regular_price', 'promo_price', 'sale'])
#
#     df3.to_excel("products.xlsx", index=False)
#     print(len(df1), len(df2), len(df3))
#     print(df3)


