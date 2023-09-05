import streamlit as st
import os

from langchain.llms import OpenAI
from langchain.document_loaders import SRTLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA

os.environ["OPENAI_API_KEY"] = "" #你的openai-key


def data_append(answer, user_input):
    print(st.session_state)
    if 'question_array' not in st.session_state:
        st.session_state.question_array = [] 
    if 'answer_array' not in st.session_state:
        st.session_state.answer_array = []

    st.session_state.question_array.insert(0, user_input)
    st.session_state.answer_array.insert(0, answer)
    return {"question": st.session_state.question_array, "answer": st.session_state.answer_array}

def main():
    document = SRTLoader("test2.srt").load()
    ext_splitter = RecursiveCharacterTextSplitter(
        chunk_size=100,
        chunk_overlap=0
    )
    db = Chroma.from_documents(
        documents=ext_splitter.split_documents(document),
        embedding=OpenAIEmbeddings(),
        persist_directory='db1'
    )

    chain = RetrievalQA.from_chain_type(
        llm=OpenAI(model='text-davinci-003'),
        chain_type="stuff",
        retriever=db.as_retriever(),
        return_source_documents=True
    )

    st.set_page_config(page_title="LangChain Demo", page_icon=":robot:")
    st.header("(LangChain) 陳煥老師 深度學習課程小幫手")
    user_input = st.text_input("請輸入您的問題： ", "", key="input")

    if st.button('詢問', key='ask_button'):
        if user_input:
            with st.spinner('小幫手思考中...'):
                result = chain({"query": user_input})
                answer = result['result']
                data_append(answer, user_input)
                st.write(answer)
        else:
            st.warning('請輸入您的問題')

    st.header('歷史問答紀錄')

    if 'question_array' in st.session_state and 'answer_array' in st.session_state:
        for question, answer in zip(st.session_state.question_array, st.session_state.answer_array):
            st.write('問：', question)
            st.write('答：', answer)
            #st.write('------------------------------------')

if __name__ == '__main__':
    main()
