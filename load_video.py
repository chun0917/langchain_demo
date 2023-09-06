from pytube import YouTube
from datetime import timedelta
import os
import whisper

def transcribe_audio(segments):
    VIDEO_FILENAME = "lesson"

    for segment in segments['segments']:
        startTime = str(0)+str(timedelta(seconds=int(segment['start'])))+',000'
        endTime = str(0)+str(timedelta(seconds=int(segment['end'])))+',000'
        text = segment['text']
        segmentId = segment['id']+1
        segment = f"{segmentId}\n{startTime} --> {endTime}\n{text[1:] if text[0] == ' ' else text}\n\n"

        srtFilename = os.path.join(f"{VIDEO_FILENAME}.srt")
        with open(srtFilename, 'a', encoding='utf-8') as srtFile:
            srtFile.write(segment)

    return srtFilename

def main():
    os.environ["OPENAI_API_KEY"] = "" #你的openai-key

    yt = YouTube('') #想要轉換的影片網址
    video = yt.streams.filter().get_audio_only().download(filename='lesson.mp3')
    print(yt)
    print(video)

    model = whisper.load_model("base")
    options = whisper.DecodingOptions(fp16 = False)
    transcription = model.transcribe(video,language='zh')

    text = transcription['text']
    print(text)

    transcribe_audio(transcription)

if __name__ == '__main__':
    main()
