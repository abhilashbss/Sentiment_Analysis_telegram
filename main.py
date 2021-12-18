import nltk
import visualize
import sentiment_analysis
import preprocess

if __name__ == '__main__':
    nltk.download('words')
    nltk.downloader.download('vader_lexicon')
    analyzer = sentiment_analysis.SentimentAnalysis('/home/abhilashbss/PycharmProjects'
                                                    '/Message_sentiment_analysis/data/result.json',
                                                    ["shib", "doge"])
    processed_messages = analyzer.get_processed_telegram_messages()
    aggregated_sentiments = analyzer.generate_date_wise_sentiment()
    analyzer.print_stats()
    visualize.plot_date_wise_sentiment_avg(aggregated_sentiments)
    visualize.plot_date_wise_sentiment_sum(aggregated_sentiments)
    visualize.plot_date_wise_message_count(aggregated_sentiments)
