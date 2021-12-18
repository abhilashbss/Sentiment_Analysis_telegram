import json
from tqdm import tqdm
import utils
import preprocess
import pandas as pd
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import visualize


def get_processed_telegram_messages(telegram_msg_path, filter_list):
    file_contents = utils.get_file_contents(telegram_msg_path)
    message_json = json.loads(file_contents)
    messages_df = pd.json_normalize(message_json['messages'])
    messages_df.sort_values('date')
    messages_df['date_without_time'] = pd.to_datetime(messages_df['date']).dt.date
    pd.set_option("display.max_rows", None, "display.max_columns", None)
    messages_df['positive_score'] = 0.0
    messages_df['negative_score'] = 0.0
    messages_df['neutral_score'] = 0.0
    messages_df['compound_score'] = 0.0
    sid = SentimentIntensityAnalyzer()
    words = set(nltk.corpus.words.words())
    indexes_to_delete = []

    for ind in tqdm(messages_df.index):
        cleaned_message = preprocess.clean_text(str(messages_df['text'][ind]))
        if not preprocess.is_topic_filter(cleaned_message, filter_list):
            indexes_to_delete.append(ind)
            continue
        message = preprocess.remove_non_english_words(cleaned_message, words)
        sentiment_dict = sid.polarity_scores(message)
        messages_df.at[ind, 'positive_score'] = sentiment_dict['pos']
        messages_df.at[ind, 'negative_score'] = sentiment_dict['neg']
        messages_df.at[ind, 'neutral_score'] = sentiment_dict['neu']
        messages_df.at[ind, 'compound_score'] = sentiment_dict['compound']

    return messages_df.drop(index=indexes_to_delete)


def generate_date_wise_sentiment(messages_df):
    messages_df['count'] = 1
    to_be_agg = messages_df[['positive_score', 'negative_score', 'neutral_score', 'date_without_time', 'count']]
    to_be_agg.rename(columns={'date_without_time': 'date'}, inplace=True)
    agg_df = to_be_agg.set_index('date') \
        .groupby('date').sum()
    return agg_df


if __name__ == '__main__':
    nltk.download('words')
    nltk.downloader.download('vader_lexicon')
    processed_messages = get_processed_telegram_messages('/home/abhilashbss/PycharmProjects'
                                                         '/Message_sentiment_analysis/data/result.json',
                                                         ["shib", "doge"])

    filtered = processed_messages.loc[(processed_messages['positive_score'] == 0.0)
                                      & (processed_messages['negative_score'] == 0.0)
                                      & (processed_messages['neutral_score'] == 0.0)]
    aggregated_sentiments = generate_date_wise_sentiment(processed_messages)
    visualize.plot_date_wise_sentiment(aggregated_sentiments)

