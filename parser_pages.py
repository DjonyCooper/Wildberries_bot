import requests

size_range = []
def search_prod(article):
    prod_info = []
    url = f'https://card.wb.ru/cards/detail?spp=0&pricemarginCoeff=1.0&reg=0&appType=1&emp=0&locale=ru&lang=ru&curr=rub&couponsGeo=12,3,18,15,21&dest=-1257786&nm={article}'
    res = requests.get(url).json()
    if res['data']['products'] != []:
        prod_info.append(int(article))
        prod_info.append(res['data']['products'][0]['name'])
        if (res['data']['products'][0]['diffPrice']) == True:
            count_size = res['data']['products'][0]['sizes']
            for i in range(len(count_size)):
                size_range.append(res['data']['products'][0]['sizes'][i]['name'])
            return size_range

        if 'salePriceU'not in str(res['data']['products'][0]):
            prod_info.append(0)
        else:
            prod_info.append(str(res['data']['products'][0]['salePriceU'])[:-2])
        base_len_article = 6
        if len(article) >= base_len_article:
            add_len = len(article) - base_len_article
            value_vol = str(article)[0:1+int(add_len)]
            value_part = str(article)[0:3+int(add_len)]
            for b_num in range(1, 1000):
                b_num = '{:02}'.format(b_num)
                try:
                    url_image = f'https://basket-{b_num}.wb.ru/vol{value_vol}/part{value_part}/{article}/images/big/1.jpg'
                    resource_data = requests.get(url_image)
                    if resource_data.status_code == 200:
                        prod_info.append(url_image)
                        return prod_info
                    else:
                         pass
                except requests.ConnectionError:
                    pass
    else:
        prod_info = []
        return prod_info

def search_prod_size(size, article):
    prod_info = []
    url = f'https://card.wb.ru/cards/detail?spp=0&pricemarginCoeff=1.0&reg=0&appType=1&emp=0&locale=ru&lang=ru&curr=rub&couponsGeo=12,3,18,15,21&dest=-1257786&nm={article}'
    res = requests.get(url).json()
    if res['data']['products'] != []:
        prod_info.append(int(article))
        prod_info.append(res['data']['products'][0]['name'])
        if (res['data']['products'][0]['diffPrice']) == True:
            count_size = res['data']['products'][0]['sizes']
            size = size
            for i in range(len(count_size)):
                if (res['data']['products'][0]['sizes'][i]['name']) == size:
                    prod_info.append(res['data']['products'][0]['sizes'][i]['name'])
                    prod_info.append(str(res['data']['products'][0]['sizes'][i]['salePriceU'])[:-2])
                    base_len_article = 6
                    if len(article) > base_len_article:
                        if len(article) >= base_len_article:
                            add_len = len(article) - base_len_article
                            value_vol = str(article)[0:1 + int(add_len)]
                            value_part = str(article)[0:3 + int(add_len)]
                            for b_num in range(1, 1000):
                                b_num = '{:02}'.format(b_num)
                                try:
                                    url_image = f'https://basket-{b_num}.wb.ru/vol{value_vol}/part{value_part}/{article}/images/big/1.jpg'
                                    resource_data = requests.get(url_image)
                                    if resource_data.status_code == 200:
                                        prod_info.append(url_image)
                                        return prod_info

                                    else:
                                        pass
                                except requests.ConnectionError:
                                    pass
        else:
            prod_info = []
            return prod_info

