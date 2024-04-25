import os

import pymongo
import streamlit as st
from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex, Settings
from llama_index.embeddings.fireworks import FireworksEmbedding
from llama_index.llms.fireworks import Fireworks
from llama_index.vector_stores.mongodb import MongoDBAtlasVectorSearch
from llama_index.core.retrievers import VectorIndexRetriever

from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine

# Load environment variables
load_dotenv()
env_vars = {
    'FIREWORKS_API_KEY': os.getenv('FIREWORKS_API_KEY'),
    'MONGO_URI': os.getenv('MONGO_URI'),
}

# Streamlit configurations
st.set_page_config(
    page_title="Chat with our sponsors docs, powered by LlamaIndex, MongoDB, and Fireworks.AI",
    page_icon="🦙",
    layout="centered",
    initial_sidebar_state="auto",
    menu_items=None
)

# Initialize settings
Settings.embed_model = FireworksEmbedding(
    api_key=env_vars['FIREWORKS_API_KEY'],
    embed_batch_size=10,
    dimensions=768
)

Settings.llm = Fireworks(
    api_key=env_vars['FIREWORKS_API_KEY'],
    model="accounts/fireworks/models/mixtral-8x22b-instruct"
)



# Initialize session state
if "messages" not in st.session_state.keys():
    st.session_state.messages = [
        {"role": "assistant", "content": "How can I help explore how these amazing tools can help you?"}
    ]


@st.cache_data(show_spinner=False)
def load_data():
    mongo_client = pymongo.MongoClient(env_vars['MONGO_URI'])
    vector_store = MongoDBAtlasVectorSearch(
        mongo_client,
        db_name="fireParse",
        collection_name="llamaIndexDocs",
        index_name="llama_docs_index"
    )
    return VectorStoreIndex.from_vector_store(vector_store=vector_store)


index = load_data()

# Configure the retriever
retriever = VectorIndexRetriever(
    index=index,
    similarity_top_k=5,  # Retrieve top 5 most similar documents
    doc_top_k=3,  # Return the top 3 most relevant documents
)

Settings.retriever = VectorIndexRetriever(
    index=index,
    similarity_top_k=5,  # Retrieve top 5 most similar documents
    doc_top_k=3,  # Return the top 3 most relevant documents
)

query_engine = RetrieverQueryEngine(
    retriever=retriever
)

# Create a ChatEngineConfig object
# config = ChatEngineConfig(
#     retriever=retriever,
#     # Add other configuration options as needed
# )


if "chat_engine" not in st.session_state.keys():
    # st.session_state.chat_engine = index.as_chat_engine(chat_mode="best", verbose=True)
    st.session_state.chat_engine = index.as_chat_engine(
                                                    chat_mode="best",  
                                                    context_prompt=(
                                                        """ You are a software developer bot that is an expert at reading over documentation to answer questions.
                                                            Use the relevant documents for context:
                                                            {context_str}
                                                            \nInstruction: Use the previous chat history, or the context above, to interact and help the user.
                                                        """
                                                    ),
                                                    verbose=True)

if prompt := st.chat_input("Your question"):  # Prompt for user input and save to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

for message in st.session_state.messages:  # Display the prior chat messages
    with st.chat_message(message["role"]):
        st.write(message["content"])

# If last message is not from assistant, generate a new response
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = st.session_state.chat_engine.chat(prompt)

            # st.write(response)
            print(response)

            st.write(response.response)
            message = {"role": "assistant", "content": response.response}
            st.session_state.messages.append(message)  # Add response to message history
