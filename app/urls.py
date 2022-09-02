from django.urls import path
from . import views

urlpatterns = [
    # Home
    path('', views.main, name='main'),

    # Stock
    path('ticker/', views.stock_price, name='ticker'),
    path('ticker/financial/', views.financial, name='financial'),
    path('ticker/options/', views.options, name='options'),
    path('ticker/short_volume/', views.short_volume, name='short_volume'),
    path('ticker/borrowed_shares/', views.borrowed_shares, name='borrowed_shares'),
    path('ticker/failure_to_deliver/', views.failure_to_deliver, name='failure_to_deliver'),
    path('ticker/regsho/', views.regsho, name='regsho'),
    path('historical_data/', views.historical_data, name='historical_data'),
    path('sub_news/', views.news_sentiment, name='sub_news'),
    path('google_trends/', views.google_trends, name='google_trends'),
    path('recommendations/', views.ticker_recommendations, name='recommendations'),
    path('major_holders/', views.ticker_major_holders, name='major_holders'),
    path('institutional_holders/', views.ticker_institutional_holders, name='institutional_holders'),
    path('mutual_fund_holders', views.ticker_mutual_fund_holders, name='mutual_fund_holders'),
    path('dividend_and_split/', views.dividend_and_split, name='dividend_and_split'),
    path('tradingview/', views.tradingview, name='tradingview'),
    path('discussion/', views.discussion, name='discussion'),
    path('ticker_earnings/', views.ticker_earnings, name='ticker_earnings'),
    path('sec_fillings/', views.sec_fillings, name='sec_fillings'),
    path('insider_trading/', views.insider_trading, name='insider_trading'),

    # Reddit
    path('reddit_analysis/', views.reddit_analysis, name='reddit_analysis'),
    path('wsb_live/', views.wsb_live, name='wsb_live'),
    path('wsb_live_ticker/', views.wsb_live_ticker, name="wsb_live_ticker"),
    path('crypto_live/', views.crypto_live, name='crypto_live'),
    path('crypto_live_ticker/', views.crypto_live_ticker, name="crypto_live_ticker"),
    path('wsb_documentation/', views.wsb_documentation, name="wsb_documentation"),
    path('reddit_ticker_analysis/', views.reddit_ticker_analysis, name='reddit_ticker_analysis'),
    path('subreddit_count/', views.subreddit_count, name='subreddit_count'),
    path('reddit_etf/', views.reddit_etf, name='reddit_etf'),

    # Market Summary
    path('latest_insider/', views.latest_insider, name='latest_insider'),
    path('market_summary/', views.market_summary, name='market_summary'),
    path('futures/', views.futures, name='futures'),

    # Government
    path('senate/', views.senate_trades, name='senate'),
    path('house/', views.house_trades, name='house'),

    # Economy
    path('reverse_repo/', views.reverse_repo, name='reverse_repo'),
    path('daily_treasury/', views.daily_treasury, name='daily_treasury'),
    path('inflation/', views.inflation, name='inflation'),
    path('world_inflation/', views.world_inflation, name='world_inflation'),
    path('retail_sales/', views.retail_sales, name='retail_sales'),
    path('initial_jobless_claims/', views.initial_jobless_claims, name='initial_jobless_claims'),

    # Discover
    path('ark_trades/', views.ark_trades, name='ark_trades'),
    path('amd_xlnx_ratio/', views.amd_xlnx_ratio, name='amd_xlnx_ratio'),
    path('ipo_calendar/', views.ipo_calendar, name='ipo_calendar'),
    path('stocktwits/', views.stocktwits, name='stocktwits'),
    path('jim_cramer/', views.jim_cramer, name='jim_cramer'),
    path('twitter_trending/', views.twitter_trending, name='twitter_trending'),
    path('beta/', views.beta, name='beta'),
    path('covid_beta/', views.covid_beta, name='covid_beta'),
    path('short_interest/', views.short_interest, name='short_interest'),
    path('low_float/', views.low_float, name='low_float'),
    path('earnings_calendar/', views.earnings_calendar, name='earnings_calendar'),
    path('stock_split/', views.stock_split, name='stock_split'),
    path('dividend_history/', views.dividend_history, name='dividend_history'),
    path('correlation/', views.correlation, name='correlation'),

    # News
    path('news/', views.news, name='news'),
    path('twitter_feed/', views.twitter_feed, name='twitter_feed'),
    path('trading_halts/', views.trading_halts, name='trading_halts'),

    # Spinner
    path('loading/', views.loading_spinner, name='loading'),

    # Subscription
    path('subscribe/', views.subscribe_to_wsb_notifications, name='subscribe'),
    path('mailing_preference/', views.mailing_preference, name='mailing_preference'),
    path('unsubscribe/', views.unsubscribe, name='unsubscribe'),
    path('sample_email/', views.sample_email, name='sample_email'),

    # About
    path('about/', views.about, name='about'),
]
