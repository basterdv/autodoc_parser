import requests


def details(category_id, ssd_value, brand_value, ManufacturerId):
    # category = list(category_id.keys())
    # Group_ID = category_id[category[0]]

    try:
        url_units = f'https://catalogoriginal.autodoc.ru/api/catalogs/original/brands/{brand_value}/cars/0/quickgroups/{category_id}/units'

        myobj = {'ssd': f'{ssd_value}'} # создаем json параметры для post запроса
        r = requests.post(url_units, json=myobj)
        json_data = r.json()

        for i in json_data['items'][0]['spareParts']:
            if 'match' in i.keys():
                partNumber = i['partNumber']

        url_details_ID = f'https://webapi.autodoc.ru/api/manufacturer/{ManufacturerId}/sparepart/{partNumber}'

        r = requests.get(url_details_ID)
        json_data = r.json()

        manufacturerName = json_data['manufacturerName']
        partName = json_data['partName']
        partNumber = json_data['partNumber']
        minimalPrice = json_data['minimalPrice']
        description = json_data['description']

        return manufacturerName, partName, partNumber, minimalPrice, description

    except:
        print('Данных нет')

