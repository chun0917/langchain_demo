# langchain_demo教案

## 介紹
本教案介紹兩個 Python 檔案 `load_video.py` 和 `assistant.py`，來完成影片載入、轉換及語音分析。以下將詳細介紹所使用的函式庫及其功能，並解析程式碼

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
   
### page資料夾內第2個檔案：`assistant.py`

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
### 系統架構與流程說明

1. **系統架構**:
![image](https://github.com/user-attachments/assets/de0dd1be-5315-4b1f-8a38-bdd2fd003c35)
系統架構：指定需要處理的課程材料。可以是本地端的影片或音檔，或是YouTube的網址，使用OpenAI Whisper將課程材料中的語音內容轉換為文本
為了提高文本的準確性，我們進行文本預處理。這包括拼寫檢查和處理可能在語音識別過程中出現的錯誤
我們將處理完的文本分割並且存放到向量資料庫
用戶將通過提問與AI助教互動，有兩種情況：
 	- 情況一：如果答案已經在預處理的文本中，AI助教可以直接根據文本內容回答問題
 	- 情況二：如果文本中沒有答案，AI助教可以利用ChatGPT模型來根據用戶的問題生成答案

2. **系統流程圖**:
![image](https://github.com/user-attachments/assets/e0c98d6a-6cde-4ecb-aa04-2451917de269)
1. 指定課程材料：
   - 第一步是明確指定需要處理的課程材料。可以是本地端的影片或音檔，或是YouTube的網址
 
2. 語音轉文字：
   - 接下來，我們使用OpenAI Whisper將課程材料中的語音內容轉換為文本
 
3. 文本預處理：
   - 為了提高文本的準確性，我們進行文本預處理。這包括拼寫檢查和處理可能在語音識別過程中出現的錯誤
 
4. 用戶提問：
   - 用戶將通過提問與AI助教互動，他們的問題將與課程內容相關
 
5. 回答生成：
   - 有兩種情況：
 	- 情況一：如果答案已經在預處理的文本中，AI助教可以直接根據文本內容回答問題
 	- 情況二：如果文本中沒有答案，AI助教可以利用ChatGPT模型來根據用戶的問題生成答案
 
6. 回答並記錄：
   - AI助教將為用戶的問題提供回答，並將這些問答儲存於歷史問答紀錄中
