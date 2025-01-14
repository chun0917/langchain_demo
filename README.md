# langchain_demo教案

## 介紹
本教案介紹兩個 Python 檔案 `load_video.py` 和 `assistant.py`，這些檔案結合了多種函式庫來實現影片載入、轉錄及語音分析。以下將詳細介紹所使用的函式庫及其功能，並解析程式碼

## 使用的函式庫

### 1. `streamlit`
`streamlit` 是一個開源的 Python 函式庫，旨在幫助開發者快速構建互動式應用。此函式庫常被用於展示數據、創建機器學習應用、建立聊天機器人等。

- `st.text_input()`: 用於顯示輸入框，讓用戶輸入文字。
- `st.button()`: 創建一個按鈕，觸發相應操作。
- `st.spinner()`: 顯示載入動畫，讓用戶在等待時不會感到無聊。
- `st.warning()`, `st.success()`: 用於顯示警告和成功信息。

### 2. `whisper`
`whisper` 是 OpenAI 提供的語音識別模型，用於將語音轉錄為文字。此模型可以處理各種語言的語音檔案，並輸出準確的文字結果。

- `whisper.load_model()`: 載入指定的模型。
- `model.transcribe()`: 對語音檔案進行轉錄。

### 3. `pytube`
`pytube` 是一個 YouTube 下載工具，可以用來從 YouTube 上下載影片、音頻等媒體文件。

- `YouTube(url)`: 用於從 YouTube 影片 URL 創建一個影片對象。
- `yt.streams.filter().get_audio_only().download()`: 下載影片的音頻部分。

### 4. `langchain`
`langchain` 是一個語言模型鏈接框架，用於構建智能應用，如聊天機器人、問答系統等。

- `SRTLoader()`: 用於載入 `.srt` 格式的字幕檔案。
- `RecursiveCharacterTextSplitter()`: 用來拆分文本，使其適合語言模型處理。
- `Chroma()`: 用於創建向量數據庫，進行文檔的嵌入表示和檢索。
- `RetrievalQA()`: 創建一個問答鏈，利用語言模型來回答問題。

## 檔案說明

### 第一個檔案：`load_video.py`

該檔案的目的是下載 YouTube 影片，並將其音頻轉錄成文字。主要步驟如下：

1. **載入影片**:
   用戶輸入 YouTube 影片的 URL，並使用 `pytube` 庫下載影片的音頻。
   
   ```python
   yt = YouTube(url)
   video = yt.streams.filter().get_audio_only().download(filename='{}.mp3'.format(yt.title))
   ```
