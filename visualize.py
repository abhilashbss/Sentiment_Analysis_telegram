import pandas as pd
import plotly.express as px
import plotly as plt


def plot_date_wise_sentiment_sum(agg_df):
    pd.options.plotting.backend = "plotly"
    agg_df.rename(columns={'count': 'Messages'}, inplace=True)
    plot_df = agg_df.drop(columns=['Average positive score', 'Average negative score', 'Average neutral score',
                                   'Average compound score'])
    fig = plot_df.plot(title="Day wise sentiment score sum")
    fig.show()


def plot_date_wise_sentiment_avg(agg_df):
    pd.options.plotting.backend = "plotly"
    agg_df['Average positive score'] = agg_df['positive_score'] / agg_df['count']
    agg_df['Average negative score'] = agg_df['negative_score'] / agg_df['count']
    agg_df['Average neutral score'] = agg_df['neutral_score'] / agg_df['count']
    agg_df['Average compound score'] = agg_df['compound_score'] / agg_df['count']
    agg_df.rename(columns={'count': 'Messages'}, inplace=True)
    fig = px.bar(agg_df, x=agg_df.index, y=['Average positive score', 'Average negative score',
                                            'Average neutral score', 'Average compound score'],
                 title='Average sentiment per day')
    fig.show()


def plot_date_wise_message_count(agg_df):
    pd.options.plotting.backend = "plotly"
    agg_df.rename(columns={'count': 'Messages'}, inplace=True)
    fig = px.bar(agg_df, x=agg_df.index, y=['Messages'], title='Day wise message count')
    fig.show()
