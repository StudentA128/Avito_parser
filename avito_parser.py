import time
import os
import re
import random

import requests
import bs4
import csv

from selenium import webdriver
from random import randint


# Function for downloading the page and getting all the links for renting an apartment.
# Функция для скачивание страницы и получение всех ссылок по аренде квартиры.
def get_links(url):

    # Variable for the list of links.
    # Переменная для списка ссылок.
    apartments_url_list = []

    # The path to the file with the content of the page we are downloading.
    # Путь к файлу с содержимым страницы, которую мы скачиваем.
    file_path = r"C:\Users\Alex\Desktop\NKNT\8_CEMAK\kypc\parser\avito_page.html"

    # User agent to work with the site.
    # Пользовательский агент для работы с сайтом.
    user_agent_list = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36",
    ]

    # Working with selenium. Open the desired page, then download it and write it to a file.
    # Работа с selenium. Открываем нужную страницу затем скачиваем её и записываем в файл.
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-agent={random.choice(user_agent_list)}")
    driver = webdriver.Chrome(executable_path=r"C:\Users\Alex\Desktop\NKNT\8_CEMAK\kypc\parser\chromedriver.exe", options=options)

    try:
        driver.get(url=url)
        time_for_sleep = randint(1, 2)
        time.sleep(time_for_sleep)

        with open("avito_page.html", "w", encoding="utf-8") as file:
            file.write(driver.page_source)

    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()

    # We run our file through Beautiful Soup and get a BeautifulSoup object that represents the html page as a nested data structure.
    # Прогоняем наш файл через Beautiful Soup и получаем объект BeautifulSoup, который представляет html страницу в виде вложенной структуры данных.
    with open("avito_page.html", "r", encoding="utf-8") as file:
        src = file.read()

    soup = bs4.BeautifulSoup(src, "lxml")

    # We find all the elements that contain links to renting an apartment.
    # Находим все элементы в которых содержатся ссылки на аренду квартиры.
    apartments_list = soup.find_all("div", class_="iva-item-titleStep-pdebR")
    page_apartments_url_list = []

    # We find the necessary links in the found elements and put them in the list.
    # В найденных элементах находим необходимые сслыки и помещаем их в список.
    for link in apartments_list:
        page_apartments_url_list.append((link.find('a').get('href')))

    # Remove duplicate links from the list, if any.
    # Удаляем из списка повторяющиеся ссылки, если они есть.
    page_apartments_url_list = set(page_apartments_url_list)

    # We add a domain name to the beginning of each link for the links to work correctly.
    # Добавляем в начало каждой ссылки доменное имя, для корректной работы ссылок.
    for i in page_apartments_url_list:
        buffer_str = "https://www.avito.ru" + i
        apartments_url_list.append(buffer_str)

    # Delete the file that contains the page we downloaded.
    # Удаляем файл в котором содержится скачанная нами страница.
    os.remove(file_path)

    # We return the list of links found on the page.
    # Возвращаем список ссылок найденных на странице.
    return apartments_url_list


