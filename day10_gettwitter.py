#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys,csv,json,datetime
import twitter
import prettyprint

twkey = {
        "cons_key": "Olb7J6GWBBji4Pm5NtseUCien",
        "cons_sec": "NqTtUN6J9ZvMAuTZjmKgGchZXhDTpY7cIpwfLeq4G9dKJF0cgd",
        "accto_key": "2905290386-nMVnHG44q9TASP95JLET2HC8DMIESTLMbOqTdwR",
        "accto_sec": "M7w1X2xyxfOnZZPTRpbpt2vpSkInL9XbGfvbvifaAVX6q"
}

CONSUMER_KEY = twkey['cons_key']
CONSUMER_SECRET = twkey['cons_sec']
ACCESS_TOKEN_KEY = twkey['accto_key']
ACCESS_TOKEN_SECRET = twkey['accto_sec']

maxcount=1000000
maxid=0
search_str="妄想キャリブレーション OR 妄キャリ -rt"
#search_str="to:%s AND 好き -rt"%(twitter_id)

api = twitter.Api(consumer_key=CONSUMER_KEY,
                  consumer_secret=CONSUMER_SECRET,
                  access_token_key=ACCESS_TOKEN_KEY,
                  access_token_secret=ACCESS_TOKEN_SECRET)

tweets = api.GetSearch(term=search_str,count=100,result_type='recent')

csv_out=open('tweet_moso.csv', mode='w')
writer=csv.writer(csv_out)

fields=['created_at', 'text', 'screen_name', 'followers', 'friends', 'rt', 'fav']
writer.writerow(fields)

for line in tweets:
    writer.writerow([line.created_at_in_seconds,
                     line.text.encode('utf-8'),
                     line.user.screen_name,
                     line.user.followers_count,
                     line.user.friends_count,
                     line.retweet_count,
                     line.favorite_count])


i=0
while True:
  for f in tweets:
    if maxid > f.id or maxid == 0:
      maxid = f.id
    #print f.text
    i = i + 1
  if len(tweets) == 0:
    break
  if maxcount <= i:
    break
  #print maxid
  tweets = api.GetSearch(term=search_str,count=100,result_type='recent',max_id=maxid-1)
  for line in tweets:
      writer.writerow([line.created_at_in_seconds,
                       line.text.encode('utf-8'),
                       line.user.screen_name,
                       line.user.followers_count,
                       line.user.friends_count,
                       line.retweet_count,
                       line.favorite_count])
      
#print len(result_date)

csv_out.close()

