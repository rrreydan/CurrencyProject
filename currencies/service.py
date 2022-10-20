import requests
from bs4 import BeautifulSoup as bs
import pandas as pd


def get_dict_of_currencies():
    """
    Auxiliary function for obtaining a dictionary with currencies
    taken from the website of the Central Bank of the Russian Federation

    :return: dictionary with all currencies and their information
    """
    request = requests.get("http://www.cbr.ru/currency_base/daily/")

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
