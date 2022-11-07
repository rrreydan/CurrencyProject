import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
from datetime import datetime


def get_dict_of_currencies(date):
    """
    Auxiliary function for obtaining a dictionary with currencies
    taken from the website of the Central Bank of the Russian Federation

    :return: dictionary with all currencies and their information
    """
    # Converting a date from a button to put it in a link to the central bank,
    # by the way, if nothing is transferred to date,
    # then the link will still remain working and will throw on today's date
    normal_date = '.'.join(date.split('-')[::-1])
    request = requests.get(f"https://www.cbr.ru/currency_base/daily/?UniDbQuery.Posted=True&UniDbQuery.To={normal_date}")

    soup = bs(request.text, "html.parser")
    td = [i.text for i in soup.findAll('td')]
    info = []

    for i in range(0, len(td), 5):
        info.append([td[i], td[i + 1], td[i + 2], td[i + 3], td[i + 4]])

    data = pd.DataFrame(info, columns=['Цифр. код', 'Букв. код', 'Единиц', 'Валюта', 'Курс'])
    data['Дата'] = [normal_date for _ in data.get('Валюта')]  # Adding a date to a DataFrame

    return data.to_dict()


def get_currencies(request, is_all=False):
    """
    A function for obtaining the necessary currencies for further use in the template

    :param request: request received from the form in the template
    :param is_all: A form parameter that says whether to output all currencies
    :return: list of selected currencies
    """
    data_dict = get_dict_of_currencies(request.POST.get('date', default=str(datetime.now())[:10]))
    list_of_currencies = []

    if is_all:
        for currency_id in range(len(data_dict.get('Валюта'))):
            info_about_currency = {}

            for i in data_dict:
                info_about_currency.update({i: data_dict.get(i).get(currency_id)})

            list_of_currencies.append(info_about_currency)

            create_export_files(list_of_currencies)

        return list_of_currencies
    else:
        if request.POST.get('id'):
            currency_id = {}
            currency_id.update(request.POST)  # getting all transmitted ids

            # going through the entire list with ids
            for cur_id in [int(i) for i in currency_id.get('id')]:
                info_about_currency = {}

                for i in data_dict:
                    info_about_currency.update({i: data_dict.get(i).get(cur_id)})

                list_of_currencies.append(info_about_currency)

            create_export_files(list_of_currencies)

            return list_of_currencies
        else:
            create_export_files(get_currencies(request, True))

            return get_currencies(request, True)


def create_export_files(list_of_currencies):
    """
    Function for creating files (Excel, CSV and PDF) for their further export

    :param list_of_currencies: List of selected currencies
    """
    pd.DataFrame(list_of_currencies).to_excel('static/files/currencies.xlsx', index=False)
    pd.DataFrame(list_of_currencies).to_csv('static/files/currencies.csv', index=False)
