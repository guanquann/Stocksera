###############################################################################
# REDDIT PRAW CREDENTIALS
# Register for an API in https://www.reddit.com/prefs/apps and enter credential
###############################################################################
API_REDDIT_CLIENT_ID = "API_KEY_HERE"
API_REDDIT_CLIENT_SECRET = "API_KEY_HERE"
API_REDDIT_USER_AGENT = "subreddit_scraper"

################################################
# CONFIG FOR SCRAPING TRENDING TICKERS ON REDDIT
################################################
# Time interval in hours to filter the results, default is 24 hours
interval = 24

# Choose subreddits to search for tickers
# Type: list
subreddits = ["wallstreetbets", "stocks", "options", "pennystocks", "investing", "shortsqueeze", "spacs"]

# Filter out results that have less than the min score
# Type: list, where the index of minimum_score correspond to subreddits list
minimum_score = [5, 5, 5, 5, 5, 5, 5]

# Number of posts to read from each subreddit. This depends on your time interval set above.
# 300 should be more than enough
# Type: list, where the index of num_posts correspond to subreddits list
num_posts = [500, 500, 500, 500, 500, 500, 500]

# Minimum volume of ticker
# Type: list, where the index of minimum_volume correspond to subreddits list
minimum_volume = [1000000, 1000000, 1000000, 1000000, 500000, 500000, 300000]

# Minimum market cap of company
# Type: list, where the index of minimum_mkt_cap correspond to subreddits list
minimum_mkt_cap = [1000000000, 1000000000, 1000000000, 500000000, 20000000, 200000000, 1000000]

# Disable multi-tasking (enabled by default). Multi-tasking speeds up downloading of data.
allow_threading = True

# Saves to SQL database if it is true
save_to_sql = True

# Saves to a csv file if it is true
save_to_csv = False
file_name = "test"
