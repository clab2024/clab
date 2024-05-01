import os

import dotenv
import pymongo
from fastapi import FastAPI
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.core.settings import Settings
from llama_index.embeddings.fireworks import FireworksEmbedding
from llama_index.readers.github import GithubRepositoryReader, GithubClient
from llama_index.vector_stores.mongodb import MongoDBAtlasVectorSearch

dotenv.load_dotenv()

app = FastAPI()


def scrape_github_repo(repo, owner, branch="main"):
    """
    Scrape github repo using LlamaIndex's github repo reader.
    Returns LlamaIndex Documents for all files in repo
    """
    github_token = os.getenv('GITHUB_TOKEN')
    client = GithubClient(github_token=github_token)
    documents = GithubRepositoryReader(
        github_client=client,
        owner=owner,
        repo=repo,
        use_parser=True,
        verbose=False,
        filter_file_extensions=([".py", ".js", ".md"],
                                GithubRepositoryReader.FilterType.INCLUDE),
    ).load_data(branch=branch)

    return documents


@app.post("/lamma-parse-and-mongo-load")
def parser():
    """Parse and store embeddings from scrape_github_repo"""

    FIREWORKS_API_KEY = os.environ.get("FIREWORKS_API_KEY")
    MONGO_URI = os.environ.get("MONGO_URI")

    documents = scrape_github_repo(owner="mongoDB", repo="chatbot")

    Settings.embed_model = FireworksEmbedding(
        api_key=FIREWORKS_API_KEY, embed_batch_size=10, dimensions=768)

    mongodb_client = pymongo.MongoClient(MONGO_URI)

    store = MongoDBAtlasVectorSearch(
        mongodb_client,
        db_name="clamdb",
        collection_name="clamcol",
        index_name="vector_fireworks_index")

    storage_context = StorageContext.from_defaults(vector_store=store)

    VectorStoreIndex.from_documents(
        documents, storage_context=storage_context, show_progress=True
    )

    return {"message": "Parsing and loading data complete"}


@app.get("/")
async def root():
    """Testing route to confirm server is running"""
    return {"message": "Hello World"}
