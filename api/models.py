# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class CryptoChange(models.Model):
    ticker = models.CharField(max_length=10, blank=True, null=True)
    mentions = models.IntegerField(blank=True, null=True)
    percent_change = models.FloatField(blank=True, null=True)

    class Meta:
        db_table = 'crypto_change'


class CryptoTrending24H(models.Model):
    ticker = models.CharField(max_length=10, blank=True, null=True)
    mentions = models.IntegerField(blank=True, null=True)
    sentiment = models.FloatField(blank=True, null=True)
    date_updated = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'crypto_trending_24h'


class CryptoTrendingHourly(models.Model):
    ticker = models.CharField(max_length=10, blank=True, null=True)
    mentions = models.IntegerField(blank=True, null=True)
    sentiment = models.FloatField(blank=True, null=True)
    date_updated = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'crypto_trending_hourly'


class CryptoWordCloud(models.Model):
    word = models.CharField(max_length=100, blank=True, null=True)
    mentions = models.IntegerField(blank=True, null=True)
    date_updated = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'crypto_word_cloud'


class Cryptocurrency(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    rank = models.IntegerField()
    ticker = models.CharField(max_length=10, blank=True, null=True)
    total = models.IntegerField()
    recent = models.IntegerField()
    previous = models.IntegerField()
    change = models.CharField(max_length=10, blank=True, null=True)
    rockets = models.IntegerField()
    posts = models.IntegerField()
    upvotes = models.IntegerField()
    comments = models.IntegerField()
    price = models.CharField(max_length=10, blank=True, null=True)
    one_day_change_percent = models.CharField(max_length=10, blank=True, null=True)
    thirty_day_change_percent = models.CharField(max_length=10, blank=True, null=True)
    volume = models.CharField(max_length=10, blank=True, null=True)
    mkt_cap = models.CharField(max_length=25, blank=True, null=True)
    circulating_supply = models.CharField(max_length=20, blank=True, null=True)
    max_supply = models.CharField(max_length=20, blank=True, null=True)
    date_updated = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cryptocurrency'
        unique_together = (('ticker', 'date_updated'),)


class DailyTickerNews(models.Model):
    ticker = models.CharField(db_column='Ticker', max_length=10, blank=True, null=True)  # Field name made lowercase.
    date = models.CharField(db_column='Date', max_length=20, blank=True, null=True)  # Field name made lowercase.
    title = models.CharField(db_column='Title', max_length=500, blank=True, null=True)  # Field name made lowercase.
    link = models.CharField(db_column='Link', max_length=300, blank=True, null=True)  # Field name made lowercase.
    sentiment = models.CharField(db_column='Sentiment', max_length=20, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'daily_ticker_news'


class DailyTreasury(models.Model):
    record_date = models.CharField(unique=True, max_length=20, blank=True, null=True)
    close_today_bal = models.FloatField(blank=True, null=True)
    open_today_bal = models.FloatField(blank=True, null=True)
    amount_change = models.FloatField(blank=True, null=True)
    percent_change = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'daily_treasury'
# Unable to inspect table 'django_admin_log'
# The error was: 'DatabaseIntrospection' object has no attribute '_parse_constraint_columns'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Earnings(models.Model):
    date = models.CharField(max_length=20, blank=True, null=True)
    hour = models.CharField(max_length=20, blank=True, null=True)
    ticker = models.CharField(max_length=10, blank=True, null=True)
    eps_est = models.CharField(max_length=20, blank=True, null=True)
    eps_act = models.CharField(max_length=20, blank=True, null=True)
    revenue_est = models.CharField(max_length=20, blank=True, null=True)
    revenue_act = models.CharField(max_length=20, blank=True, null=True)
    year = models.CharField(max_length=10, blank=True, null=True)
    quarter = models.CharField(max_length=10, blank=True, null=True)
    mkt_cap = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'earnings'
        unique_together = (('ticker', 'hour'),)


class EarningsCalendar(models.Model):
    company_name = models.CharField(max_length=200, blank=True, null=True)
    ticker = models.CharField(max_length=10, blank=True, null=True)
    mkt_cap = models.BigIntegerField(blank=True, null=True)
    eps_est = models.CharField(max_length=20, blank=True, null=True)
    eps_act = models.CharField(max_length=20, blank=True, null=True)
    surprise = models.CharField(max_length=20, blank=True, null=True)
    earning_date = models.CharField(max_length=20, blank=True, null=True)
    earning_time = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'earnings_calendar'
        unique_together = (('company_name', 'ticker'),)


class Ftd(models.Model):
    date = models.CharField(db_column='Date', max_length=20, blank=True, null=True)  # Field name made lowercase.
    ticker = models.CharField(db_column='Ticker', max_length=10, blank=True, null=True)  # Field name made lowercase.
    failure_to_deliver = models.FloatField(db_column='Failure to Deliver', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    price = models.CharField(db_column='Price', max_length=20, blank=True, null=True)  # Field name made lowercase.
    t_35_date = models.CharField(db_column='T+35 Date', max_length=20, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.

    class Meta:
        managed = False
        db_table = 'ftd'
        unique_together = (('date', 'ticker'),)


class HighestShortVolume(models.Model):
    rank = models.BigIntegerField(db_column='Rank', blank=True, null=True)  # Field name made lowercase.
    ticker = models.TextField(db_column='Ticker', blank=True, null=True)  # Field name made lowercase.
    short_volume = models.FloatField(db_column='Short Volume', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    short_exempt_vol = models.FloatField(db_column='Short Exempt Vol', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    total_volume = models.FloatField(db_column='Total Volume', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    field_shorted = models.FloatField(db_column='% Shorted', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it started with '_'.
    previous_close = models.FloatField(db_column='Previous Close', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    number_1_day_change_field = models.FloatField(db_column='1 Day Change %', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'. Field renamed because it wasn't a valid Python identifier.
    market_cap = models.TextField(db_column='Market Cap', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.

    class Meta:
        managed = False
        db_table = 'highest_short_volume'


class InitialJoblessClaims(models.Model):
    record_date = models.CharField(unique=True, max_length=20, blank=True, null=True)
    value = models.IntegerField(blank=True, null=True)
    percent_change = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'initial_jobless_claims'


class InsiderTrading(models.Model):
    ticker = models.CharField(db_column='Ticker', max_length=10, blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=200, blank=True, null=True)  # Field name made lowercase.
    relationship = models.CharField(db_column='Relationship', max_length=200, blank=True, null=True)  # Field name made lowercase.
    transactiondate = models.CharField(db_column='TransactionDate', max_length=20, blank=True, null=True)  # Field name made lowercase.
    transactiontype = models.CharField(db_column='TransactionType', max_length=100, blank=True, null=True)  # Field name made lowercase.
    cost = models.FloatField(db_column='Cost', blank=True, null=True)  # Field name made lowercase.
    shares = models.IntegerField(db_column='Shares', blank=True, null=True)  # Field name made lowercase.
    value = models.IntegerField(db_column='Value', blank=True, null=True)  # Field name made lowercase.
    sharesleft = models.IntegerField(db_column='SharesLeft', blank=True, null=True)  # Field name made lowercase.
    url = models.CharField(db_column='URL', max_length=300, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'insider_trading'


class Investing(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    rank = models.IntegerField()
    ticker = models.CharField(max_length=10, blank=True, null=True)
    total = models.IntegerField()
    recent = models.IntegerField()
    previous = models.IntegerField()
    change = models.CharField(max_length=10, blank=True, null=True)
    rockets = models.IntegerField()
    posts = models.IntegerField()
    upvotes = models.IntegerField()
    comments = models.IntegerField()
    price = models.CharField(max_length=10, blank=True, null=True)
    one_day_change_percent = models.CharField(max_length=10, blank=True, null=True)
    fifty_day_change_percent = models.CharField(max_length=10, blank=True, null=True)
    volume = models.CharField(max_length=10, blank=True, null=True)
    mkt_cap = models.CharField(max_length=25, blank=True, null=True)
    floating_shares = models.CharField(max_length=10, blank=True, null=True)
    beta = models.CharField(max_length=10, blank=True, null=True)
    short_per_float = models.CharField(max_length=10, blank=True, null=True)
    industry = models.CharField(max_length=100, blank=True, null=True)
    prev_close = models.CharField(max_length=10, blank=True, null=True)
    open = models.CharField(max_length=10, blank=True, null=True)
    day_low = models.CharField(max_length=10, blank=True, null=True)
    day_high = models.CharField(max_length=10, blank=True, null=True)
    target = models.CharField(max_length=10, blank=True, null=True)
    recommend = models.CharField(max_length=20, blank=True, null=True)
    date_updated = models.CharField(max_length=20, blank=True, null=True)
    subreddit = models.CharField(max_length=25, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'investing'
        unique_together = (('ticker', 'date_updated'),)


class IpoCalendar(models.Model):
    date = models.TextField(db_column='Date', blank=True, null=True)  # Field name made lowercase.
    symbol = models.TextField(db_column='Symbol', blank=True, null=True)  # Field name made lowercase.
    name = models.TextField(db_column='Name', blank=True, null=True)  # Field name made lowercase.
    expected_price = models.TextField(db_column='Expected Price', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    number_shares = models.TextField(db_column='Number Shares', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    mkt_cap = models.TextField(db_column='Mkt Cap', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    status = models.TextField(db_column='Status', blank=True, null=True)  # Field name made lowercase.
    exchange = models.TextField(db_column='Exchange', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ipo_calendar'


class JimCramerTrades(models.Model):
    ticker = models.CharField(db_column='Ticker', max_length=10, blank=True, null=True)  # Field name made lowercase.
    date = models.CharField(db_column='Date', max_length=20, blank=True, null=True)  # Field name made lowercase.
    segment = models.CharField(db_column='Segment', max_length=50, blank=True, null=True)  # Field name made lowercase.
    call = models.CharField(db_column='Call', max_length=50, blank=True, null=True)  # Field name made lowercase.
    price = models.FloatField(db_column='Price', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'jim_cramer_trades'


class LatestInsiderTrading(models.Model):
    ticker = models.CharField(db_column='Ticker', max_length=10, blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=200, blank=True, null=True)  # Field name made lowercase.
    relationship = models.CharField(db_column='Relationship', max_length=200, blank=True, null=True)  # Field name made lowercase.
    transactiondate = models.CharField(db_column='TransactionDate', max_length=20, blank=True, null=True)  # Field name made lowercase.
    transactiontype = models.CharField(db_column='TransactionType', max_length=100, blank=True, null=True)  # Field name made lowercase.
    cost = models.FloatField(db_column='Cost', blank=True, null=True)  # Field name made lowercase.
    shares = models.IntegerField(db_column='Shares', blank=True, null=True)  # Field name made lowercase.
    value = models.IntegerField(db_column='Value', blank=True, null=True)  # Field name made lowercase.
    sharesleft = models.IntegerField(db_column='SharesLeft', blank=True, null=True)  # Field name made lowercase.
    datefilled = models.CharField(db_column='DateFilled', max_length=20, blank=True, null=True)  # Field name made lowercase.
    url = models.CharField(db_column='URL', max_length=300, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'latest_insider_trading'
        unique_together = (('ticker', 'name', 'relationship', 'transactiondate', 'transactiontype', 'cost', 'shares', 'value', 'sharesleft', 'datefilled'),)


class LatestInsiderTradingAnalysis(models.Model):
    ticker = models.TextField(db_column='Ticker', blank=True, null=True)  # Field name made lowercase.
    amount = models.BigIntegerField(db_column='Amount', blank=True, null=True)  # Field name made lowercase.
    mktcap = models.BigIntegerField(db_column='MktCap', blank=True, null=True)  # Field name made lowercase.
    proportion = models.FloatField(db_column='Proportion', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'latest_insider_trading_analysis'


class LowFloat(models.Model):
    ticker = models.CharField(max_length=10, blank=True, null=True)
    company_name = models.CharField(max_length=200, blank=True, null=True)
    exchange = models.CharField(max_length=100, blank=True, null=True)
    previous_close = models.FloatField(blank=True, null=True)
    one_day_change = models.FloatField(blank=True, null=True)
    floating_shares = models.CharField(max_length=20, blank=True, null=True)
    outstanding_shares = models.CharField(max_length=20, blank=True, null=True)
    short_int = models.CharField(max_length=20, blank=True, null=True)
    market_cap = models.CharField(max_length=20, blank=True, null=True)
    industry = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'low_float'


class MarketNews(models.Model):
    date = models.CharField(db_column='Date', max_length=20, blank=True, null=True)  # Field name made lowercase.
    title = models.CharField(db_column='Title', max_length=300, blank=True, null=True)  # Field name made lowercase.
    source = models.CharField(db_column='Source', max_length=100, blank=True, null=True)  # Field name made lowercase.
    url = models.CharField(db_column='URL', max_length=300, blank=True, null=True)  # Field name made lowercase.
    section = models.CharField(db_column='Section', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'market_news'
        unique_together = (('date', 'title'),)


class Options(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    rank = models.IntegerField()
    ticker = models.CharField(max_length=10, blank=True, null=True)
    total = models.IntegerField()
    recent = models.IntegerField()
    previous = models.IntegerField()
    change = models.CharField(max_length=10, blank=True, null=True)
    rockets = models.IntegerField()
    posts = models.IntegerField()
    upvotes = models.IntegerField()
    comments = models.IntegerField()
    price = models.CharField(max_length=10, blank=True, null=True)
    one_day_change_percent = models.CharField(max_length=10, blank=True, null=True)
    fifty_day_change_percent = models.CharField(max_length=10, blank=True, null=True)
    volume = models.CharField(max_length=10, blank=True, null=True)
    mkt_cap = models.CharField(max_length=25, blank=True, null=True)
    floating_shares = models.CharField(max_length=10, blank=True, null=True)
    beta = models.CharField(max_length=10, blank=True, null=True)
    short_per_float = models.CharField(max_length=10, blank=True, null=True)
    industry = models.CharField(max_length=100, blank=True, null=True)
    prev_close = models.CharField(max_length=10, blank=True, null=True)
    open = models.CharField(max_length=10, blank=True, null=True)
    day_low = models.CharField(max_length=10, blank=True, null=True)
    day_high = models.CharField(max_length=10, blank=True, null=True)
    target = models.CharField(max_length=10, blank=True, null=True)
    recommend = models.CharField(max_length=20, blank=True, null=True)
    date_updated = models.CharField(max_length=20, blank=True, null=True)
    subreddit = models.CharField(max_length=25, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'options'
        unique_together = (('ticker', 'date_updated'),)


class Pennystocks(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    rank = models.IntegerField()
    ticker = models.CharField(max_length=10, blank=True, null=True)
    total = models.IntegerField()
    recent = models.IntegerField()
    previous = models.IntegerField()
    change = models.CharField(max_length=10, blank=True, null=True)
    rockets = models.IntegerField()
    posts = models.IntegerField()
    upvotes = models.IntegerField()
    comments = models.IntegerField()
    price = models.CharField(max_length=10, blank=True, null=True)
    one_day_change_percent = models.CharField(max_length=10, blank=True, null=True)
    fifty_day_change_percent = models.CharField(max_length=10, blank=True, null=True)
    volume = models.CharField(max_length=10, blank=True, null=True)
    mkt_cap = models.CharField(max_length=25, blank=True, null=True)
    floating_shares = models.CharField(max_length=10, blank=True, null=True)
    beta = models.CharField(max_length=10, blank=True, null=True)
    short_per_float = models.CharField(max_length=10, blank=True, null=True)
    industry = models.CharField(max_length=100, blank=True, null=True)
    prev_close = models.CharField(max_length=10, blank=True, null=True)
    open = models.CharField(max_length=10, blank=True, null=True)
    day_low = models.CharField(max_length=10, blank=True, null=True)
    day_high = models.CharField(max_length=10, blank=True, null=True)
    target = models.CharField(max_length=10, blank=True, null=True)
    recommend = models.CharField(max_length=20, blank=True, null=True)
    date_updated = models.CharField(max_length=20, blank=True, null=True)
    subreddit = models.CharField(max_length=25, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pennystocks'
        unique_together = (('ticker', 'date_updated'),)


class RedditEtf(models.Model):
    ticker = models.CharField(max_length=10, blank=True, null=True)
    open_date = models.CharField(max_length=20, blank=True, null=True)
    open_price = models.FloatField(blank=True, null=True)
    num_shares = models.IntegerField(blank=True, null=True)
    close_date = models.CharField(max_length=20, blank=True, null=True)
    close_price = models.FloatField(blank=True, null=True)
    pnl = models.FloatField(db_column='PnL', blank=True, null=True)  # Field name made lowercase.
    percentage = models.FloatField(blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'reddit_etf'


class RelatedTickers(models.Model):
    ticker = models.CharField(max_length=10, blank=True, null=True)
    ticker1 = models.CharField(max_length=10, blank=True, null=True)
    ticker2 = models.CharField(max_length=10, blank=True, null=True)
    ticker3 = models.CharField(max_length=10, blank=True, null=True)
    ticker4 = models.CharField(max_length=10, blank=True, null=True)
    ticker5 = models.CharField(max_length=10, blank=True, null=True)
    ticker6 = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'related_tickers'


class RestFrameworkApiKeyApikey(models.Model):
    id = models.CharField(primary_key=True, max_length=150)
    created = models.DateTimeField()
    name = models.CharField(max_length=50)
    revoked = models.IntegerField()
    expiry_date = models.DateTimeField(blank=True, null=True)
    hashed_key = models.CharField(max_length=150)
    prefix = models.CharField(unique=True, max_length=8)

    class Meta:
        managed = False
        db_table = 'rest_framework_api_key_apikey'


class RetailSales(models.Model):
    record_date = models.CharField(unique=True, max_length=20, blank=True, null=True)
    value = models.FloatField(blank=True, null=True)
    percent_change = models.FloatField(blank=True, null=True)
    covid_monthly_avg = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'retail_sales'


class ReverseRepo(models.Model):
    record_date = models.CharField(unique=True, max_length=20, blank=True, null=True)
    amount = models.FloatField(blank=True, null=True)
    parties = models.IntegerField(blank=True, null=True)
    average = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'reverse_repo'


class SecFillings(models.Model):
    ticker = models.CharField(max_length=10, blank=True, null=True)
    filling = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=100, blank=True, null=True)
    filling_date = models.CharField(max_length=20, blank=True, null=True)
    report_url = models.CharField(max_length=300, blank=True, null=True)
    filing_url = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sec_fillings'


class SharesAvailable(models.Model):
    ticker = models.CharField(max_length=10, blank=True, null=True)
    fee = models.FloatField(blank=True, null=True)
    available = models.IntegerField(blank=True, null=True)
    date_updated = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'shares_available'
        unique_together = (('ticker', 'fee', 'available', 'date_updated'),)


class ShortInterest(models.Model):
    ticker = models.CharField(max_length=10, blank=True, null=True)
    date = models.CharField(max_length=20, blank=True, null=True)
    short_interest = models.IntegerField(blank=True, null=True)
    average_vol = models.IntegerField(blank=True, null=True)
    days_to_cover = models.FloatField(blank=True, null=True)
    percent_float_short = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'short_interest'


class ShortVolume(models.Model):
    date = models.CharField(db_column='Date', max_length=20, blank=True, null=True)  # Field name made lowercase.
    ticker = models.CharField(db_column='Ticker', max_length=10, blank=True, null=True)  # Field name made lowercase.
    short_vol = models.FloatField(db_column='Short Vol', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    short_exempt_vol = models.FloatField(db_column='Short Exempt Vol', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    total_vol = models.FloatField(db_column='Total Vol', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    field_shorted = models.FloatField(db_column='% Shorted', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it started with '_'.

    class Meta:
        managed = False
        db_table = 'short_volume'
        unique_together = (('date', 'ticker'),)


class Shortsqueeze(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    rank = models.IntegerField()
    ticker = models.CharField(max_length=10, blank=True, null=True)
    total = models.IntegerField()
    recent = models.IntegerField()
    previous = models.IntegerField()
    change = models.CharField(max_length=10, blank=True, null=True)
    rockets = models.IntegerField()
    posts = models.IntegerField()
    upvotes = models.IntegerField()
    comments = models.IntegerField()
    price = models.CharField(max_length=10, blank=True, null=True)
    one_day_change_percent = models.CharField(max_length=10, blank=True, null=True)
    fifty_day_change_percent = models.CharField(max_length=10, blank=True, null=True)
    volume = models.CharField(max_length=10, blank=True, null=True)
    mkt_cap = models.CharField(max_length=25, blank=True, null=True)
    floating_shares = models.CharField(max_length=10, blank=True, null=True)
    beta = models.CharField(max_length=10, blank=True, null=True)
    short_per_float = models.CharField(max_length=10, blank=True, null=True)
    industry = models.CharField(max_length=100, blank=True, null=True)
    prev_close = models.CharField(max_length=10, blank=True, null=True)
    open = models.CharField(max_length=10, blank=True, null=True)
    day_low = models.CharField(max_length=10, blank=True, null=True)
    day_high = models.CharField(max_length=10, blank=True, null=True)
    target = models.CharField(max_length=10, blank=True, null=True)
    recommend = models.CharField(max_length=20, blank=True, null=True)
    date_updated = models.CharField(max_length=20, blank=True, null=True)
    subreddit = models.CharField(max_length=25, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'shortsqueeze'
        unique_together = (('ticker', 'date_updated'),)


class Spacs(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    rank = models.IntegerField()
    ticker = models.CharField(max_length=10, blank=True, null=True)
    total = models.IntegerField()
    recent = models.IntegerField()
    previous = models.IntegerField()
    change = models.CharField(max_length=10, blank=True, null=True)
    rockets = models.IntegerField()
    posts = models.IntegerField()
    upvotes = models.IntegerField()
    comments = models.IntegerField()
    price = models.CharField(max_length=10, blank=True, null=True)
    one_day_change_percent = models.CharField(max_length=10, blank=True, null=True)
    fifty_day_change_percent = models.CharField(max_length=10, blank=True, null=True)
    volume = models.CharField(max_length=10, blank=True, null=True)
    mkt_cap = models.CharField(max_length=25, blank=True, null=True)
    floating_shares = models.CharField(max_length=10, blank=True, null=True)
    beta = models.CharField(max_length=10, blank=True, null=True)
    short_per_float = models.CharField(max_length=10, blank=True, null=True)
    industry = models.CharField(max_length=100, blank=True, null=True)
    prev_close = models.CharField(max_length=10, blank=True, null=True)
    open = models.CharField(max_length=10, blank=True, null=True)
    day_low = models.CharField(max_length=10, blank=True, null=True)
    day_high = models.CharField(max_length=10, blank=True, null=True)
    target = models.CharField(max_length=10, blank=True, null=True)
    recommend = models.CharField(max_length=20, blank=True, null=True)
    date_updated = models.CharField(max_length=20, blank=True, null=True)
    subreddit = models.CharField(max_length=25, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'spacs'
        unique_together = (('ticker', 'date_updated'),)


class Stocks(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    rank = models.IntegerField()
    ticker = models.CharField(max_length=10, blank=True, null=True)
    total = models.IntegerField()
    recent = models.IntegerField()
    previous = models.IntegerField()
    change = models.CharField(max_length=10, blank=True, null=True)
    rockets = models.IntegerField()
    posts = models.IntegerField()
    upvotes = models.IntegerField()
    comments = models.IntegerField()
    price = models.CharField(max_length=10, blank=True, null=True)
    one_day_change_percent = models.CharField(max_length=10, blank=True, null=True)
    fifty_day_change_percent = models.CharField(max_length=10, blank=True, null=True)
    volume = models.CharField(max_length=10, blank=True, null=True)
    mkt_cap = models.CharField(max_length=25, blank=True, null=True)
    floating_shares = models.CharField(max_length=10, blank=True, null=True)
    beta = models.CharField(max_length=10, blank=True, null=True)
    short_per_float = models.CharField(max_length=10, blank=True, null=True)
    industry = models.CharField(max_length=100, blank=True, null=True)
    prev_close = models.CharField(max_length=10, blank=True, null=True)
    open = models.CharField(max_length=10, blank=True, null=True)
    day_low = models.CharField(max_length=10, blank=True, null=True)
    day_high = models.CharField(max_length=10, blank=True, null=True)
    target = models.CharField(max_length=10, blank=True, null=True)
    recommend = models.CharField(max_length=20, blank=True, null=True)
    date_updated = models.CharField(max_length=20, blank=True, null=True)
    subreddit = models.CharField(max_length=25, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stocks'
        unique_together = (('ticker', 'date_updated'),)


class StockseraTrending(models.Model):
    ticker = models.CharField(unique=True, max_length=10, blank=True, null=True)
    name = models.CharField(max_length=300, blank=True, null=True)
    count = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stocksera_trending'


class StocktwitsTrending(models.Model):
    rank = models.IntegerField(blank=True, null=True)
    watchlist = models.IntegerField(blank=True, null=True)
    ticker = models.CharField(max_length=10, blank=True, null=True)
    date_updated = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stocktwits_trending'


class SubredditCount(models.Model):
    updated_date = models.CharField(max_length=20, blank=True, null=True)
    ticker = models.CharField(max_length=10, blank=True, null=True)
    subreddit = models.CharField(max_length=50, blank=True, null=True)
    subscribers = models.IntegerField(blank=True, null=True)
    active = models.IntegerField(blank=True, null=True)
    percentage_active = models.FloatField(blank=True, null=True)
    growth = models.FloatField(blank=True, null=True)
    percentage_price_change = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'subreddit_count'
        unique_together = (('ticker', 'subreddit', 'updated_date'),)


class Subscribers(models.Model):
    name = models.TextField(blank=True, null=True)
    email = models.TextField(unique=True, blank=True, null=True)
    freq = models.TextField(blank=True, null=True)
    user_id = models.TextField(blank=True, null=True)
    date_joined = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'subscribers'


class TopFtd(models.Model):
    date = models.TextField(db_column='Date', blank=True, null=True)  # Field name made lowercase.
    ticker = models.TextField(db_column='Ticker', blank=True, null=True)  # Field name made lowercase.
    ftd = models.FloatField(db_column='FTD', blank=True, null=True)  # Field name made lowercase.
    price = models.FloatField(db_column='Price', blank=True, null=True)  # Field name made lowercase.
    ftd_x_field = models.FloatField(db_column='FTD x $', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    t_35_date = models.TextField(db_column='T+35 Date', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.

    class Meta:
        managed = False
        db_table = 'top_ftd'


class TradingHalts(models.Model):
    halt_date = models.CharField(db_column='Halt Date', max_length=20, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    halt_time = models.CharField(db_column='Halt Time', max_length=20, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    ticker = models.CharField(db_column='Ticker', max_length=10, blank=True, null=True)  # Field name made lowercase.
    exchange = models.CharField(db_column='Exchange', max_length=100, blank=True, null=True)  # Field name made lowercase.
    reason = models.CharField(db_column='Reason', max_length=100, blank=True, null=True)  # Field name made lowercase.
    resume_date = models.CharField(db_column='Resume Date', max_length=20, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    resume_time = models.CharField(db_column='Resume Time', max_length=20, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.

    class Meta:
        managed = False
        db_table = 'trading_halts'
        unique_together = (('halt_date', 'halt_time', 'ticker'),)


class TwitterFollowers(models.Model):
    ticker = models.CharField(max_length=10, blank=True, null=True)
    followers = models.IntegerField(blank=True, null=True)
    updated_date = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'twitter_followers'
        unique_together = (('ticker', 'updated_date'),)


class TwitterTrending(models.Model):
    ticker = models.CharField(max_length=10, blank=True, null=True)
    tweet_count = models.IntegerField(blank=True, null=True)
    updated_date = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'twitter_trending'
        unique_together = (('ticker', 'updated_date'),)


class UsaInflation(models.Model):
    year = models.TextField(db_column='Year', blank=True, null=True)  # Field name made lowercase.
    jan = models.FloatField(db_column='Jan', blank=True, null=True)  # Field name made lowercase.
    feb = models.TextField(db_column='Feb', blank=True, null=True)  # Field name made lowercase.
    mar = models.TextField(db_column='Mar', blank=True, null=True)  # Field name made lowercase.
    apr = models.TextField(db_column='Apr', blank=True, null=True)  # Field name made lowercase.
    may = models.TextField(db_column='May', blank=True, null=True)  # Field name made lowercase.
    jun = models.TextField(db_column='Jun', blank=True, null=True)  # Field name made lowercase.
    jul = models.TextField(db_column='Jul', blank=True, null=True)  # Field name made lowercase.
    aug = models.TextField(db_column='Aug', blank=True, null=True)  # Field name made lowercase.
    sep = models.TextField(db_column='Sep', blank=True, null=True)  # Field name made lowercase.
    oct = models.TextField(db_column='Oct', blank=True, null=True)  # Field name made lowercase.
    nov = models.TextField(db_column='Nov', blank=True, null=True)  # Field name made lowercase.
    dec = models.TextField(db_column='Dec', blank=True, null=True)  # Field name made lowercase.
    ave = models.FloatField(db_column='Ave', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'usa_inflation'


class Wallstreetbets(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    rank = models.IntegerField()
    ticker = models.CharField(max_length=10, blank=True, null=True)
    total = models.IntegerField()
    recent = models.IntegerField()
    previous = models.IntegerField()
    change = models.CharField(max_length=10, blank=True, null=True)
    rockets = models.IntegerField()
    posts = models.IntegerField()
    upvotes = models.IntegerField()
    comments = models.IntegerField()
    price = models.CharField(max_length=10, blank=True, null=True)
    one_day_change_percent = models.CharField(max_length=10, blank=True, null=True)
    fifty_day_change_percent = models.CharField(max_length=10, blank=True, null=True)
    volume = models.CharField(max_length=10, blank=True, null=True)
    mkt_cap = models.CharField(max_length=25, blank=True, null=True)
    floating_shares = models.CharField(max_length=10, blank=True, null=True)
    beta = models.CharField(max_length=10, blank=True, null=True)
    short_per_float = models.CharField(max_length=10, blank=True, null=True)
    industry = models.CharField(max_length=100, blank=True, null=True)
    prev_close = models.CharField(max_length=10, blank=True, null=True)
    open = models.CharField(max_length=10, blank=True, null=True)
    day_low = models.CharField(max_length=10, blank=True, null=True)
    day_high = models.CharField(max_length=10, blank=True, null=True)
    target = models.CharField(max_length=10, blank=True, null=True)
    recommend = models.CharField(max_length=20, blank=True, null=True)
    date_updated = models.CharField(max_length=20, blank=True, null=True)
    subreddit = models.CharField(max_length=25, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wallstreetbets'
        unique_together = (('ticker', 'date_updated'),)


class WorldInflation(models.Model):
    country = models.TextField(db_column='Country', blank=True, null=True)  # Field name made lowercase.
    last = models.FloatField(db_column='Last', blank=True, null=True)  # Field name made lowercase.
    previous = models.FloatField(db_column='Previous', blank=True, null=True)  # Field name made lowercase.
    reference = models.TextField(db_column='Reference', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'world_inflation'


class WsbChange(models.Model):
    ticker = models.CharField(max_length=10, blank=True, null=True)
    mentions = models.IntegerField(blank=True, null=True)
    percent_change = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wsb_change'


class WsbDiscussions(models.Model):
    ticker = models.CharField(max_length=10, blank=True, null=True)
    text_body = models.CharField(max_length=500, blank=True, null=True)
    sentiment = models.FloatField(blank=True, null=True)
    date_posted = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wsb_discussions'


class WsbEtf(models.Model):
    ticker = models.CharField(max_length=10, blank=True, null=True)
    open_date = models.CharField(max_length=20, blank=True, null=True)
    open_price = models.CharField(max_length=20, blank=True, null=True)
    close_date = models.CharField(max_length=20, blank=True, null=True)
    close_price = models.CharField(max_length=20, blank=True, null=True)
    percentage = models.CharField(max_length=20, blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wsb_etf'


class WsbTrending24H(models.Model):
    ticker = models.CharField(max_length=10, blank=True, null=True)
    mentions = models.IntegerField(blank=True, null=True)
    sentiment = models.FloatField(blank=True, null=True)
    calls = models.IntegerField(blank=True, null=True)
    puts = models.IntegerField(blank=True, null=True)
    date_updated = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wsb_trending_24h'


class WsbTrendingHourly(models.Model):
    ticker = models.CharField(max_length=10, blank=True, null=True)
    mentions = models.IntegerField(blank=True, null=True)
    sentiment = models.FloatField(blank=True, null=True)
    calls = models.IntegerField(blank=True, null=True)
    puts = models.IntegerField(blank=True, null=True)
    date_updated = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wsb_trending_hourly'


class WsbWordCloud(models.Model):
    word = models.CharField(max_length=100, blank=True, null=True)
    mentions = models.IntegerField(blank=True, null=True)
    date_updated = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wsb_word_cloud'


class WsbYf(models.Model):
    ticker = models.TextField(blank=True, null=True)
    mkt_cap = models.TextField(blank=True, null=True)
    price_change = models.FloatField(blank=True, null=True)
    industry = models.TextField(blank=True, null=True)
    sector = models.TextField(blank=True, null=True)
    difference_sma = models.FloatField(blank=True, null=True)
    difference_52w_high = models.FloatField(blank=True, null=True)
    difference_52w_low = models.FloatField(blank=True, null=True)
    mentions = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wsb_yf'
