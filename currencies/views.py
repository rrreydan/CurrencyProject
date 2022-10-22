from . import service
from .models import Currency

from django.shortcuts import render


def show_currency(request):
    currencies = Currency.objects.all()

    if request.GET.get('is_all'):
        list_of_currencies = []
        data_dict = service.get_dict_of_currencies()

        for i in currencies:
            info_about_currency = {}

            for j in data_dict.keys():
                for k in data_dict[j].keys():
                    if k == i.id - 1:
                        info_about_currency[j] = data_dict[j][i.id - 1]

            list_of_currencies.append(info_about_currency)

        return render(request, 'show_currency.html', {'info_all': list_of_currencies, 'currencies': currencies})
    else:
        currency_id = int(request.GET.get('id', default=1))
        info_about_currency = {}
        data_dict = service.get_dict_of_currencies()

        for i in data_dict.keys():
            for j in data_dict[i].keys():
                if j == currency_id - 1:
                    info_about_currency[i] = data_dict[i][currency_id - 1]

        return render(request, 'show_currency.html', {'info': info_about_currency, 'currencies': currencies})
