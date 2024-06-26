import requests


def categiry(brand_value, ssd_value):  # Категории ТО
    try:

        url_details_TO = (f'https://catalogoriginal.autodoc.ru/api/catalogs/original/brands/{brand_value}/cars/0'
                          f'/quickgroups?ssd={ssd_value}')

        quickGroupId = {}

        t = 0
        r = requests.get(url_details_TO)
        json_data = r.json()
        for i in json_data['data'][0]['children']:
            t += 1
            dictionary = {i['name']: i['quickGroupId']}
            quickGroupId[t] = dictionary

        return quickGroupId


    except:
        print('Данных не нашлось')
