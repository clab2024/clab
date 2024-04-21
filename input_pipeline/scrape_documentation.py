from llama_index.readers.web import SimpleWebPageReader
from llama_index.core.ingestion import IngestionPipeline
from llama_index.embeddings.fireworks import FireworksEmbedding
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.ingestion import IngestionPipeline
import pymongo
from llama_index.vector_stores.mongodb import MongoDBAtlasVectorSearch
from dotenv import load_dotenv
import os
import json

load_dotenv()

FIREWORKS_API_KEY = os.getenv('FIREWORKS_API_KEY')
MONGO_URI = os.getenv('MONGO_URI')
mongo_uri = (MONGO_URI,)

mongodb_client = pymongo.MongoClient(mongo_uri)

vector_store = MongoDBAtlasVectorSearch(
    mongodb_client,
    db_name = "sponsorDocuments",
    collection_name = "fireworkDocsTest",
    index_name = "vector_fireworks_index"
)

text_splitter = SentenceSplitter(chunk_size=700, chunk_overlap=0)
embed_model = FireworksEmbedding(api_key=FIREWORKS_API_KEY, embed_batch_size=10, dimensions=768)

pipeline = IngestionPipeline(
    transformations=[
        text_splitter,
        embed_model,
    ],
    vector_store=vector_store,
)

with open("documentation_to_scrape.json", "r") as json_file:
    loaded_dict = json.load(json_file)

    for _, urls in loaded_dict.keys():
        documents = SimpleWebPageReader(html_to_text=True,metadata_fn=lambda url: {"src":url}).load_data(urls)
        pipeline.run(documents=documents, show_progress=True)