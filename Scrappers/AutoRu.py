import requests
import csv

# Заголовки страницы
HEADERS = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
    'Connection': 'keep-alive',
    'Content-Length': '137',
    'content-type': 'application/json',
    'Cookie': '_csrf_token=1c0ed592ec162073ac34d79ce511f0e50d195f763abd8c24; autoru_sid=a%3Ag5e3b198b299o5jhpv6nlk0ro4daqbpf.fa3630dbc880ea80147c661111fb3270%7C1580931467355.604800.8HnYnADZ6dSuzP1gctE0Fw.cd59AHgDSjoJxSYHCHfDUoj-f2orbR5pKj6U0ddu1G4; autoruuid=g5e3b198b299o5jhpv6nlk0ro4daqbpf.fa3630dbc880ea80147c661111fb3270; suid=48a075680eac323f3f9ad5304157467a.bc50c5bde34519f174ccdba0bd791787; from_lifetime=1580933172327; from=yandex; X-Vertis-DC=myt; crookie=bp+bI7U7P7sm6q0mpUwAgWZrbzx3jePMKp8OPHqMwu9FdPseXCTs3bUqyAjp1fRRTDJ9Z5RZEdQLKToDLIpc7dWxb90=; cmtchd=MTU4MDkzMTQ3MjU0NQ==; yandexuid=1758388111580931457; bltsr=1; navigation_promo_seen-recalls=true',
    'Host': 'auto.ru',
    'origin': 'https://auto.ru',
    'Referer': 'https://auto.ru/ryazan/cars/mercedes/all/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0',
    'x-client-app-version': '202002.03.092255',
    'x-client-date': '1580933207763',
    'x-csrf-token': '1c0ed592ec162073ac34d79ce511f0e50d195f763abd8c24',
    'x-page-request-id': '60142cd4f0c0edf51f96fd0134c6f02a',
    'x-requested-with': 'fetch'
}

# URL на который будет отправлен запрос
URL = 'https://auto.ru/-/ajax/desktop/listing/'

# Параметры запроса
PARAMS = {
    # 'catalog_filter': [{"mark": "VAZ"}],
    'section': "all",
    'category': "cars",
    'sort': "fresh_relevance_1-desc",
}