# Function for receiving and saving information about the apartment.
# Функция для получения и сохранения информации о квартире.
def get_detailed_info(url):

    # The path to the file with the content of the page we are downloading.
    # Путь к файлу с содержимым страницы, которую мы скачиваем.
    file_path = r"C:\Users\Alex\Desktop\NKNT\8_CEMAK\kypc\parser\page_apartment.html"

    # List of headers of various information about the apartments.
    # Список заголовков различной информации о квартирах.
    about_apartment_titles = []

    # List with the necessary information about the apartments.
    # Список с необходимой информацией о квартирах.
    about_apartment_info = []

    # Headers template of various information about the apartment.
    # Шаблон заголовков различной информации о квартире.
    pattern_with_apartment_info = ["Количество комнат", "Стоимость аренды", "Залог", "Общая площадь", "Площадь кухни", 
        "Жилая площадь", "Этаж", "Ремонт", "Балкон или лоджия", "Тип комнат", "Санузел", "Мебель", "Техника", "Интернет и ТВ", 
        "Тип дома", "Этажей в доме", "Год постройки", "Пассажирский лифт", "Грузовой лифт", "Парковка", "Адрес", "Район", 
        "Количество жильцов", "Кол-во кроватей", "Можно с детьми", "Можно курить", "Можно с животными", "Дополнительно", "Описание"]

    # Line template with various information about the apartment.
    # Шаблон строки с различной информацией о квартире.
    str_with_apartment_info = ["not stated", "not stated", "not stated", "not stated", "not stated", "not stated", "not stated", 
        "not stated", "not stated", "not stated", "not stated", "not stated", "not stated", "not stated", "not stated", "not stated", 
        "not stated", "not stated", "not stated", "not stated", "not stated", "not stated", "not stated", "not stated", "not stated", 
        "not stated", "not stated", "not stated", "not stated"]


    # Templates for extracting the necessary information from a string.
    # Шаблоны для извлечения необходимой информации из строки.
    pattern_for_titles = re.compile(r'(.*?):')
    pattern_for_info = re.compile(r': (.*?)\n')
    pattern_for_building_info = re.compile(r':(.*?)\n')

    # User agent to work with the site.
    # Пользовательский агент для работы с сайтом.
    user_agent_list = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36",
    ]

    # Working with selenium. Open the desired page, then download it and write it to a file.
    # Работа с selenium. Открываем нужную страницу затем скачиваем её и записываем в файл.
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-agent={random.choice(user_agent_list)}")
    driver = webdriver.Chrome(executable_path=r"C:\Users\Alex\Desktop\NKNT\8_CEMAK\kypc\parser\chromedriver.exe", options=options)

    try:
        driver.get(url=url)
        time_for_sleep = randint(1, 2)
        time.sleep(time_for_sleep)

        with open("page_apartment.html", "w", encoding="utf-8") as file:
            file.write(driver.page_source)

    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()
    # -----------

    # We run our file through Beautiful Soup and get a BeautifulSoup object that represents the html page as a nested data structure.
    # Прогоняем наш файл через Beautiful Soup и получаем объект BeautifulSoup, который представляет html страницу в виде вложенной структуры данных.
    with open("page_apartment.html", "r", encoding="utf-8") as file:
        src = file.read()

    soup = bs4.BeautifulSoup(src, "lxml")
    # -----------

    ad_removed = soup.find("div", attrs={"data-marker": "item-view/item-params"})
    if ad_removed is None:
        ad_removed_str_er = "ad removed"
        print(ad_removed_str_er)
        return

    # Extracting all the necessary information about the apartment and creating a list with this information.
    # Извлечение всей необходимой информации о квартире и формирование списка с данной информацией.
    description_list = soup.find("div", attrs={"data-marker": "item-view/item-params"}).find_all("li")
    apartment_description_list = []

    for i in description_list:
        apartment_description_list.append(i.text.strip(" \n"))

    for i in apartment_description_list:
        str_info = pattern_for_info.findall(i + "\n")
        for n in str_info:
            about_apartment_info.append(n.strip(" ,"))

        str_titles = pattern_for_titles.findall(i + "\n")
        for n in str_titles:
            about_apartment_titles.append(n.strip(" ,"))

    price_str = soup.find(class_="js-item-price")
    if price_str is None:
        price_str = "not found"
    if type(price_str) is str:
        print("error with price_str")
        return
    price_info = price_str.text.strip(" \n")
    str_with_apartment_info[1] = price_info

    apartment_address_title = "Адрес"
    apartment_district_title = "Район"

    location_str = soup.find(itemprop="address")
    if location_str is None:
        location_str = "not found"
    if type(location_str) is str:
        print("error with location_str")
        return

    apartment_location = location_str.text.split("р-н ")

    if len(apartment_location) == 2:
        apartment_address = apartment_location[0]
        apartment_district = apartment_location[1]
    else:
        str_not_found = "not found"
        apartment_address = apartment_location[0]
        apartment_district = str_not_found

    about_apartment_titles.append(apartment_address_title)
    about_apartment_info.append(apartment_address)
    about_apartment_titles.append(apartment_district_title)
    about_apartment_info.append(apartment_district)

    building_list = soup.find("div", class_="style-item-params-1-rPe").find_all("li")
    building_parameters_list = []

    for i in building_list:
        building_parameters_list.append(i.text.strip(" \n"))

    for i in building_parameters_list:
        building_str_info = pattern_for_building_info.findall(i + "\n")
        for n in building_str_info:
            about_apartment_info.append(n.strip(" ,"))

        building_str_titles = pattern_for_titles.findall(i + "\n")
        for n in building_str_titles:
            about_apartment_titles.append(n.strip(" ,"))

    # Filling in the string template based on the information received from the site.
    # Заполнение шаблона строки на основании информации полученной с сайта.
    len_str_with_apartment_info = len(str_with_apartment_info)
    len_about_apartment_info = len(about_apartment_info)
    n_1 = 0
    n_2 = 0
    while n_1 < len_about_apartment_info:
        while n_2 < len_str_with_apartment_info:
            if about_apartment_titles[n_1] == pattern_with_apartment_info[n_2]:
                str_with_apartment_info[n_2] = about_apartment_info[n_1]
            n_2 = n_2 + 1
        n_1 = n_1 + 1
        n_2 = 0

    # Adding a link to the ad to the top of the list with information about the apartment.
    # Добавление в начало списка с информацией о квартире ссылки на объявление.
    str_with_apartment_info.insert(0, url)


    # Recording the final information about the apartment in a csv file.
    # Запись итоговой информации о квартире в csv файл.
    csv_operations(str_with_apartment_info)

    # Delete the file that contains the page we downloaded.
    # Удаляем файл в котором содержится скачанная нами страница.
    os.remove(file_path)


# A function for writing information about an apartment to a csv file.
# Функция для записи информации о квартире в csv файл.
def csv_operations(data):

    # Open the csv file and write the data about the apartment into it.
    # Открываем csv файл и записываем в него данные о квартире.
    with open("avito_dataset.csv", mode="a", encoding='utf-8') as csv_file:
        file_writer = csv.writer(csv_file, delimiter=";", lineterminator="\n")
        file_writer.writerow(data)
    # -----------


# The main function of the program.
# Главная функция программы.
def main():

    apartments_url_list = []
    number_of_pages = 21
    num = 9

    url_start = 'https://krasnoyarsk.cian.ru/cat.php?deal_type=rent&engine_version=2&offer_type=flat&p='
    url_end = '&region=4827&room1=1&room2=1&room3=1&room4=1&room9=1&type=4'

    while num <= number_of_pages:
        url_with_number = url_start + str(num) + url_end
        apartments_url_list_buffer = get_links(url_with_number)
        apartments_url_list = apartments_url_list + apartments_url_list_buffer
        num = num + 1

    apartments_url_list = set(apartments_url_list)

    print(len(apartments_url_list))
    print(len(set(apartments_url_list)))

    with open("links.txt", "w", encoding="utf-8") as file:
        links_text = "page number: "
        counter = 1
        for j in apartments_url_list:
            file.write(j + '\n')
            print(counter)
            counter = counter + 1

    j = 1
    apartment_num_text = "apartment number: "
    for k in apartments_url_list:
        get_detailed_info(k)
        print(j)
        j = j + 1


if __name__ == '__main__':
    main()
