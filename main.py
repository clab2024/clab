from fastapi import FastAPI
import pymongo
import os
import nest_asyncio
from llama_index.vector_stores.mongodb import MongoDBAtlasVectorSearch
from llama_index.core import VectorStoreIndex
from llama_index.core import StorageContext
from llama_index.core import SimpleDirectoryReader
from llama_parse import LlamaParse  # pip install llama-parse
from llama_index.core import SimpleDirectoryReader  # pip install llama-index
from llama_index.core.settings import Settings
from llama_index.llms.openai import OpenAI
# from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.embeddings.fireworks import FireworksEmbedding
from llama_index.core.node_parser import SentenceSplitter
import dotenv
from llama_index.readers.github import (GithubRepositoryReader, GithubClient)
dotenv.load_dotenv()
nest_asyncio.apply()


LLAMA_PARSE_API_KEY = os.environ.get("LLAMA_PARSE_API_KEY")
FIREWORKS_API_KEY = os.environ.get("FIREWORKS_API_KEY")
MONGO_URI = os.environ.get("MONGO_URI")

dotenv.load_dotenv()
github_token = os.getenv('GITHUB_TOKEN')
client = GithubClient(github_token=github_token)
# TODO add more filters
default_directory_filters = ["docs", "examples"]


def scrape_github_repo(repo, owner, github_client=client, branch="main"):
    documents = GithubRepositoryReader(
        github_client=github_client,
        owner=owner,
        repo=repo,
        use_parser=True,
        verbose=False,
        filter_file_extensions=([".py", ".js", ".md"],
                                GithubRepositoryReader.FilterType.INCLUDE),
    ).load_data(branch=branch)

    return documents


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/lamma-parse-and-mongo-load")
async def parser():

    parser = LlamaParse(
        api_key=LLAMA_PARSE_API_KEY,
        result_type="markdown",  # "markdown" and "text" are available
        verbose=True,
        language="en",  # Optionally you can define a language, default=en
    )

    # file_extractor = {".pdf": parser}
    # reader = SimpleDirectoryReader("./data", file_extractor=file_extractor)
    # documents = reader.load_data()
    # print(f"Size of documents: {len(documents)}")
    documents = scrape_github_repo(repo="RPG-API", owner="b3fr4nk")

    # Settings.llm = OpenAI()
    # Settings.embed_model = OpenAIEmbedding(model="text-embedding-ada-002")
    # Settings.chunk_size = 100
    # Settings.chunk_overlap = 10

    Settings.embed_model = FireworksEmbedding(
        api_key=FIREWORKS_API_KEY, embed_batch_size=10, dimensions=768)
    # Settings.chunk_size = 100
    # Settings.chunk_overlap = 10

    mongo_uri = (
        MONGO_URI
    )

    mongodb_client = pymongo.MongoClient(mongo_uri)

    # store = MongoDBAtlasVectorSearch(
    # mongodb_client,
    # db_name = "clamdb",
    # collection_name = "clamcol",
    # index_name = "vector_index")

    store = MongoDBAtlasVectorSearch(
        mongodb_client,
        db_name="clamdb",
        collection_name="clamcol",
        index_name="vector_fireworks_index")

    storage_context = StorageContext.from_defaults(vector_store=store)

    # Store your data as vector embeddings.
    index = VectorStoreIndex.from_documents(
        documents, storage_context=storage_context, show_progress=True
    )

    return {"message": "Parsin and loading data complete"}
