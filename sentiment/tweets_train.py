"""
@author: Tyler Griggs

The Program runs in the command line to pull tweets about a term, and allows the
    user to manually tag them with a positive or negative sentiment.

Instructions:
    The user will enter two command line arguments. The first is the term of which
    returned tweets will contain. The second argument is the number of pages of
    tweets to load into the TWEET dictionary, provided by twitter_scraper.

    argv[1]         User or Hashtag
    argv[2]         Integer of pages to return

Tweets will be displayed one at a time, waiting for the user to input the
    sentiment associated with the tweet, or skip it for a number of reasons.

    1               Positive Sentiment
    2               Negative Sentiment
    e               Exit the script, saving the tagged tweets to a file
    [any input]     Skips the current tweet

Examples:
    python tweets.py elonmusk 2
    python tweets.py #apple 10

    The #IPhoneSE is a genius move by Apple.
    1
    Positve

    <instance>
    <id>1251572470609580034</id>
    <sentiment>positive</sentiment>
    <context>The #IPhoneSE is a genius move by #Apple.</context>
    <\instance>
"""

from sys import argv
import twitter_scraper as ts

term1 = str(argv[1])
term2 = int(argv[2])

print('Twitter Manual Sentiment Tagger')
print('Enter "1" for Positive. Enter "2" for Negative, Enter "e" to EXIT, anything else will SKIP the current Tweet.')

# Supervised Training File Output
f = open('angel.txt', 'a+')

tweets = ts.get_tweets(term1, pages=term2)
for tweet in tweets:
    if not tweet['isRetweet']:

        userInput = input(str(tweet['text']) + '\n')

        if userInput == '1':
            sentiment = 'positive'
            print('Positive')
        elif userInput == '2':
            sentiment = 'negative'
            print('Negative')
        elif userInput == 'e':
            break
        else:
            print('SKIPPED')
            continue

        f.write('<instance>\n')
        f.write('<id>' + str(tweet['tweetId']) + '</id>\n')
        f.write('<sentiment>' + sentiment + '</sentiment>\n')
        f.write('<context>' + str(tweet['text']) + '</context>\n')
        f.write('<\instance>\n\n')

f.close()
