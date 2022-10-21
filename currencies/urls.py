from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_currency, name='show_currency'),
    path('select/', views.select_currency, name='select'),
]
