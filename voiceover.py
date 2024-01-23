import os
import speed_up_audio
from pydub import AudioSegment

voiceoverDir = "voiceovers"

import subprocess

def create_voice_over(fileName, text, voice_to_use):
    #making voiceover
    
    os.makedirs(voiceoverDir, exist_ok=True)
    old_name = f"{voiceoverDir}/{fileName}.wav"
    new_name = f"{voiceoverDir}/{fileName}.mp3"
    text = text.replace(".", ",")
    text = fileName + "|" + text
    # print("TEXT: ", text)
    args = [
        "mimic3",
        text,
        "--csv",
        "--voice",
        voice_to_use,
        "--output-dir",
        voiceoverDir]
    try:
        subprocess.check_call(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        audio_segment = AudioSegment.from_wav(old_name)
        
        # Trim the first and last 250 milliseconds (adjust as needed)
        # trimmed_audio = audio_segment[100:-500]
        trimmed_audio = audio_segment
        # Export the trimmed audio as MP3
        trimmed_audio.export(new_name, format="mp3")
        os.remove(old_name)
        # speed_up_audio.speed_up(new_name, new_name, 1.1)
        return new_name
    except subprocess.CalledProcessError as e:
        # Handle error
        print("ERROR w voiceover")
        pass

