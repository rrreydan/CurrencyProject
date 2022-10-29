from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_currency, name='show_currency'),
    path('export/', views.export_currency, name='export_currency'),
]
