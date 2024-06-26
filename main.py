import requests


def car_data(vin):  # Данные по автомобилю из введенного номера кузова
    vin_1 = 'WAUBH54B11N111054'
    vin_2 = 'FNN15-502358'
    vin_3 = 'KMHJN81BP9U044420'
    vin_4 = 'Z25A-0014596'

    url = f'https://catalogoriginal.autodoc.ru/api/catalogs/original/cars/{vin}/modifications'

    print(f'Вин номера или номер кузова автомобиля - {vin}')
    print('---------------------------------------')

    try:
        response = requests.get(url=url)
        json_data = response.json()

        Ssd = json_data['commonAttributes'][1]['value']
        Brand = json_data['commonAttributes'][2]['value']
        ManufacturerId = json_data['commonAttributes'][3]['value']
        Name = json_data['commonAttributes'][6]['value']
        Date = json_data['commonAttributes'][8]['value']
        Catalog = json_data['commonAttributes'][4]['value']

        print('Данные по автомобилю')
        print(f'Производитель - {Brand}')
        print(f'Наименование - {Name}')
        print(f'Дата выпуска - {Date}')
        print('--------------------------------')

        return Ssd, ManufacturerId, Catalog

    except:
        print('Данные по вин номеру или номеру кузова не найдены')


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
            dictionary = {}
            print(t, '-', i['name'])
            dictionary[i['name']] = i['quickGroupId']
            quickGroupId[t] = dictionary

        category_id = int(input('Выберите категорию запчасти для ТО - '))

        return quickGroupId[category_id]

    except:
        print('Данных не нашлось')


def details(category_id, ssd_value, brand_value, ManufacturerId):
    print('-------------------')
    category = list(category_id.keys())
    Group_ID = category_id[category[0]]
    print(f'Выбранна группа - {category[0]}')
    print('------------------')

    try:
        url_units = f'https://catalogoriginal.autodoc.ru/api/catalogs/original/brands/{brand_value}/cars/0/quickgroups/{Group_ID}/units'
        # 'https://catalogoriginal.autodoc.ru/api/catalogs/original/brands/AU1519/cars/0/quickgroups/2/units'

        myobj = {'ssd': f'{ssd_value}'}
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

        print(f'Производитель - {manufacturerName}')
        print(f'Название запчасти - {partName}')
        print(f'Номер запчасти - {partNumber}')
        print(f'Минимальная цена - {minimalPrice}')
        print(f'Описание - {description}')

    except:
        print('Данных нет')


def get_data():
    vin = input('Введите вин код: ')
    ssd_value, ManufacturerId, brand_value = car_data(vin=vin)

    print('Запчасти для ТО')
    print('---------------------------')
    category_id = categiry(brand_value, ssd_value)
    details(category_id, ssd_value, brand_value, ManufacturerId)


def main():
    get_data()


if __name__ == '__main__':
    main()
