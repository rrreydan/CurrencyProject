import requests
from bs4 import BeautifulSoup as bs
import pandas as pd


def get_dict_of_currencies():
    """
    Auxiliary function for obtaining a dictionary with currencies
    taken from the website of the Central Bank of the Russian Federation

    :return: dictionary with all currencies and their information
    """
    request = requests.get("https://www.cbr.ru/currency_base/daily/")

    soup = bs(request.text, "html.parser")
    currencies_table = soup.find('tbody')
    headers = []

    # getting all the column names
    for i in currencies_table.find_all('th'):
        title = i.text
        headers.append(title)

    data = pd.DataFrame(columns=headers)

    # getting all the information from the table
    for i in currencies_table.find_all('tr')[1:]:
        row_data = i.find_all('td')
        row = [i.text for i in row_data]
        length = len(data)
        data.loc[length] = row

    return data.to_dict()


def get_all_currencies(currencies):
    data_dict = get_dict_of_currencies()
    list_of_currencies = []

    for currency_id in range(len(currencies)):
        info_about_currency = {}

        for i in data_dict:
            info_about_currency.update({i: data_dict.get(i).get(currency_id)})

        list_of_currencies.append(info_about_currency)

    return list_of_currencies


def get_some_currencies(request):
    data_dict = get_dict_of_currencies()

    try:
        currency_id = {}
        currency_id.update(request.GET)  # getting all transmitted ids
        list_of_currencies = []

        # going through the entire list with ids
        for cur_id in [int(i) for i in currency_id.get('id')]:
            info_about_currency = {}

            for i in data_dict:
                info_about_currency.update({i: data_dict.get(i).get(cur_id - 1)})

            list_of_currencies.append(info_about_currency)

        return list_of_currencies
    except TypeError:
        return [{
            'Цифр. код': data_dict.get('Цифр. код').get(0),
            'Букв. код': data_dict.get('Букв. код').get(0),
            'Единиц': data_dict.get('Единиц').get(0),
            'Валюта': data_dict.get('Валюта').get(0),
            'Курс': data_dict.get('Курс').get(0)}]
