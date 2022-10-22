from . import service
from .models import Currency

from django.shortcuts import render


def show_currency(request):
    currencies = Currency.objects.all()
    currency_id = int(request.GET.get('id', default=1))

    info_about_currency = {}

    data_dict = service.get_dict_of_currencies()

    for i in data_dict.keys():
        for j in data_dict[i].keys():
            if j == currency_id - 1:
                info_about_currency[i] = data_dict[i][currency_id - 1]

    return render(request, 'show_currency.html', {'info': info_about_currency, 'currencies': currencies})
