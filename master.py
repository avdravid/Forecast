#!/usr/bin/env python3

import cgi,cgitb, json
from text_analysis import TextAnalyzer
from twitter import Twitter
cgitb.enable(display=0, logdir="/home/ubuntu/workspace/logs")

#get data from HTTP request
data = cgi.FieldStorage()
#find 'results' key-pair
count = data['count'].value
user = data['user'].value

t = Twitter(count, user)
#creates twitter object and passes in # tweets with username

(number, category, posts, url) = t.getData()
#data retrieval

print("Content-type: text/html\n")
print(json.dumps({
    'category': category, 
    'number': round(number*5),
    'posts': posts,
    'gun_url': url
}))
#print results

