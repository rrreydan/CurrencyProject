from . import service
from .models import Currency

from django.shortcuts import render


def show_currency(request):
    currencies = Currency.objects.all()

    # Check whether the item with the withdrawal of all currencies is selected
    # if yes, then create a list and fill it with all currencies
    if request.GET.get('is_all'):
        list_of_currencies = []
        data_dict = service.get_dict_of_currencies()

        for currency_id in range(len(currencies)):
            info_about_currency = {}

            for i in data_dict:
                info_about_currency.update({i: data_dict.get(i).get(currency_id)})

            list_of_currencies.append(info_about_currency)

        return render(request, 'show_currency.html', {'info_all': list_of_currencies, 'currencies': currencies})
    else:
        currency_id = {}
        currency_id.update(request.GET)  # getting all transmitted ids
        list_of_currencies = []
        data_dict = service.get_dict_of_currencies()

        # going through the entire list with ids
        for cur_id in [int(i) for i in currency_id.get('id')]:
            info_about_currency = {}

            for i in data_dict:
                info_about_currency.update({i: data_dict.get(i).get(cur_id - 1)})

            list_of_currencies.append(info_about_currency)

        return render(request, 'show_currency.html', {'info': list_of_currencies, 'currencies': currencies})
