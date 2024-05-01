import re
import pymongo
from dotenv import load_dotenv
import os
import json
from llama_index.readers.web import SimpleWebPageReader
from llama_index.core.ingestion import IngestionPipeline
from llama_index.embeddings.fireworks import FireworksEmbedding
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.ingestion import IngestionPipeline
from llama_index.vector_stores.mongodb import MongoDBAtlasVectorSearch
from llama_index.vector_stores.mongodb import MongoDBAtlasVectorSearch
from llama_index.readers.web import SimpleWebPageReader
from llama_index.core.node_parser import SemanticSplitterNodeParser

load_dotenv()

class LlamaDocsPageReader(SimpleWebPageReader):
    def load_data(self, urls):
        documents = super().load_data(urls)
        processed_documents = []
        for doc in documents:
            processed_doc = self.process_document(doc)
            processed_documents.append(processed_doc)
        return processed_documents

    def process_document(self, document):
        # Split the document text by "Table of Contents"
        pattern = r'(?i)\n\n*table\s*of\s*contents\n\n*'
        parts = re.split(pattern, document.text, maxsplit=1)
        # If there is a part after "Table of Contents", use it as the document text
        if len(parts) > 1:
            document.text = "Table of contents".join(parts[1:])
        return document


# FireworksEmbedding defaults to using model
embed_model = FireworksEmbedding(api_key=os.getenv('FIREWORKS_API_KEY'), 
                                #  model="nomic-ai/nomic-embed-text-v1.5",
                                 embed_batch_size=10, 
                                 dimensions=768 # can range from 64 to 768
                                 )

# the tried and true sentence splitter
text_splitter = SentenceSplitter(chunk_size=1000, chunk_overlap=200)
# the semantic splitter uses our embedding model to group semantically related sentences together
semantic_parser = SemanticSplitterNodeParser(embed_model=embed_model)

# we set up MongoDB as our document and vector database
vector_store = MongoDBAtlasVectorSearch(
    pymongo.MongoClient(os.getenv('MONGO_URI')),
    db_name="fireParse",
    collection_name="llamaIndexDocs",
    index_name="llama_docs_index"
)

#finally we use LlamaIndex's pipeline to string this all together
pipeline = IngestionPipeline(
    transformations=[
        semantic_parser, #can replace with text_splitter
        embed_model,
    ],
    vector_store=vector_store,
)

with open("input_pipeline/sample_documentation_to_scrape.json", "r") as json_file:
    loaded_dict = json.load(json_file)

for key, urls in loaded_dict.items():
    documents = LlamaDocsPageReader(html_to_text=True).load_data(urls)
    pipeline.run(documents=documents, show_progress=True)
