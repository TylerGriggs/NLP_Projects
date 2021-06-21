"""
@author: Tyler Griggs

The Program runs in the command line to pull YouTube comments about a topic, and allows the
    user to manually tag them with a positive or negative sentiment for training.
    NEED TO PROVIDE A VALID YOUTUBE API IN THE SCRIPT BELOW, "api_key"

Instructions:
    The user will enter two command line arguments. The first is the term of which
    returned tweets will contain. The second argument is the number of videos from the search
    to load into the dictionary, provided by youtube_api package.

    argv[1]         Topic or "search string for results"
    argv[2]         Integer of pages to return

Comments will be displayed one at a time, waiting for the user to input the
    sentiment associated with the comment, or skip it for a number of reasons.

    1               Positive Sentiment
    2               Negative Sentiment
    e               Exit the script, saving the tagged tweets to a file
    [any input]     Skips the current comment

Examples:
    python yt_comments.py "food travel city" 2
    python yt_comments.py "apple iphone" 10

    The #IPhoneSE is a genius move by Apple.
    1
    Positve

Saved Format:
    <instance>
    <id>1251572470609580034</id>
    <sentiment>positive</sentiment>
    <context>The #IPhoneSE is a genius move by #Apple.</context>
    <\instance>

"""

from sys import argv
from youtube_api import YouTubeDataAPI

api_key = 'YOUTUBE_API_KEY_GOES_HERE'
yt = YouTubeDataAPI(api_key)

topic = str(argv[1])
num_videos = int(argv[2])

videos = yt.search(topic, max_results=num_videos)

print('YouTube Manual Sentiment Tagger')
print('Enter "1" for Positive. Enter "2" for Negative, Enter "e" to EXIT, anything else will SKIP the current Tweet.')

# Supervised Training File Output
f = open('youtube_tagging.txt', 'a+')

for video in videos:
    try:
        comment_data = yt.get_video_comments(video['video_id'], get_replies=False, max_results=10)
    except:
        print('Could not retrieve YouTube comment data for video: ' + str(video))
    for comment in comment_data:
        text = str(comment['text'])
        userInput = input(text + '\n')

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
        f.write('<id>' + str(comment['comment_id']) + '</id>\n')
        f.write('<sentiment>' + sentiment + '</sentiment>\n')
        f.write('<context>' + str(text.encode('utf-8')) + '</context>\n')
        f.write('<likes>' + str(comment['comment_like_count']) + '</likes>\n')
        f.write('<\instance>\n\n')

f.close()