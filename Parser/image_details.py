import requests

def img_datail(ManufacturerId, partNumber):
    try:
        url = f'https://webapi.autodoc.ru/api/manufacturer/{ManufacturerId}/sparepart/{partNumber}'

        r = requests.get(url)

        json_data = r.json()
        img_url = json_data['galleryModel']['imgUrls']

        return img_url[0]

    except:

        return 'https://www.autodoc.ru/assets/img/no-image.png'
