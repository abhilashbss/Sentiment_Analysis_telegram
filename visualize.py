import pandas as pd


def plot_date_wise_sentiment(agg_df):
    pd.options.plotting.backend = "plotly"
    fig = agg_df.plot()
    fig.show()
