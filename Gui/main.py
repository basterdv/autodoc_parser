from pywebio.input import *
from pywebio.output import *
from pywebio import start_server
from pywebio.session import run_js
import os

from Parser import vin_data, categorys, details_data, image_details


async def main():
    clear()

    logo_path = os.path.join('Gui/images', 'logo.jpg')
    put_image(open(logo_path, 'rb').read())

    vin = await input("Введите вин код или номер кузова(фрейм) автомобиля", type=TEXT)
    put_text('vin - %r' % vin)

    Brand, Name, Date, Ssd, Catalog, ManufacturerId = vin_data.car_data(vin=vin)
    # Table Output
    put_table([
        ['Производитель', Brand],
        ['Наименование', Name],
        ['Дата выпуска', Date],
    ])

    quickGroupId = categorys.categiry(Catalog, Ssd)

    categorys_list = []
    for i in quickGroupId:
        categorys_list = categorys_list + list(quickGroupId[i].keys())

    # Drop-down selection
    category = await select('Выберите категорию для ТО.', categorys_list)

    for i in quickGroupId:
        if list(quickGroupId[i].keys())[0] == category:
            cat_id = (list(quickGroupId[i].values())[0])

    put_text('Выбрана категория для ТО - %r' % category)

    manufacturerName, partName, partNumber, minimalPrice, description = details_data.details(cat_id, Ssd,
                                                                                             Catalog,
                                                                                             ManufacturerId)

    url_img = image_details.img_datail(ManufacturerId, partNumber)

    # Table Output
    put_table([
        ['Производитель', manufacturerName],
        ['Название запчасти', partName, put_image(url_img,  width='100')],
        ['Номер запчасти', partNumber],
        ['Минимальная цена', f'{minimalPrice} руб.'],
        ['Описание ', description]
    ])

    put_button('Новый запрос', onclick=lambda: run_js('location.reload()'))


if __name__ == '__main__':
    start_server(main, host='0.0.0.0', port=8080, debug=True)
