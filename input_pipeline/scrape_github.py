import openai
import nest_asyncio

from llama_index.core import VectorStoreIndex
from llama_index.readers.github import (GithubRepositoryReader, GithubClient)
import dotenv
import os

dotenv.load_dotenv()
github_token = os.getenv('GITHUB_TOKEN')
client = GithubClient(github_token=github_token)
# TODO add more filters
default_directory_filters = ["docs", "examples"]


def scrape_github_repo(repo, owner, github_client=client, branch="main", filters=[]):
    documents = GithubRepositoryReader(
        github_client=github_client,
        owner=owner,
        repo=repo,
        use_parser=True,
        verbose=False,
        filter_directories=(filters, GithubRepositoryReader.FilterType.EXCLUDE)
    ).load_data(branch=branch)

    return documents


atlas_chatbot_documents = scrape_github_repo(owner="b3fr4nk", repo="RPG-API")
print(atlas_chatbot_documents[0])
# pymongo_documents = scrape_github_repo(
#     owner="mongodb", repo="mongo-python-driver")
