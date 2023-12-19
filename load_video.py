import streamlit as st
import os
import re
import whisper

from pytube import YouTube
from pytube.exceptions import RegexMatchError
from datetime import timedelta

os.environ["OPENAI_API_KEY"] = "" # 你的OpenAI API Key

def validate_url(url):
    pattern = re.compile(r'^https?://')
    if re.match(pattern, url):
        return True
    else:
        st.warning("請輸入有效的網址，例如：http://youtube.com")
        return False

def load_file(url):
    try:
        yt = YouTube(url)
        video = yt.streams.filter().get_audio_only().download(filename='{}.mp3'.format(yt.title))
        model = whisper.load_model("base")
        options = whisper.DecodingOptions(fp16 = False)
        transcription = model.transcribe(video,language='zh')
        return True, transcription, yt.title
    except RegexMatchError:
        st.warning("請確認網址是否為有效的YouTube影片")
        return False

def transcribe_audio(filename,segments):
    VIDEO_FILENAME = filename

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
    st.set_page_config(page_title="AI Assistant", page_icon=":robot:")
    st.header("智慧課程小幫手")
    st.warning("注意！請先載入影片再至assistant分頁進行提問")
    url_input = st.text_input("請輸入影片網址： ", "", key="url_input")
    url_button = st.button("載入")
    if url_button:
        if validate_url(url_input):
            print(url_input)
            st.empty()
            load_spinner = st.spinner('載入影片中...')
            with load_spinner:
                if load_file(url_input):
                    transcription = load_file(url_input)
                    transcribe_audio(transcription[2],transcription[1])
            st.success("影片載入成功")
if __name__ == '__main__':
    main()
