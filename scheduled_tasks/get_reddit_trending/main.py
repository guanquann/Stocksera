import argparse
from scheduled_tasks.get_reddit_trending.AutoDD import *
from collections import Counter


def main():
    # Instantiate the parser
    parser = argparse.ArgumentParser(description='AutoDD Optional Parameters')

    parser.add_argument('--interval', nargs='?', const=48, type=int, default=24,
                        help='Choose a time interval in hours to filter the results, default is 24 hours')

    parser.add_argument('--sub', nargs='?', const='wallstreetbets', type=str, default='wallstreetbets',
                        help='Choose a different subreddit to search for tickers in, default is wallstreetbets')

    parser.add_argument('--min', nargs='?', const=30, type=int, default=30,
                        help='Filter out results that have less than the min score, default is 30')

    parser.add_argument('--sort', nargs='?', const=1, type=int, default=1,
                        help='Sort the results table by descending order of score, 1 = sort by total score, '
                             '2 = sort by recent score, 3 = sort by previous score, 4 = sort by change in score, '
                             '5 = sort by # of rocket emojis')

    parser.add_argument('--allsub', default=False, action='store_true',
                        help='Using this parameter searches from one subreddit only, '
                             'default subreddit is r/wallstreetbets.')

    parser.add_argument('--psaw', default=True, action='store_true',
                         help='Using this parameter selects psaw (push-shift) as the reddit scraper over praw '
                              '(reddit-api)')

    parser.add_argument('--no-threads', action='store_false', dest='threads',
                        help='Disable multi-tasking (enabled by default). Multi-tasking speeds up downloading of data.')

    parser.add_argument('--csv', default=True, action='store_true',
                        help='Using this parameter produces a table_records.csv file, rather than a .txt file')

    parser.add_argument('--filename', nargs='?', const='table_records', type=str, default='table_records_test',
                        help='Change the file name from table_records to whatever you wish')

    args = parser.parse_args()

    print("Getting submissions...")
    # call reddit api to get results
    current_scores, current_rocket_scores, current_positive, current_negative, prev_scores, prev_rocket_scores, prev_positive, prev_negative = get_submission_generators(args.interval, args.sub, args.allsub, args.psaw)

    print("Populating results...")
    results_df = populate_df(current_scores, prev_scores, args.interval)
    results_df = filter_df(results_df, args.min)

    print("Counting rockets...")
    rockets = Counter(current_rocket_scores) + Counter(prev_rocket_scores)
    results_df.insert(loc=4, column='rockets', value=pd.Series(rockets))
    results_df = results_df.fillna(value=0).astype({'rockets': 'int32'})

    positive = Counter(current_positive) + Counter(prev_positive)
    results_df.insert(loc=5, column='positive', value=pd.Series(positive))
    results_df = results_df.fillna(value=0).astype({'positive': 'int32'})

    negative = Counter(current_negative) + Counter(prev_negative)
    results_df.insert(loc=6, column='negative', value=pd.Series(negative))
    results_df = results_df.fillna(value=0).astype({'negative': 'int32'})

    print("Getting financial stats...")
    results_df = get_financial_stats(results_df, args.threads)

    # Sort by Total (sort = 1), Recent (sort = 2), Prev (sort = 3), Change (sort = 4), Rockets (sort = 5)
    results_df.sort_values(by=results_df.columns[args.sort - 1], inplace=True, ascending=False)

    print_df(results_df, args.filename, args.csv, args.sub, args.allsub)


if __name__ == '__main__':
    main()
