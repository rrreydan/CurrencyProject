import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

from .models import Currency

last_list_of_currencies = []


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


def get_currencies(request, is_all=False):
    data_dict = get_dict_of_currencies(request.GET.get('date', default=''))
    list_of_currencies = []
    global last_list_of_currencies

    if is_all:
        for currency_id in range(len(Currency.objects.all())):
            info_about_currency = {}

            for i in data_dict:
                info_about_currency.update({i: data_dict.get(i).get(currency_id)})

            list_of_currencies.append(info_about_currency)

            last_list_of_currencies = list_of_currencies

        return list_of_currencies
    else:
        try:
            currency_id = {}
            currency_id.update(request.GET)  # getting all transmitted ids

            # going through the entire list with ids
            for cur_id in [int(i) for i in currency_id.get('id')]:
                info_about_currency = {}

                for i in data_dict:
                    info_about_currency.update({i: data_dict.get(i).get(cur_id - 1)})

                list_of_currencies.append(info_about_currency)

            last_list_of_currencies = list_of_currencies

            return list_of_currencies
        except TypeError:
            last_list_of_currencies = get_currencies(request, True)

            return get_currencies(request, True)


def export(export_type):
    df = pd.DataFrame(last_list_of_currencies)

    if export_type == 'excel':
        df.to_excel('currencies.xlsx')
    elif export_type == 'csv':
        df.to_csv('currencies.csv')
    elif export_type == 'pdf':
        dataframe_to_pdf(df, 'currencies.pdf')


def _draw_as_table(df, pagesize):
    alternating_colors = [['white'] * len(df.columns), ['lightgray'] * len(df.columns)] * len(df)
    alternating_colors = alternating_colors[:len(df)]
    fig, ax = plt.subplots(figsize=pagesize)
    ax.axis('tight')
    ax.axis('off')
    the_table = ax.table(cellText=df.values,
                         rowLabels=df.index,
                         colLabels=df.columns,
                         rowColours=['lightblue'] * len(df),
                         colColours=['lightblue'] * len(df.columns),
                         cellColours=alternating_colors,
                         loc='center')
    return fig


def dataframe_to_pdf(df, filename, numpages=(1, 1), pagesize=(11, 8.5)):
    with PdfPages(filename) as pdf:
        nh, nv = numpages
        rows_per_page = len(df) // nh
        cols_per_page = len(df.columns) // nv
        for i in range(0, nh):
            for j in range(0, nv):
                page = df.iloc[(i * rows_per_page):min((i + 1) * rows_per_page, len(df)),
                               (j * cols_per_page):min((j + 1) * cols_per_page, len(df.columns))]
                fig = _draw_as_table(page, pagesize)
                if nh > 1 or nv > 1:
                    # Add a part/page number at bottom-center of page
                    fig.text(0.5, 0.5 / pagesize[0],
                             "Part-{}x{}: Page-{}".format(i + 1, j + 1, i * nv + j + 1),
                             ha='center', fontsize=8)
                pdf.savefig(fig, bbox_inches='tight')

                plt.close()
