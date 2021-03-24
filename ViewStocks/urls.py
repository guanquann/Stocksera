from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('ticker_price/', views.stock_price, name='ticker_price'),
    path('reddit_analysis/', views.reddit_analysis, name='reddit_analysis'),
    path('google_analysis/', views.google_analysis, name='google_analysis'),
    path('industry/', views.industries_analysis, name='industry_analysis'),
]
