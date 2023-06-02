import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "../../../"))
from scheduled_tasks.reddit.stocks.AutoDD import *

# CONFIG FOR SCRAPING TRENDING POSTS ON REDDIT
# Time interval in hours to filter the results, default is 24 hours
interval = 24

# Choose subreddits to search for tickers
# Type: list
subreddits = ["wallstreetbets", "stocks", "options", "pennystocks", "shortsqueeze", "spacs"]

# Filter out results that have less than the min score
# Type: list, where the index of minimum_score correspond to subreddits list
minimum_score = [5, 5, 5, 5, 5, 5]

# Number of posts to read from each subreddit. This depends on your time interval set above.
# 300 should be more than enough
# Type: list, where the index of num_posts correspond to subreddits list
num_posts = [1000, 500, 500, 500, 1000, 500]

# Minimum volume of ticker
# Type: list, where the index of minimum_volume correspond to subreddits list
minimum_volume = [1000000, 1000000, 1000000, 1000000, 500000, 300000]

# Minimum market cap of company
# Type: list, where the index of minimum_mkt_cap correspond to subreddits list
minimum_mkt_cap = [1000000000, 1000000000, 1000000000, 500000000, 200000000, 1000000]

# Disable multi-tasking (enabled by default). Multi-tasking speeds up downloading of data.
allow_threading = True

# Saves to SQL database if it is true
save_to_sql = True

# Saves to a csv file if it is true
save_to_csv = False
file_name = "test"


def main():
    print("Getting Reddit Stocks Trending Post...")
    for index, subreddit in enumerate(subreddits):
        current_scores, prev_scores, total_rocket_score, total_posts_score, \
            total_upvotes_score, total_comments_score = get_submission_generators(interval, subreddit,
                                                                                  n_num=num_posts[index])

        results_df = populate_df(current_scores, prev_scores, interval)
        results_df = filter_df(results_df, minimum_score[index])

        results_df.insert(loc=4, column='rockets', value=pd.Series(total_rocket_score))
        results_df.insert(loc=5, column='posts', value=pd.Series(total_posts_score))
        results_df.insert(loc=6, column='upvotes', value=pd.Series(total_upvotes_score))
        results_df.insert(loc=7, column='comments', value=pd.Series(total_comments_score))

        results_df = get_financial_stats(results_df, minimum_volume[index], minimum_mkt_cap[index], allow_threading)
        results_df.sort_values(by=results_df.columns[0], inplace=True, ascending=False)
        print("Reddit Stocks Trending Post Successfully Completed...\n")


if __name__ == '__main__':
    main()
