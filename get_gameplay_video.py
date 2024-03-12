from pytube import YouTube
from moviepy.editor import VideoFileClip
from moviepy.video.fx.all import crop
import os
import time
import random
from get_youtube_link import get_youtube_link
import ssl

# Disable SSL certificate verification

def auto_download_and_crop_youtube_video(max_duration=60):
    ssl._create_default_https_context = ssl._create_unverified_context
    output_dir = 'background_videos'
    os.makedirs(output_dir, exist_ok=True)
    files_count = len([f for f in os.listdir(output_dir) if os.path.isfile(os.path.join(output_dir, f))]) - 1
    
    # Download YouTube video
    video_url = get_youtube_link()
    if video_url == None:
        return None
    yt = YouTube(video_url)
    stream = yt.streams.filter(file_extension='mp4', res='720p').first()
    video_file = stream.download(output_dir, filename="og_video.mp4")

    # Trim the video to at most one minute from the middle
    clip = VideoFileClip(video_file)
    video_name = "background.mp4"
    start_time = random.uniform(5, clip.duration - max_duration)
    end_time = start_time + max_duration
    trimmed_clip = clip.subclip(start_time, end_time)
    process_and_save_clip(trimmed_clip, output_dir, video_name)
    
    os.remove(os.path.join(output_dir, "og_video.mp4"))
    print(f"Video downloaded, trimmed, and cropped successfully to {output_dir}")
    return os.path.join(output_dir, video_name)

def download_and_crop_youtube_video(video_url, max_duration=60, split_video=False):
    try:
        output_dir = 'background_videos'
        os.makedirs(output_dir, exist_ok=True)
        files_count = len([f for f in os.listdir(output_dir) if os.path.isfile(os.path.join(output_dir, f))]) - 1
        
        # Download YouTube video
        yt = YouTube(video_url)
        stream = yt.streams.filter(file_extension='mp4', res='720p').first()
        video_file = stream.download(output_dir, filename="og_video.mp4")

        # Trim the video to at most one minute from the middle
        clip = VideoFileClip(video_file)
        if split_video:
            parts = int((clip.duration - 30) / max_duration)
            for i in range(parts):
                video_name = "cropped_video_" + str(files_count + i) + ".mp4"
                start_time = i * max_duration + 15  # Exclude the first 15 seconds
                end_time = (i + 1) * max_duration + 15  # Exclude the last 15 seconds
                part_clip = clip.subclip(start_time, end_time)
                process_and_save_clip(part_clip, output_dir, video_name)
        else:
            video_name = "cropped_video_" + str(files_count) + ".mp4"
            start_time = random.uniform(5, clip.duration - max_duration)
            end_time = start_time + max_duration
            trimmed_clip = clip.subclip(start_time, end_time)
            process_and_save_clip(trimmed_clip, output_dir, video_name)
        
        os.remove(os.path.join(output_dir, "og_video.mp4"))
        print(f"Video downloaded, trimmed, and cropped successfully to {output_dir}")
    except Exception as e:
        print(f"Error: {e}")

def process_and_save_clip(clip, output_dir, video_name):
    (w, h) = clip.size
    new_height = h
    new_width = (9 * h / 16)
    print("new dims should be, ", new_height," and ", new_width)

    cropped_clip = crop(clip, height=new_height, width=new_width, x_center=w/2, y_center=h/2)
    print("dim: ", cropped_clip.size)
    final_clip = cropped_clip.resize(width=1080)
    # Set the volume to zero
    final_clip = final_clip.set_audio(None)
    print("dim: ", final_clip.size)

    output_path = os.path.join(output_dir, video_name)
    final_clip.write_videofile(output_path, codec="libx264", audio_codec=None)
    print(f"Saved video {video_name}")

if __name__ == "__main__":
    startTime = time.time()
    # youtube_url = "https://www.youtube.com/watch?v=b5WwymCBwEc"
    # download_and_crop_youtube_video(youtube_url)
    download_and_crop_youtube_video("https://www.youtube.com/watch?v=R0b-VFV8SJ8", max_duration=60, split_video=True)
    endTime = time.time()
    print(f"Total time: {endTime - startTime}")
