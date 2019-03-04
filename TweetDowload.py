import tweepy
from tweepy import OAuthHandler
import matplotlib.pyplot as plt
import csv
from os import chdir

# Enviroment settings
ProjectPath = "D:/Google_Drive/Master/Dgp/DGP_Proj_Code"
consumer_key = ''
consumer_secret = ''
access_token = '-'
access_token_secret = ''

class TwitterClient(object):
    def __init__(self):

        try:
            self.auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
            self.auth.set_access_token(access_token, access_token_secret)
            self.api = tweepy.API(self.auth)
        except:
            print("Error: Authentication Failed")

    def get_tweets(self, query, count = 120):
        tweets = []
        try:
            #Es necesario poner tweet_mode = extended sino aparece el texto cortado
            fetched_tweets = self.api.search(q = query, count = count, tweet_mode='extended')
            for tweet in fetched_tweets:

                parsed_tweet = {}
                parsed_tweet['retweets'] = tweet.retweet_count
                parsed_tweet['id'] = tweet.id_str
                parsed_tweet['likes'] = tweet.favorite_count
                parsed_tweet['date'] = tweet.created_at
                parsed_tweet['text'] = tweet.full_text
                parsed_tweet['followers_count'] = tweet.user.followers_count
                parsed_tweet['screen_name'] = tweet.user.screen_name
                parsed_tweet['user_since'] = tweet.user.created_at
                
                # Solamente nos quedamos aquellos que NO son retweets porque sino no tenemos el full text
                if tweet.retweet_count > 0:
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)
            return tweets

        except tweepy.TweepError as e:
            print("Error : " + str(e))

def main():

    api = TwitterClient()
    
    chdir(ProjectPath+"/Inbox")

    #EMTVALENCIA
    tweets = api.get_tweets(query = 'busvalencia OR emtvalencia OR grezzi OR giussepegrezzi OR transitvalencia OR transitovalencia -filter:retweets', count = 100)    
    #csvFile = open('D:/Google_Drive/Master/Dgp/DGP_Proj_Code/Inbox/emtvalencia_online.csv', 'w', newline='')
    csvFile = open('emtvalencia_online.csv', 'w', newline='', encoding='utf-8')
    csvWriter = csv.writer(csvFile, quoting = csv.QUOTE_MINIMAL)
    csvWriter.writerow(['Twitter Query: emt valencia -filter:retweets,'])
    csvWriter.writerow(['Date','Screen Name','Full Name','Tweet Text','Tweet ID','Link(s)','Media','Location','Retweets','Favorites','App','Followers','Follows','Listed','Verfied','User Since','Location','Bio','Website','Timezone','Profile Image'])
        
    for tweet in tweets:
        csvWriter.writerow([tweet['date'], "@"+tweet['screen_name'], 'null', tweet['text'], tweet['id'], 'null', 'null', 'null', tweet['retweets'], tweet['likes'], 'null', tweet['followers_count'], 'null', 'null', tweet['user_since'], 'null', 'null', 'null', 'null', 'null'])
        #print("Tweet: ",tweet['retweets'], tweet['id'], tweet['date'], tweet['text'], tweet['followers_count'], tweet['screen_name'], tweet['user_since'])

    csvFile.close()

    #METROVALENCIA
    tweets = api.get_tweets(query = 'metro valencia -filter:retweets', count = 100)    
    #csvFile = open('D:/Google_Drive/Master/Dgp/DGP_Proj_Code/Inbox/metrovalencia_online.csv', 'w', newline='')
    csvFile = open('metrovalencia_online.csv', 'w', newline='', encoding='utf-8')
    csvWriter = csv.writer(csvFile, quoting = csv.QUOTE_MINIMAL)
    csvWriter.writerow(['Twitter Query: metro valencia -filter:retweets,'])
    csvWriter.writerow(['Date','Screen Name','Full Name','Tweet Text','Tweet ID','Link(s)','Media','Location','Retweets','Favorites','App','Followers','Follows','Listed','Verfied','User Since','Location','Bio','Website','Timezone','Profile Image'])
        
    for tweet in tweets:
        csvWriter.writerow([tweet['date'], "@"+tweet['screen_name'], 'null', tweet['text'], tweet['id'], 'null', 'null', 'null', tweet['retweets'], tweet['likes'], 'null', tweet['followers_count'], 'null', 'null', tweet['user_since'], 'null', 'null', 'null', 'null', 'null'])
        #print("Tweet: ",tweet['retweets'], tweet['id'], tweet['date'], tweet['text'], tweet['followers_count'], tweet['screen_name'], tweet['user_since'])

    csvFile.close()

    #VALENBISI
    tweets = api.get_tweets(query = 'valenbisi -filter:retweets', count = 100)    
    #csvFile = open('D:/Google_Drive/Master/Dgp/DGP_Proj_Code/Inbox/valenbisi_online.csv', 'w', newline='')
    csvFile = open('valenbisi_online.csv', 'w', newline='', encoding='utf-8')
    csvWriter = csv.writer(csvFile, quoting = csv.QUOTE_MINIMAL)
    csvWriter.writerow(['Twitter Query: valenbisi -filter:retweets,'])
    csvWriter.writerow(['Date','Screen Name','Full Name','Tweet Text','Tweet ID','Link(s)','Media','Location','Retweets','Favorites','App','Followers','Follows','Listed','Verfied','User Since','Location','Bio','Website','Timezone','Profile Image'])
        
    for tweet in tweets:
        csvWriter.writerow([tweet['date'], "@"+tweet['screen_name'], 'null', tweet['text'], tweet['id'], 'null', 'null', 'null', tweet['retweets'], tweet['likes'], 'null', tweet['followers_count'], 'null', 'null', tweet['user_since'], 'null', 'null', 'null', 'null', 'null'])
        #print("Tweet: ",tweet['retweets'], tweet['id'], tweet['date'], tweet['text'], tweet['followers_count'], tweet['screen_name'], tweet['user_since'])

    csvFile.close()
    
if __name__ == "__main__":
    main()
