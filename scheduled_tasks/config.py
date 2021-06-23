# PRAW credentials
# Register for an API in https://www.reddit.com/prefs/apps and enter credential
API_REDDIT_CLIENT_ID = "YOUR_OWN_API"
API_REDDIT_CLIENT_SECRET = "YOUR_OWN_API"
API_REDDIT_USER_AGENT = "subreddit_scraper"

# Time interval in hours to filter the results, default is 24 hours
interval = 24

# Choose a different subreddit to search for tickers in, default is wallstreetbets, stocks, stockmarket,
subreddits = ["wallstreetbets", "stocks", "stockmarket"]

# Filter out results that have less than the min score
minimum_score = 20

# Minimum volume of ticker
minimum_volume = 1200000

# Minimum market cap of company
minimum_mkt_cap = 1000000000

# Disable multi-tasking (enabled by default). Multi-tasking speeds up downloading of data.
allow_threading = True

# Saves to SQL database if it is true
save_to_sql = True

# Saves to a csv file if it is true
save_to_csv = False
file_name = "test"
