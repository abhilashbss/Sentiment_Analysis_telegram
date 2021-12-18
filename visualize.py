import pandas as pd
import plotly.express as px


def plot_date_wise_sentiment_sum(agg_df):
    pd.options.plotting.backend = "plotly"
    agg_df.rename(columns={'count': 'Messages'}, inplace=True)
    fig = agg_df.plot()
    fig.show()


def plot_date_wise_sentiment_avg(agg_df):
    pd.options.plotting.backend = "plotly"
    agg_df['Average positive score'] = agg_df['positive_score'] / agg_df['count']
    agg_df['Average negative score'] = agg_df['negative_score'] / agg_df['count']
    agg_df['Average neutral score'] = agg_df['neutral_score'] / agg_df['count']
    agg_df['Average compound score'] = agg_df['compound_score'] / agg_df['count']
    agg_df.rename(columns={'count': 'Messages'}, inplace=True)
    fig = px.bar(agg_df, x=agg_df.index, y=['Average positive score', 'Average negative score',
                                            'Average neutral score', 'Average compound score'])
    fig.show()


def plot_date_wise_message_count(agg_df):
    pd.options.plotting.backend = "plotly"
    agg_df.rename(columns={'count': 'Messages'}, inplace=True)
    fig = px.bar(agg_df, x=agg_df.index, y=['Messages'])
    fig.show()
