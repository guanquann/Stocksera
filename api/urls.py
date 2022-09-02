from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.urls import path
from . import views

schema_view = get_schema_view(
   openapi.Info(
      title="Stocksera API",
      default_version='v1',
      description="Official API for Stocksera",
      terms_of_service="https://stocksera.pythonanywhere.com",
      contact=openapi.Contact(email="stocksera@gmail.com"),
      license=openapi.License(name="MIT License"),
   ),
   public=True,
)

urlpatterns = [
    path(r'swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path(r'docs/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path('stocksera_trending/', views.stocksera_trending, name='api_stocksera_trending'),

    path('stocks/sec_fillings/<str:ticker_selected>/', views.sec_fillings, name='api_sec_fillings'),

    path('stocks/news_sentiment/<str:ticker_selected>/', views.news_sentiment, name='api_news_sentiment'),

    path('stocks/insider_trading/<str:ticker_selected>/', views.insider_trading, name='api_insider_trading'),

    path('discover/latest_insider_summary/', views.latest_insider_summary, name='api_latest_insider_summary'),

    path('discover/latest_insider/', views.latest_insider, name='api_latest_insider'),

    path('stocks/top_short_volume/', views.top_short_volume, name='api_top_short_volume'),

    path('stocks/short_volume/<str:ticker_selected>/', views.short_volume, name='api_short_volume'),

    path('stocks/top_failure_to_deliver/', views.top_failure_to_deliver, name='api_top_failure_to_deliver'),

    path('stocks/failure_to_deliver/<str:ticker_selected>/', views.failure_to_deliver, name='api_failure_to_deliver'),

    path('stocks/regsho/', views.regsho, name='api_regsho'),
    path('stocks/regsho/<str:ticker_selected>/', views.regsho, name='api_regsho'),

    path('news/earnings_calendar/', views.earnings_calendar, name='api_earnings_calendar'),

    path('news/market_news/', views.market_news, name='api_market_news'),

    path('news/trading_halts/', views.trading_halts, name='api_trading_halts'),

    path('reddit/subreddit_count/<str:ticker_selected>/', views.subreddit_count, name='api_subreddit_count'),

    path('reddit/<str:subreddit>/', views.reddit_mentions, name='api_reddit_mentions'),
    path('reddit/<str:subreddit>/<str:ticker_selected>/', views.reddit_mentions, name='api_reddit_mentions'),

    path('reddit/wsb_options/', views.wsb_options, name='api_wsb_options'),

    path('government/<str:gov_type>/', views.government, name='api_government'),

    path('economy/reverse_repo/', views.reverse_repo, name='api_reverse_repo'),
    path('economy/daily_treasury/', views.daily_treasury, name='api_daily_treasury'),

    path('economy/inflation/<str:area>/', views.inflation, name='api_inflation'),

    path('economy/retail_sales/', views.retail_sales, name='api_retail_sales'),
    path('economy/initial_jobless_claims/', views.initial_jobless_claims, name='api_initial_jobless_claims'),

    path('discover/short_interest/', views.short_interest, name='api_short_interest'),

    path('discover/low_float/', views.low_float, name='api_low_float'),

    path('stocktwits/', views.stocktwits, name='api_stocktwits'),
    path('stocktwits/<str:ticker_selected>/', views.stocktwits, name='api_stocktwits'),

    path('discover/ipo_calendar/', views.ipo_calendar, name='api_ipo_calendar'),

    path('news/market_summary/', views.market_summary, name='api_market_summary'),

    path('discover/jim_cramer/', views.jim_cramer, name='api_jim_cramer'),
    path('discover/jim_cramer/<str:ticker_selected>/', views.jim_cramer, name='api_jim_cramer'),

    path('stocks/borrowed_shares/<str:ticker_selected>/', views.borrowed_shares, name='api_borrowed_shares'),

    path('discover/stock_split/', views.stock_split, name='api_stock_split'),

    path('discover/dividend_history/', views.dividend_history, name='api_dividend_history'),

    path('stocksera_api_key/', views.stocksera_api_key, name='api_stocksera_api_key'),
    path('signup/', views.signup, name='api_signup'),
    path('login/', views.login, name='api_login'),
]
