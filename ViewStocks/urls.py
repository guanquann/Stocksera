from django.urls import path

from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('ticker/', views.stock_price, name='ticker'),
    path('earnings_calendar/', views.earnings_calendar, name='earnings_calendar'),
    path('ticker/financial/', views.financial, name='financial'),
    path('ticker/options/', views.options, name='options'),
    path('reddit_analysis/', views.reddit_analysis, name='reddit_analysis'),
    path('top_movers/', views.top_movers, name='top_movers'),
    path('short_interest/', views.short_interest, name='short_interest'),
    path('low_float/', views.low_float, name='low_float'),
    path('penny_stocks/', views.penny_stocks, name='penny_stocks'),
    path('latest_news/', views.latest_news, name='latest_news'),
    path('subreddit_count/', views.subreddit_count, name='subreddit_count'),
    path('industry/', views.industries_analysis, name='industry_analysis'),
    path('reddit_etf/', views.reddit_etf, name='reddit_etf'),
    path('opinion/', views.opinion, name='opinion'),
    path('contact/', views.contact, name='contact'),
]
