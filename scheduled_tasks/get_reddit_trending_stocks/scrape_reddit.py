from scheduled_tasks.get_reddit_trending_stocks.AutoDD import *
from scheduled_tasks.config import *
from collections import Counter


def main():
    print("Getting submissions...")
    for subreddit in subreddits:
        current_scores, current_rocket_scores, prev_scores, prev_rocket_scores = \
            get_submission_generators(interval, subreddit)

        print("Populating results for {}...".format(subreddit))
        results_df = populate_df(current_scores, prev_scores, interval)
        results_df = filter_df(results_df, minimum_score)

        print("Counting rockets for {}...".format(subreddit))
        rockets = Counter(current_rocket_scores) + Counter(prev_rocket_scores)
        results_df.insert(loc=4, column='rockets', value=pd.Series(rockets))
        results_df = results_df.fillna(value=0).astype({'rockets': 'int32'})

        print("Getting financial stats for {}...".format(subreddit))
        results_df = get_financial_stats(results_df, minimum_volume, minimum_mkt_cap, allow_threading)
        print(results_df.columns)
        results_df.sort_values(by=results_df.columns[0], inplace=True, ascending=False)
        print_df(results_df, file_name, save_to_sql, save_to_csv, subreddit)
        print()


if __name__ == '__main__':
    main()
