from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('ticker_price/', views.stock_price, name='ticker_price'),
]
