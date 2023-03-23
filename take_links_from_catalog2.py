# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL страницы для парсинга
url = 'http://www.terrydoors.ru/catalog/'

# Получение списка всех категорий на странице
def get_categories(url):
    categories = []
    # Загрузка страницы
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    # Нахождение всех категорий
    # Находим все теги <div> с классом factory-list
    divs = soup.find_all('div', class_='categories__item')

    # Инициализируем список для хранения ссылок
    categories = []

    # Итерируемся по всем найденным тегам <div>
    for div in divs:
        # Находим все теги <a> внутри текущего тега <div>
        a_tags = div.find_all('a')
        # Извлекаем ссылки и добавляем их в список
        for a in a_tags:
            categories.append(a['href'])
    return categories

# Получение списка всех товаров в каждой категории
def get_products(category_url):
    products = []
    # Загрузка страницы
    response = requests.get(category_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    # Нахождение всех товаров
    products_tags = soup.find_all('a', class_='product-link')
    for product in products_tags:
        products.append(product.get('href'))
    return products

# Получение данных для каждого товара
def get_product_data(product_url):
    # Загрузка страницы
    response = requests.get(product_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    # Нахождение необходимых данных
    data_1 = soup.find('div', class_='data-1').text.strip()
    data_2 = soup.find('div', class_='data-2').text.strip()
    data_3 = soup.find('div', class_='data-3').text.strip()
    data_4 = soup.find('div', class_='data-4').text.strip()
    data_5 = soup.find('div', class_='data-5').text.strip()
    return [data_1, data_2, data_3, data_4, data_5]

# Запись данных в Excel-документ
def write_to_excel(data):
    df = pd.DataFrame(data, columns=['Data 1', 'Data 2', 'Data 3', 'Data 4', 'Data 5'])
    df.to_excel('output.xlsx', index=False)


    
def main():
    # Запуск парсера

    # categories = get_categories(url)
    # print('categories:',len(categories))
    # print(categories)
    # Проходим по каждой категории
    products_data = []
    categories = ["http://www.terrydoors.ru/catalog/"]
    for category in categories:
        # page_num = 0

        # Формируем URL страницы категории с порядковым номером страницы
        
        # url = "https://www.ferroni-doors.ru"
        # category_url = f'{url}{category}'#?page={page_num}
        print('Идем на категорию',category)
        # response = requests.get(category_url)
        response = requests.get(category)

        

        soup = BeautifulSoup(response.text, 'html.parser')

        # Получаем список товаров на странице
        products_list = soup.find_all('div', class_='catalog-item left-out')
        print(f'Собрали всего продуктов {len(products_list)}')


        # Проходим по каждому товару
        for product in products_list:
            # Получаем ссылку на страницу товара
            product_url = product.find('a')['href']
            

            # Переходим на страницу товара
            response = requests.get(product_url)
            soup = BeautifulSoup(response.text, 'html.parser')

            # Получаем необходимые данные о товаре
            product_data = {}
            product_data['Название'] = soup.find('h1', class_='global').text.strip()
            #description2
            for li in soup.select('div.about-product-inner div'):
                # print(li.text)
                try:
                    key = li.select_one('div.about-line').text.strip()
                    # print(key)
                    value = li.select_one('div.ab-info').text.strip()
                    # print(value)
                    product_data[key] = value
                except:
                    None
            #основные цвета
            colors = soup.find_all('div', class_='color-item choise-color')
            product_data['Основные цвета'] = ''
            for i in colors:
                product_data['Основные цвета'] += i.text.strip() + '\n'
            #Дополнительные цвета
            colors_add = soup.find_all('div', class_='color-item')
            product_data['Дополнительные цвета'] = ''
            for i in colors_add:
                product_data['Дополнительные цвета'] += i.text.strip() + '\n'
            #Описание основное
            desc_main = soup.find_all('div', class_='description-text')
            product_data['Описание'] = desc_main


            
            foto_block = soup.find('div', class_='card-main-img')
            #foto_block2 = foto_block.find('img')
            product_data['Фото'] = foto_block.find('img')['src']

            # #Берем данные из хлебных крошек
            # count_breadCrumbs = 0
            product_data["Категория"] = soup.find_all('a', rel='category tag')[1].text.strip()
            product_data['Ссылка'] = product_url
            # # Добавляем данные в список
            products_data.append(product_data)

            
    # # Создаем DataFrame из списка данных и сохраняем в Excel файл
    df = pd.DataFrame(products_data)
    df.to_excel('products_data.xlsx', index=False)


if __name__ == '__main__':
    main()
        
        
        
        