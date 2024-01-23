General structure is based off of https://github.com/Shifty-The-Dev/RedditVideoGenerator

#HOW TO USE
Use get_gameplay_video to download Youtube background video under Creative Commons. It will save it in background_videos.
Then, in the config file, specify the reddit client and secret, as well as other things such as number of comments you want to obtain, as well as if you want to manually select which post from a list. Also specify a subreddit.
Then run main. This will get the reddit post, make images of the text, get the voiceovers, and then compile it on top of the background video.

#Changes:
Added code to get background video.
Pyttsx3 wasn't working, so I switched to mimic3.
Capturing screenshots wasn't working, so I generate text images based on the reddit words.
Splitting up texts into phrases, so that the text doesnt cover whole screen.
Removed VLC preview.

#Things to note:
You need to make and app on reddit to get the keys to put in the config. Rename EXAMPLE_CONFIG.ini to config.ini.
You may also need to associate a Youtube account with this code, so that it can download the videos.
Also, be sure to install dependencies as needed. Will work on getting a requirements.txt in the future.
