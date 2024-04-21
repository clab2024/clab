import streamlit as st
import openai
from llama_index.llms.openai import OpenAI
from llama_index.llms.fireworks import Fireworks
from llama_index.embeddings.fireworks import FireworksEmbedding
try:
  from llama_index import VectorStoreIndex, ServiceContext, Document, SimpleDirectoryReader
except ImportError:
  from llama_index.core import VectorStoreIndex, ServiceContext, Document, SimpleDirectoryReader

from llama_index.vector_stores.mongodb import MongoDBAtlasVectorSearch #MongoDBAtlasVectorStore
from llama_index.core import StorageContext
from llama_index.core import Settings
import pymongo
import os
from dotenv import load_dotenv

load_dotenv()

Settings.embed_model = FireworksEmbedding(
    api_key=os.getenv('FIREWORKS_API_KEY'), embed_batch_size=10, dimensions=768)

Settings.llm = Fireworks(api_key=os.getenv('FIREWORKS_API_KEY'), model="accounts/fireworks/models/llama-v3-70b-instruct")

st.set_page_config(page_title="Chat with our sponsors docs, powered by LlamaIndex, MongoDB, and Fireworks.AI", page_icon="🦙", layout="centered", initial_sidebar_state="auto", menu_items=None)
# openai.api_key = st.secrets.openai_key
st.title("Chat with our sponsors docs, powered by LlamaIndex, MongoDB, and Fireworks.AI 💬🦙")

if "messages" not in st.session_state.keys(): # Initialize the chat messages history
    st.session_state.messages = [
        {"role": "assistant", "content": "How can I help explore how these amazing tools can help you?"}
    ]

@st.cache_resource(show_spinner=False)
def load_data():
    with st.spinner(text="Creating our vector store."):
        mongo_client = pymongo.MongoClient(os.getenv('MONGO_URI'))
        vector_store = MongoDBAtlasVectorSearch(
    
        mongo_client, 
        db_name="sponsorDocuments", 
        collection_name="fireworkDocsTest", 
        index_name="vector_index"
        )
        index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
        return index

index = load_data()

if "chat_engine" not in st.session_state.keys(): # Initialize the chat engine
        st.session_state.chat_engine = index.as_chat_engine(chat_mode="condense_question", verbose=True)

if prompt := st.chat_input("Your question"): # Prompt for user input and save to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

for message in st.session_state.messages: # Display the prior chat messages
    with st.chat_message(message["role"]):
        st.write(message["content"])

# If last message is not from assistant, generate a new response
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = st.session_state.chat_engine.chat(prompt)
            st.write(response.response)
            message = {"role": "assistant", "content": response.response}
            st.session_state.messages.append(message) # Add response to message history