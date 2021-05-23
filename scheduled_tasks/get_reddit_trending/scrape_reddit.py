from scheduled_tasks.get_reddit_trending.AutoDD import *
from scheduled_tasks.config import *
from collections import Counter


def main():
    print("Getting submissions...")
    for subreddit in subreddits:
        current_scores, current_rocket_scores, current_positive, current_negative, prev_scores, prev_rocket_scores, \
            prev_positive, prev_negative = get_submission_generators(interval, subreddit)

        print("Populating results for {}...".format(subreddit))
        results_df = populate_df(current_scores, prev_scores, interval)
        results_df = filter_df(results_df, minimum_score)

        print("Counting rockets for {}...".format(subreddit))
        rockets = Counter(current_rocket_scores) + Counter(prev_rocket_scores)
        results_df.insert(loc=4, column='rockets', value=pd.Series(rockets))
        results_df = results_df.fillna(value=0).astype({'rockets': 'int32'})

        positive = Counter(current_positive) + Counter(prev_positive)
        results_df.insert(loc=5, column='positive', value=pd.Series(positive))
        results_df = results_df.fillna(value=0).astype({'positive': 'int32'})

        negative = Counter(current_negative) + Counter(prev_negative)
        results_df.insert(loc=6, column='negative', value=pd.Series(negative))
        results_df = results_df.fillna(value=0).astype({'negative': 'int32'})

        print("Getting financial stats for {}...".format(subreddit))
        results_df = get_financial_stats(results_df, minimum_volume, minimum_mkt_cap, allow_threading)

        results_df.sort_values(by=results_df.columns[1], inplace=True, ascending=False)

        print_df(results_df, file_name, save_to_csv, subreddit)


if __name__ == '__main__':
    main()
