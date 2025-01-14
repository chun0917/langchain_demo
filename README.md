# langchain_demo教案

## 介紹
本教案介紹兩個 Python 檔案 `load_video.py` 和 `assistant.py`，這些檔案結合了多種函式庫來實現影片載入、轉換及語音分析。以下將詳細介紹所使用的函式庫及其功能，並解析程式碼

## 使用的函式庫

### 1. `streamlit`
`streamlit` 是一個開源的 Python 函式庫，常被用於展示數據、建立聊天機器人等

- `st.text_input()`: 用於顯示輸入框，讓用戶輸入文字
- `st.button()`: 創建一個按鈕，觸發相應操作
- `st.spinner()`: 顯示載入動畫，讓用戶在等待時不會感到無聊
- `st.warning()`, `st.success()`: 用於顯示警告和成功訊息

### 2. `whisper`
`whisper` 是 OpenAI 提供的語音識別模型，用於將語音轉換為文字。此模型可以處理各種語言的語音檔案，並輸出準確的文字結果

- `whisper.load_model()`: 載入指定的模型
- `model.transcribe()`: 對語音檔案進行轉換

### 3. `pytube`
`pytube` 是一個 YouTube 下載工具，可以用來從 YouTube 上下載影片、音檔等

- `YouTube(url)`: 用於從 YouTube 影片 URL 創建一個影片對象
- `yt.streams.filter().get_audio_only().download()`: 下載影片的音檔部分

### 4. `langchain`
`langchain` 是一個語言模型開源框架，用於構建AI應用，如聊天機器人、問答系統等

- `SRTLoader()`: 用於載入 `.srt` 格式的字幕文檔
- `RecursiveCharacterTextSplitter()`: 用來拆分文本，使其適合語言模型處理
- `Chroma()`: 用於創建向量數據庫，進行文檔的嵌入表示和檢索
- `RetrievalQA()`: 創建一個問答鏈，利用語言模型來回答問題

## 檔案說明

### 第1個檔案：`load_video.py`

目的是下載 YouTube 影片，並將其音檔轉換成文檔。主要步驟如下：

1. **載入影片**:
   用戶輸入 YouTube 影片的 URL，並使用 `pytube` 下載影片的音檔
   
   ```python
   yt = YouTube(url)
   video = yt.streams.filter().get_audio_only().download(filename='{}.mp3'.format(yt.title))
   ```
2. **語音轉錄**:
   使用 `whisper` 模型將下載的音檔轉換成文檔
   ```python
   model = whisper.load_model("base")
   transcription = model.transcribe(video, language='zh')
   ```
3. **生成字幕檔**:
   將轉換的結果以 `.srt` 格式保存，方便後續使用
   ```python
   for segment in segments['segments']:
   startTime = str(0) + str(timedelta(seconds=int(segment['start']))) + ',000'
   endTime = str(0) + str(timedelta(seconds=int(segment['end']))) + ',000'
   text = segment['text']
   segmentId = segment['id'] + 1
   segment = f"{segmentId}\n{startTime} --> {endTime}\n{text[1:] if text[0] == ' ' else text}\n\n"
   ```
   
### 第2個檔案：`assistant.py`

用於建立一個問答系統，根據 `.srt` 字幕檔案進行文本分析，並回答使用者的問題。主要步驟如下：

1. **載入字幕檔案**:
   使用 `langchain` 的 `SRTLoader` 載入 `.srt` 字幕檔案，並將其分割成適合語言模型處理的小段文本
   ```python
  document = SRTLoader("test2.srt").load()
  text_splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=0)
   ```

2. **建立向量資料庫**:
   使用 `Chroma` 創建一個向量數據庫，將分割後的文本轉換為向量
   ```python
   db = Chroma.from_documents(documents=ext_splitter.split_documents(document), embedding=OpenAIEmbeddings(), persist_directory='db1')
   ```

3. **進行問答**:
使用 `RetrievalQA` 問答鏈，將使用者的問題與文檔內容進行匹配，並使用語言模型回答問題
   ```python
   chain = RetrievalQA.from_chain_type(llm=OpenAI(model='text-davinci-003'), chain_type="stuff", retriever=db.as_retriever(), return_source_documents=True)
   if prompt:
      chain = create_chain()
      result = chain({"query": prompt})
      answer = result['result']
      data_append(prompt, answer)
   ```
