from pydub import AudioSegment
import os

def speed_up(slow_mp3_path, fast_mp3_path, rate = 1.2):
    # A couple of var for readability

    # Get the audiosegment from the file
    slow_mp3_obj = AudioSegment.from_file(slow_mp3_path)
    # File's in memory, you can safely delete the original file if you want to save disk space now
    os.remove(slow_mp3_path)
    # Speed it up
    speed_update = slow_mp3_obj.speedup(rate)
    # Save the updated mp3
    speed_update.export(fast_mp3_path, format="mp3")
    return fast_mp3_path