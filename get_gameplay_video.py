from pytube import YouTube
from moviepy.editor import VideoFileClip
from moviepy.video.fx.all import crop
import os
import time

def download_and_crop_youtube_video(video_url, max_duration=60):
    try:
        output_dir = 'background_videos'
        os.makedirs(output_dir, exist_ok=True)
        files_count = len([f for f in os.listdir(output_dir) if os.path.isfile(os.path.join(output_dir, f))]) - 1
        video_name = "cropped_video_" + str(files_count) + ".mp4"
        # Download YouTube video
        yt = YouTube(video_url)
        stream = yt.streams.filter(file_extension='mp4', res='720p').first()
        video_file = stream.download(output_dir, filename="og_video.mp4")

        # Trim the video to at most one minute from the middle
        clip = VideoFileClip(video_file)
        start_time = max(0, clip.duration // 2 - max_duration / 2)
        end_time = min(clip.duration, clip.duration // 2 + max_duration / 2)
        trimmed_clip = clip.subclip(start_time, end_time)
        
        (w, h) = trimmed_clip.size
        new_height = h
        new_width = (9 * h / 16)
        print("new dims should be, ", new_height," and ", new_width)

        cropped_clip = crop(trimmed_clip, height=new_height, width=new_width, x_center=w/2, y_center=h/2)
        print("dim: ", cropped_clip.size)
        final_clip = cropped_clip.resize(width=1080)
        # Set the volume to zero
        final_clip = final_clip.set_audio(None)
        print("dim: ", final_clip.size)
        output_path = os.path.join(output_dir, video_name)
        path_to_remove = os.path.join(output_dir, "og_video.mp4")
        os.remove(path_to_remove)

        final_clip.write_videofile(output_path, codec="libx264", audio_codec=None)

        print(f"Video downloaded, trimmed, and cropped successfully to {output_path}")
        return output_path
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    startTime = time.time()
    # youtube_url = "https://www.youtube.com/watch?v=b5WwymCBwEc"
    # download_and_crop_youtube_video(youtube_url)
    download_and_crop_youtube_video("https://www.youtube.com/watch?v=fPflaU71dCY")
    endTime = time.time()
    print(f"Total time: {endTime - startTime}")
