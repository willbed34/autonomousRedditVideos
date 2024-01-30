from moviepy.editor import *
import reddit, screenshot, time, subprocess, random, configparser, sys, math
from os import listdir
from os.path import isfile, join
from get_gameplay_video import auto_download_and_crop_youtube_video
import shutil

def createVideo():
    config = configparser.ConfigParser()
    config.read('config.ini')
    outputDir = config["General"]["OutputDirectory"]
    os.makedirs(outputDir, exist_ok=True)
    startTime = time.time()


    # Get script from reddit
    # If a post id is listed, use that. Otherwise query top posts
    if (len(sys.argv) == 2):
        script = reddit.getContentFromId(outputDir, sys.argv[1])
    else:
        postOptionCount = int(config["Reddit"]["NumberOfPostsToSelectFrom"])
        script = reddit.getContent(outputDir, postOptionCount)
    fileName = script.getFileName()

    # Create screenshots
    print("Starting to create screenshots.")
    screenshot.getPostScreenshots(fileName, script)
    # Setup background clip
    print("Getting background clip.")
    #trying automatically
    bg_video_path  = auto_download_and_crop_youtube_video()
    print("Getting this file path: ", bg_video_path)
    if bg_video_path == None:
        print("Couldn't find youtube vid link, going to predownloaded ones")
        bgDir = config["General"]["BackgroundDirectory"]
        backgroundVideo = VideoFileClip(
            filename=f"{bgDir}/cropped_video_0.mp4", 
            audio=False).subclip(0, script.getDuration())
    else:
        backgroundVideo = VideoFileClip(
        filename=bg_video_path, 
        audio=False).subclip(0, script.getDuration())
    print("Just got video")
    

    w, h = backgroundVideo.size

    def __createClip(screenShotFile, audioClip, marginSize):
        imageClip = ImageClip(
            screenShotFile,
            duration=audioClip.duration
            ).set_position(("center", "center"))
        imageClip = imageClip.resize(width=(w-marginSize))
        videoClip = imageClip.set_audio(audioClip)
        videoClip.fps = 1
        return videoClip

    # Create video clips
    print("Editing clips together...")
    clips = []
    marginSize = int(config["Video"]["MarginSize"])

    clips.append(__createClip(script.titleSCFile, script.titleAudioClip, marginSize))
    for comment in script.frames:
        clips.append(__createClip(comment.screenShotFile, comment.audioClip, marginSize))

    # Merge clips into single track
    contentOverlay = concatenate_videoclips(clips).set_position(("center", "center"))

    # Compose background/foreground
    final = CompositeVideoClip(
        clips=[backgroundVideo, contentOverlay], 
        size=backgroundVideo.size).set_audio(contentOverlay.audio)
    final.duration = script.getDuration()
    final.set_fps(backgroundVideo.fps)

    # Write output to file
    print("Rendering final video...")
    bitrate = config["Video"]["Bitrate"]
    threads = config["Video"]["Threads"]
    outputFile = f"{outputDir}/{fileName}.mp4"
    final.write_videofile(
        outputFile, 
        codec = 'libx264',
        audio_codec='aac',
        threads = threads, #8000k
        bitrate = bitrate #12
    )
    print(f"Video completed in {time.time() - startTime}")

    print("Video is ready to upload!")
    print(f"Title: {script.title}  File: {outputFile}")
    print("Starting cleanup...")
    print("Removing screenshots...")
    screenshots_dir = "screenshots"
    try:
        shutil.rmtree(screenshots_dir)
        print(f"Removed directory: {screenshots_dir}")
    except FileNotFoundError:
        print(f"The directory '{screenshots_dir}' does not exist.")
    except Exception as e:
        print(f"Error while removing directory {screenshots_dir}: {e}")

    print("Removing voiceovers...")
    voiceovers_dir = "voiceovers"
    try:
        shutil.rmtree(voiceovers_dir)
        print(f"Removed directory: {voiceovers_dir}")
    except FileNotFoundError:
        print(f"The directory '{voiceovers_dir}' does not exist.")
    except Exception as e:
        print(f"Error while removing directory {voiceovers_dir}: {e}")
    endTime = time.time()
    print(f"Total time: {endTime - startTime}")

if __name__ == '__main__':
    print("Main is called")
    createVideo()
