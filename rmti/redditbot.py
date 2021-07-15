"""An AI application that reads your Myers-Briggs Type Indicator.

This script...
"""

import praw
import pandas as pd
from itertools import cycle
import time
import sys

class RedditBot:
    pass

MBTI_TYPES = ["ISTJ", "ISTP", "ISFJ", "ISFP", "INFJ", "INFP", "INTJ", "INTP", 
            "ESTP", "ESTJ", "ESFP", "ESFJ", "ENFP", "ENFJ", "ENTP", "ENTJ"]
COLS = ["redditor", "type", "text"]

reddit = praw.Reddit('bot1', config_interpolation="basic")

def process_data(subreddit_group, file_name=None):
    users = get_redditors_from_subreddit(subreddit_group)
    data = []
    for user in users:
        type = get_user_type(user)
        if type != "":
            texts = get_user_texts(user)
                
            if texts:
                data.append(list(zip(cycle([user]), cycle([type]), texts)))

    reddit_df = generate_data(data)
    if file_name is not None:
        generate_data_file(reddit_df, file_name)
        return
    return reddit_df

def generate_data(data):
    """Generate a data frame with the given data."""

    if data:
        reddit_data = [item for sublist in data for item in sublist]
        reddit_df = pd.DataFrame(reddit_data, columns=COLS)
        return reddit_df

def generate_data_file(reddit_df, file_name):
    """Generate a data file and save that 
    object as a csv with the name of file_name.
    """

    reddit_df.to_csv('.\data\{}.csv'.format(file_name), index = False, header=True)

def get_redditors_from_subreddit(subreddit_group):
    """Goes through comments of a subreddit and adds the author of 
    the comment to a set of redditors. This is a workaround until we 
    find or use an API that gets all redditors from a subreddit. 
    """

    users = set()
    for comment in reddit.subreddit(subreddit_group).comments(limit=100):
        author = comment.author
        users.add(str(author))
    return users

def get_user_texts(user):
    """Goes through the user's submissions and extracts their text into
    a list of texts.
    """

    texts = []
    for submission in reddit.redditor(user).submissions.new(limit=10):
        if submission.selftext:
            texts.append(submission.selftext)
    
    return texts

def get_user_type(user):
    """Given a user or redditor retruns the user's personality 
    type based off of what the user used as their flair. Since 
    a user may have updated their flair over time this method
    also ensures that it returns only a flair that is in the list of
    MTBTI types. 
    """

    type = ""
    flairs = []
    for submission in reddit.redditor(user).submissions.new(limit=100):
        if submission.author_flair_text in MBTI_TYPES:
            flairs.append(submission.author_flair_text)
    if flairs:
        type = max(set(flairs), key=flairs.count)
    
    return type

if (__name__ == '__main__'):
    time = time.time()

    print("""
    #########################################################################################
    #########################################################################################
    Usage: This script acts to pull everything together and generate 
    a data file.
    Expalain....
    Parameters:
        subreddit_group (string): name of subreddit group to search.
        file_name (string): name of of the file you want to save your data under.
        
    Examples:
        python3 RedditBot.py 'ENFJ' 'test_file'
        python3 RedditBot.py d 'test_file'
        python3 RedditBot.py
    #########################################################################################
    #########################################################################################

        """)

    # Defaults:
    subreddit_group = "ENFJ"
    file_name = "personality_data_{}".format(time)

    # Command line inputs
    if len(sys.argv) > 1:
        if sys.argv[1] != 'd':
            subreddit_group = sys.argv[1]
        if sys.argv[2] != 'd':
            file_name = sys.argv[2]

    print("Generating data...")
    process_data(subreddit_group, file_name)