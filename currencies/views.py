from datetime import datetime

from . import service

from django.shortcuts import render


def show_currency(request):
    currencies = {}

    # Transfer to select only those currencies that existed at the time of the selected date
    currencies.update(service.get_dict_of_currencies(request.POST.get('date', default='')).get('Валюта'))

    return render(request, 'show_currency.html', {'info': service.get_currencies(request),
                                                  'currencies': currencies,
                                                  'chosen_date': request.POST.get('date'),
                                                  'date_now': str(datetime.now())[:10]})
