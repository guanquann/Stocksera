from scheduled_tasks.get_reddit_trending_stocks.AutoDD import *
from scheduled_tasks.config import *


def main():
    print("Getting submissions...")
    for index, subreddit in enumerate(subreddits):
        current_scores, prev_scores, total_rocket_score, total_posts_score, \
            total_upvotes_score, total_comments_score = get_submission_generators(interval, subreddit)

        print("Populating results for {}...".format(subreddit))
        results_df = populate_df(current_scores, prev_scores, interval)
        results_df = filter_df(results_df, minimum_score[index])

        print("Counting rockets, posts, upvotes, comments for {}...".format(subreddit))
        results_df.insert(loc=4, column='rockets', value=pd.Series(total_rocket_score))
        results_df.insert(loc=5, column='posts', value=pd.Series(total_posts_score))
        results_df.insert(loc=6, column='upvotes', value=pd.Series(total_upvotes_score))
        results_df.insert(loc=7, column='comments', value=pd.Series(total_comments_score))

        print("Getting financial stats for {}...".format(subreddit))
        results_df = get_financial_stats(results_df, minimum_volume[index], minimum_mkt_cap[index], allow_threading)
        print(results_df.columns)
        results_df.sort_values(by=results_df.columns[0], inplace=True, ascending=False)
        print_df(results_df, file_name, save_to_sql, save_to_csv, subreddit)
        print()


if __name__ == '__main__':
    main()
