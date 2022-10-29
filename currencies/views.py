from . import service
from .models import Currency

from django.shortcuts import render


def show_currency(request):
    currencies = Currency.objects.all()

    # Check whether the item with the withdrawal of all currencies is selected
    # if yes, then create a list and fill it with all currencies
    if request.GET.get('is_all'):
        return render(request, 'show_currency.html', {'info': service.get_currencies(request, True),
                                                      'currencies': currencies})
    else:
        return render(request, 'show_currency.html', {'info': service.get_currencies(request),
                                                      'currencies': currencies})
