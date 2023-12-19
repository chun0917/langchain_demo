import streamlit as st
import os

from langchain.llms import OpenAI
from langchain.document_loaders import SRTLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA

os.environ["OPENAI_API_KEY"] = "" # 你的OpenAI API Key

def create_chain():
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
    return chain

def data_append(prompt, answer):
    if 'messages' not in st.session_state:
        st.session_state.messages = [] 
    
    st.session_state.messages.append({"role":"user", "content":prompt})
    st.session_state.messages.append({"role":"assistant", "content":answer})

    print(st.session_state.messages)

def main():
    st.set_page_config(page_title="AI Assistant", page_icon=":robot:")
    prompt = st.chat_input("請輸入您的問題")
    if prompt:
        chain = create_chain()
        result = chain({"query": prompt})
        answer = result['result']
        data_append(prompt, answer)
        if 'messages' in st.session_state :
            for message in st.session_state.messages:
	            with st.chat_message(message["role"]):
		            st.markdown(message["content"])
                      
if __name__ == '__main__':
    main()