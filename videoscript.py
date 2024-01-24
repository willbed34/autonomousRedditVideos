from datetime import datetime
from moviepy.editor import AudioFileClip
import voiceover
import random

MAX_WORDS_PER_COMMENT = 100
MIN_COMMENTS_FOR_FINISH = 4
MIN_DURATION = 20
MAX_DURATION = 58

class VideoScript:
    title = ""
    fileName = ""
    titleSCFile = ""
    url = ""
    totalDuration = 0
    frames = []

    def __init__(self, url, title, fileId) -> None:
        self.fileName = f"{datetime.today().strftime('%Y-%m-%d')}-{fileId}"
        self.url = url
        self.title = title
        #TODO add "story mode", where its just the post, not the comments
        # if NumberComments == 0
        self.titleAudioClip = self.__createVoiceOver("title", title, "en_US/hifi-tts_low")

    def addCommentScene(self, text, commentId, voice_type = "en_US/hifi-tts_low") -> None:
        frame = ScreenshotScene(text, commentId)
        frame.audioClip = self.__createVoiceOver(commentId, text, voice_type)
        self.frames.append(frame)

    def getDuration(self):
        return self.totalDuration

    def getFileName(self):
        return self.fileName

    def __createVoiceOver(self, name, text, voice_type):
        file_path = voiceover.create_voice_over(f"{self.fileName}-{name}", text, voice_type)
        audioClip = AudioFileClip(file_path)
        if (self.totalDuration + audioClip.duration > MAX_DURATION):
            return None
        self.totalDuration += audioClip.duration
        return audioClip


class ScreenshotScene:
    text = ""
    screenShotFile = ""
    commentId = ""

    def __init__(self, text, commentId) -> None:
        self.text = text
        self.commentId = commentId