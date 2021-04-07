from django.urls import path

from . import views

urlpatterns = [
    path('home/', views.main, name='main'),
    path('', views.format, name='format'),
    path('ticker/', views.stock_price, name='ticker'),
    path('reddit_analysis/', views.reddit_analysis, name='reddit_analysis'),
    path('google_analysis/', views.google_analysis, name='google_analysis'),
    path('industry/', views.industries_analysis, name='industry_analysis'),
    path('reddit_etf/', views.reddit_etf, name='reddit_etf'),
    path('opinion/', views.opinion, name='opinion'),
    path('contact/', views.contact, name='contact'),
]