def parse_page(page):
    PARAMS['page'] = page

    response = requests.post(URL, json=PARAMS,
                             headers=HEADERS)  # Делаем post запрос на url
    data = response.json()[
        'offers']  # Переменная data хранит полученные объявления

    img_url = []  # Словарь в котором будут все картинки

    i = 0  # Переменная для перехода по объявлениям
    while i <= len(
            data) - 1:  # len(data)-1 это количество пришедших объявлений

        # Доступность объявления
        try:
            Availability = str(data[i]['availability'])
        except:
            License_plate = 'Not availability'

        # Категория автомобиля
        try:
            Category = str(data[i]['category'])
        except:
            Category = 'Not category'

        # Цвет автомобиля (возвращается в формате hex)
        try:
            Color_hex = str(data[i]['color_hex'])
        except:
            Color_hex = 'Not color'

        # Описание автомобиля
        try:
            Description = str(data[i]['description'])
        except:
            Description = 'Not description'

        # Растаможен ли автомобиль (возвращает True или False)
        try:
            Custom_cleared = str(data[i]['documents']['custom_cleared'])
        except:
            Custom_cleared = 'Not custom cleared'

        # Лицензия на автомобиль
        try:
            License_plate = str(data[i]['documents']['license_plate'])
        except:
            License_plate = 'Not license plate '

        # Колличество владельцев автомобиля
        try:
            Owners_number = str(data[i]['documents']['owners_number'])
        except:
            Owners_number = 'The number of owners is not specified'

        # PTS автомобиля
        try:
            PTS = str(data[i]['documents']['pts'])
        except:
            PTS = 'Not PTS'

        # VIN автомобиля
        try:
            VIN = str(data[i]['documents']['vin'])
        except:
            VIN = 'Not VIN'

        try:
            Vin_resolution = str(data[i]['documents']['vin_resolution'])
        except:
            Vin_resolution = 'Not vin resolution '

        # Год выпуска автомобиля
        try:
            Year = str(data[i]['documents']['year'])
        except:
            Year = 'Not year'

        # Цена в рублях, евро и долларах
        try:
            Price_rub = str(data[i]['price_info']['RUR']) + '₽'
        except:
            Price_rub = 'Not price rub'

        try:
            Price_eur = str(data[i]['price_info']['EUR']) + '€'
        except:
            Price_eur = 'Not price eur'

        try:
            Price_usd = str(data[i]['price_info']['USD']) + '$'
        except:
            Price_usd = 'Not price usd'

        # С салона ли машина или нет
        try:
            Salon = str(data[i]['salon']['is_official'])
        except:
            Salon = 'Not salon'

        # Координаты места нахождения машины (возвращается долгота и широта)
        try:
            Seller = 'Координаты: ' + str(
                data[i]['seller']['location']['coord'][
                    'latitude']) + ':' + str(
                data[i]['seller']['location']['coord']['longitude'])
        except:
            Seller = 'Not seller'

        # Регион, в котором находится автомобиль
        try:
            Region = 'Регион: ' + str(
                data[i]['seller']['location']['region_info']['name'])
        except:
            Region = 'Not region'

        # Временная зона в которой находится автомобиль
        try:
            Timezone = 'Временная зона: ' + str(
                data[i]['seller']['location']['timezone_info']['abbr'])
        except:
            Timezone = 'Not timezone'

        # Пробег автомобиля
        try:
            Mileage = 'Пробег: ' + str(data[i]['state']['mileage'])
        except:
            Mileage = 'Not mileage'

        # Картинки автомобиля
        # Возвращается несколько фото, мы их добавляем в словарь img_url
        for img in data[i]['state']['image_urls']:
            img_url.append(img['sizes']['1200x900'])

        # Тип автомобиля
        try:
            Tip_auto = 'Тип автомобиля: ' + str(
                data[i]['vehicle_info']['configuration']['body_type'])
        except:
            Tip_auto = 'Not tip auto'

        # Количество дверей у автомобиля
        try:
            Count_doors = 'Колличество дверей: ' + str(
                data[i]['vehicle_info']['configuration']['doors_count'])
        except:
            Count_doors = 'Not count doors'

        # Класс автомобиля
        try:
            Class_auto = 'Класс автомобиля: ' + str(
                data[i]['vehicle_info']['configuration']['auto_class'])
        except:
            Class_auto = 'Not class auto'

        # Название автомобиля
        try:
            Name_auto = 'Имя автомобиля: ' + str(
                data[i]['vehicle_info']['configuration']['human_name'])
        except:
            Name_auto = 'Not name auto'

        # Объем багажника автомобиля
        try:
            trunk_volume_min = 'Объем багажника: ' + str(
                data[i]['vehicle_info']['configuration']['trunk_volume_min'])
        except:
            trunk_volume_min = 'Not trunk volume min'

        # Марка автомобиля
        try:
            Marka_info = 'Марка автомобиля: ' + str(
                data[i]['vehicle_info']['mark_info']['name'])
        except:
            Marka_info = 'Not marka info'

        # Модель автомобиля
        try:
            Model_info = 'Модель автомобиля: ' + str(
                data[i]['vehicle_info']['model_info']['name'])
        except:
            Model_info = 'Not model info'

        # Информация об автомобиле
        try:
            Ik_summary = 'Информация: ' + str(data[i]['lk_summary'])
        except:
            Ik_summary = 'Not ik summary'

        link_img = ''  # Переменная для ссылок
        for link_img_0 in img_url:  # Перебираем ссылки из словаря img_url, и записываем их в одну переменную текстом
            link_img += str(link_img_0) + '\n'

        with open('autoRu.csv', 'a') as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerow((License_plate, Availability, Category, Color_hex,
                             Description, Owners_number, PTS, VIN,
                             Vin_resolution, Year, Price_rub, Price_usd, Salon,
                             Seller, Region, Timezone, Mileage, Tip_auto,
                             Count_doors, Class_auto, Name_auto,
                             trunk_volume_min, Marka_info, Model_info,
                             Ik_summary, link_img
                             ))
            print('CSV written')

        i += 1  # Увеличиваем переменную перехода по объявлениям на 1

    return len(data)

def main():
    number_of_parsed = 0

    with open('autoRu.csv', 'w') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(
            ['License_plate', 'Availability', 'Category', 'Color_hex',
             'Description', 'Owners_number', 'PTS', 'VIN',
             'Vin_resolution', 'Year', 'Price_rub', 'Price_usd', 'Salon',
             'Seller_coordinates', 'Region', 'Timezone', 'Mileage',
             'Type_auto', 'Count_doors', 'Class_auto', 'Name_auto',
             'Trunk_volume', 'Marka_info', 'Model_info', 'Ik_summary',
             'Link_img'
             ])

    for page in range(0, 100):
        number_of_parsed += parse_page(page)
        print('Page: ' + str(page))

    print('Successfully parsed: ')
    print(number_of_parsed)


if __name__ == '__main__':
    main()
