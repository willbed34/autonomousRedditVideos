# Project Name

General structure is based off of [RedditVideoGenerator](https://github.com/Shifty-The-Dev/RedditVideoGenerator).

## How to Use

1. Use `get_gameplay_video` to download a Youtube background video under Creative Commons. It will save it in the `background_videos` directory.
2. In the config file, specify the Reddit client and secret, along with other parameters such as the number of comments you want to obtain and whether you want to manually select a post from a list. Also, specify a subreddit.
3. Run `main.py`. This will get the Reddit post, generate images of the text, obtain voiceovers, and then compile everything on top of the background video.

## Changes

- Added code to download the background video.
- Switched from Pyttsx3 to mimic3 as Pyttsx3 wasn't working.
- Text images are generated based on the Reddit words as capturing screenshots wasn't working.
- Splitting up texts into phrases to avoid covering the whole screen.
- Removed VLC preview.
- Added ability to speed up audio.

## Things to Note

- You need to create an app on Reddit to obtain the keys for the config. Rename `EXAMPLE_CONFIG.ini` to `config.ini`.
- You may need to associate a YouTube account with this code for video downloads.
- Create venv
- Install dependencies as needed using `requirements.txt`.

## TODO
- Automate background video capturing, select from a few categories like csgo, minecraft, fortnite, gta, using selection or randomizing.
- Find best subreddits for selection that are more Q/A based.
- Enable "story mode", where most of text is in original post.
- Fix error when repeated quotation in a comment
- Maybe make dictionary, mapping subreddits to config specs. For isntance, 2 sentence horror would have diff config than askreddit.
- Put screenshots and voiceovers into subfolders for a given post
- If duration exceeds, don't return none, have it handle accordingly
