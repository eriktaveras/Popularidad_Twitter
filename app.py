import tweepy
from textblob import TextBlob
from typing import List

consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""

class TwitterClient:
    def __init__(self):
        try:
            self.auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
            self.auth.set_access_token(access_token, access_token_secret)
            self.api = tweepy.API(self.auth)
        except tweepy.TweepError:
            print("Error: Authentication Failed")

    def clean_tweet(self, tweet: str) -> str:
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def get_tweet_sentiment(self, tweet: str) -> str:
        analysis = TextBlob(self.clean_tweet(tweet))
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'

    def get_tweets(self, query: str, count: int = 10) -> List[dict]:
        tweets = []
        try:
            fetched_tweets = self.api.search(q=query, count=count)
            for tweet in fetched_tweets:
                parsed_tweet = {}
                parsed_tweet['text'] = tweet.text
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)
                tweets.append(parsed_tweet)
            return tweets
        except tweepy.TweepError as e:
            print(f"Error: {e}")
            return tweets

def main():
    query = input("Input Search: ")
    api = TwitterClient()
    tweets = api.get_tweets(query, count=200)

    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
    print(f"Positive tweets percentage: {100*len(ptweets)/len(tweets)}%")
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
    print(f"Negative tweets percentage: {100*len(ntweets)/len(tweets)}%")
    print(f"Neutral tweets percentage: {100*(len(tweets) - len(ntweets) - len(ptweets))/len(tweets)}%")

    print("\n\nPositive tweets:")
    for tweet in ptweets[:10]:
        print(tweet['text'])

    print("\n\nNegative tweets:")
    for tweet in ntweets[:10]:
        print(tweet['text'])

if __name__ == "__main__":
