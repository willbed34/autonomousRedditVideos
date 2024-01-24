import os
import re
import praw
import markdown_to_text
import time
from videoscript import VideoScript
import configparser
import random

config = configparser.ConfigParser()
config.read('config.ini')
CLIENT_ID = config["Reddit"]["CLIENT_ID"]
CLIENT_SECRET = config["Reddit"]["CLIENT_SECRET"]
USER_AGENT = config["Reddit"]["USER_AGENT"]
SUBREDDIT = config["Reddit"]["SUBREDDIT"]
MAX_WORDS_PER_COMMENT = int(config["Comments"]["MaxLength"])
MIN_WORDS_PER_COMMENT = int(config["Comments"]["MinLength"])
NUMBER_COMMENTS = int(config["Comments"]["NumberComments"])

def getContent(outputDir, postOptionCount) -> VideoScript:
    reddit = __getReddit()
    existingPostIds = __getExistingPostIds(outputDir)

    now = int(time.time())
    autoSelect = postOptionCount == 0
    posts = []
    for submission in reddit.subreddit(SUBREDDIT).top(time_filter="week", limit=postOptionCount*3 + 1):
        # if (f"{submission.id}.mp4" in existingPostIds or submission.over_18):
        if (f"{submission.id}.mp4" in existingPostIds):
            continue
        hoursAgoPosted = (now - submission.created_utc) / 3600
        print(f"[{len(posts)}] {submission.title}     {submission.score}    {'{:.1f}'.format(hoursAgoPosted)} hours ago")
        posts.append(submission)
        if (autoSelect or len(posts) >= postOptionCount):
            break

    if (autoSelect):
        return __getContentFromPost(posts[0])
    else:
        postSelection = int(input("Input: "))
        selectedPost = posts[postSelection]
        return __getContentFromPost(selectedPost)

def getContentFromId(outputDir, submissionId) -> VideoScript:
    reddit = __getReddit()
    existingPostIds = __getExistingPostIds(outputDir)
    
    if (submissionId in existingPostIds):
        print("Video already exists!")
        exit()
    try:
        submission = reddit.submission(submissionId)
    except:
        print(f"Submission with id '{submissionId}' not found!")
        exit()
    return __getContentFromPost(submission)

def __getReddit():
    return praw.Reddit(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        user_agent=USER_AGENT
    )


def __getContentFromPost(submission) -> VideoScript:
    print("URL: ", submission.url)
    print("TITLE: ", submission.title)
    print("ID: ", submission.id)
    content = VideoScript(submission.url, submission.title, submission.id)
    print(f"Creating video for post: {submission.title}")
    print(f"Url: {submission.url}")

    number_done = 0
    for comment in submission.comments:
        if number_done >= NUMBER_COMMENTS:
            break
        voices = ["en_UK/apope_low", "en_US/cmu-arctic_low", "en_US/hifi-tts_low", "en_US/ljspeech_low", "en_US/m-ailabs_low", "en_US/vctk_low"]
        voice_to_use = random.choice(voices)
        comment_text = comment.body
        comment_id = comment.id
        if comment_text == "[removed]":
            print("found a comment removed")
            continue
        raw_text = markdown_to_text.markdown_to_text(comment_text)
        #if too many words
        wordCount = len(raw_text.split())
        if (wordCount > MAX_WORDS_PER_COMMENT or wordCount < MIN_WORDS_PER_COMMENT):
            continue
        #split into 3s
        new_comments = make_subcomments(comment_text)
        for new_id, new_comment in enumerate(new_comments):

            content.addCommentScene(new_comment, comment_id+str(new_id), voice_to_use)

        number_done += 1
        # print("Original comment: ", comment)
        # print("New comments: ", new_comments)
    return content

def __getExistingPostIds(outputDir):
    files = os.listdir(outputDir)
    # I'm sure anyone knowledgeable on python hates this. I had some weird 
    # issues and frankly didn't care to troubleshoot. It works though...
    files = [f for f in files if os.path.isfile(outputDir+'/'+f)]
    return [re.sub(r'.*?-', '', file) for file in files]

def make_subcomments(comment):
    new_comments = []
    pattern = re.compile(r'([.!,;:?]+)')

    # Use the pattern to split the text
    new_comments = re.split(pattern, comment)

    # Remove empty strings from the list
    new_comments = [substring.strip() for substring in new_comments if substring.strip()]
    print("New comments: ", new_comments)
    if len(new_comments) == 1:
        return new_comments
    #so that the punctuation is joined with the text
    new_comments = [new_comments[i] + new_comments[i + 1] for i in range(0, len(new_comments), 2)]
    return new_comments