import requests


def car_data(vin):  # Данные по автомобилю из введенного номера кузова
    url = f'https://catalogoriginal.autodoc.ru/api/catalogs/original/cars/{vin}/modifications'
    response = requests.get(url=url)
    json_data = response.json()

    Ssd = json_data['commonAttributes'][1]['value']
    Brand = json_data['commonAttributes'][2]['value']
    ManufacturerId = json_data['commonAttributes'][3]['value']
    Name = json_data['commonAttributes'][6]['value']
    Date = json_data['commonAttributes'][8]['value']
    Catalog = json_data['commonAttributes'][4]['value']

    return Brand, Name, Date, Ssd, Catalog, ManufacturerId
