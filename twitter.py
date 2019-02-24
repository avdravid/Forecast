#!/usr/bin/env python3
import tweepy, cgitb
import numpy as np
from text_analysis import TextAnalyzer

cgitb.enable(display=0, logdir="/home/ubuntu/workspace/logs")

class Twitter:
    def __init__(self, num, name):
        self.auth = tweepy.OAuthHandler('5SlnMghNlVoWI3UcobXYUrau5', '0VNq9Tq9sDX9BTFZm0yAyGJfUTFgLEEye3A0MU7stRgB4XkKj7')
        self.auth.set_access_token('2664657090-9pjisTaiJvw6O1XSrevOt5VcQEpoIQbDwUZdVVu',  'bHmUC6Ef6IezYLpi3Grm43fk2czMZNk8O8mkPZ4QEu7b0')
        self.api = tweepy.API(self.auth)
        self.name = name
        self.num = int(num)
        
        
    def retrieve(self):
        tweet_list = []
        url_list = []
        new_tweets = self.api.user_timeline(screen_name = self.name, count=self.num, tweet_mode="extended")
        for tweet in new_tweets:
            tweet_list.append(tweet.full_text)
            try:
                url_list.append(tweet.entities['media'][0]['media_url'])
            except (NameError, KeyError):
                pass
        return tweet_list
    
    def getData(self):
        if self.num > 0:
            category_list = []
            number_list = []
            for tweet in self.retrieve():
                text_analyzer = TextAnalyzer(tweet)
                (category, number) = text_analyzer.run()
                if category != 0:
                    category_list.append(category)
                number_list.append(number)
            avg = np.mean(number_list)
            if len(category_list) != 0:
                d = {x:category_list.count(x) for x in category_list}
                key_max = max(d.keys(), key=(lambda k: d[k]))
                result = d[key_max] * avg
            else:
                result = avg
                key_max = 0
            if self.name == "MSoloBot":
                url = "https://pbs.twimg.com/media/D0LUK9NXQAEK8bB.png:large"
            else:
                url = ""
            return (result, key_max, self.retrieve(), url)
        else:
            return (0, 0, 0, '')