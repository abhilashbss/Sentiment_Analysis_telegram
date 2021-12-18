import json
from tqdm import tqdm
import utils
import preprocess
import pandas as pd
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer


class SentimentAnalysis:

    def __init__(self, json_path, filter_list):
        self.json_path = json_path
        self.filter_list = filter_list
        self.messages_df = None
        self.date_wise_agg_df = None

    def get_processed_telegram_messages(self):
        file_contents = utils.get_file_contents(self.json_path)
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
            if not preprocess.is_topic_filter(cleaned_message, self.filter_list):
                indexes_to_delete.append(ind)
                continue
            message = preprocess.remove_non_english_words(cleaned_message, words)
            sentiment_dict = sid.polarity_scores(message)
            messages_df.at[ind, 'positive_score'] = sentiment_dict['pos']
            messages_df.at[ind, 'negative_score'] = sentiment_dict['neg']
            messages_df.at[ind, 'neutral_score'] = sentiment_dict['neu']
            messages_df.at[ind, 'compound_score'] = sentiment_dict['compound']

        self.messages_df = messages_df.drop(index=indexes_to_delete)
        return self.messages_df

    def generate_date_wise_sentiment(self):
        self.messages_df['count'] = 1
        to_be_agg = self.messages_df[
            ['positive_score', 'negative_score', 'neutral_score', 'compound_score', 'date_without_time', 'count']]
        to_be_agg.rename(columns={'date_without_time': 'date'}, inplace=True)
        agg_df = to_be_agg.set_index('date') \
            .groupby('date').sum()
        self.date_wise_agg_df = agg_df
        return self.date_wise_agg_df

    def print_stats(self):
        print("Messages processed: ", len(self.messages_df.index))

