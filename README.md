# 🚀 LlamaWorksDB from Team CLAB

## 📅 Event Details

**Event**: MongoDB GenAI Hackathon SF  
**Date**: April 20, 2024

The MongoDB GenAI Hackathon SanFranc was a grand event with over 100+ participants forming 20+ teams. The teams competed fiercely, showcasing their innovative projects and technical prowess.

LlamaWorksDB is a Retrieval Augmented Generation (RAG) product designed to interact with the documentation of various products such as LlamaIndex, Fireworks, MongoDB, git repositories, and cookbooks. This project was developed by team CLAB (Chris, Leo, Andrew, Barath)

## 🏆 Award

Our project, **"LlamaWorksDB"** ,was awarded 🏆 the **"Best use of LlamaIndex"** during the MongoDB GenAI Hackathon SF. We are proud of our achievement and grateful for the recognition, with cash prize of 500 USD, we are excited to continue our journey in the world of AI and ML.

## Table of Contents

- [Project Overview](#project-overview)
- [Team Members](#team-members)
- [Presentation](#presentation)
- [Application Screenshots](#application-screenshots)
- [Data Sources](#data-sources)
- [References](#references)

## 📚 Project Overview

LlamaWorksDB leverages the LlamaIndex, Fireworks, MongoDB documentation, git repositories, and cookbooks, along with the llamaParse API, to parse and represent files for efficient retrieval and context augmentation. The Fireworks model(nomic-ai/nomic-embed-text-v1.5) is used for embeddings with a dimension of 768.

## 🏃‍♂️‍➡️ Install and Run Instructions

1. Clone the repo somewhere and navigate to that directory
2. Create a python virtual environment using `python3 -m venv ./venv` and then use `source ./venv/bin/activate` to enter the virtual environment (optional)
3. Use `pip install -r requirments.txt` to install all necessary dependencies.
4. Create a .env file in the root of the project containing your API keys for your github token, mongo uri, fireworks API key, and LlamaParse API key.
5. Make sure you modify the vector store information in both scrape_documentation.py and main.py to match your MongoDB Atlas configuration
6. To add documentation from navigate to the ingestion_pipeline directory and run `python3 scrape_documentation.py` to add all documentation in documentation_to_scrape.json
7. To add Github examples navigate back to the root directory and run `uvicorn main:app --reload` then send a post request to localhost:8000/lamma-parse-and-mongo-load
8. Finally to run the chatbot `python3 -m streamlit run streamlit_app.py`

## 📝 Modifying Source Data

If you want to try out LlamaWorksDB with other documentation Follow these Steps:

1. For Github projects change line 44 in main.py to the owner and repo you wish to embed and store.
2. for website documentation modify input_pipeline/documentation_to_scrape with all of the urls you want to scrape.

## 👥 Team Members

<table>
  <tr>
    <td>
      <img src="https://github.com/clab2024/clab/assets/2089311/55c4ac49-67bc-42ed-b486-3bf9710ace94" width="300">
    </td>
  <td>
    <img src="https://github.com/clab2024/clab/assets/2089311/bc247980-600f-404f-8069-95d918742676" width="300">
    </td>
  </tr>
</table>
      - Chris<br>
      - Leo<br>
      - Andrew<br>
      - Barath [Twitter](https://twitter.com/baraths84)

## 🎥 Presentation

You can view our project presentation [here](https://docs.google.com/presentation/d/1Lrh9lr5KSHSxeS6SAg3rC75AUWI0VYrKnUFPUV93jBg/edit?usp=sharing).

## 📸 Application Screenshots

Here is screenshot of the application:

<img src="https://github.com/clab2024/clab/assets/2089311/648f3e62-daa3-4f0b-af78-22c2e64ab525" width="400">

## 📂 Data Sources

We used the GithubRepositoryReader to ingest the chat-llamaindex and chatbot repositories listed below. The SimpleWebPageReader was used to ingest the LLamaindex web documentation (modules, api-reference, some errors with example) and all of the Firework documentation (blog posts, api reference, model cards).

- [chat-llamaindex](https://github.com/run-llama/chat-llamaindex)
- [chatbot](https://github.com/mongodb/chatbot/)
- https://readme.fireworks.ai/docs/quickstart

## 📚 References

- [GithubRepositoryReader Demo](https://docs.llamaindex.ai/en/stable/examples/data_connectors/GithubRepositoryReaderDemo/)
- [SimpleWebPageReader](https://docs.llamaindex.ai/en/stable/examples/data_connectors/WebPageDemo/?h=simplewebpagereader#using-simplewebpagereader)
- [Fireworks Embeddings](https://docs.llamaindex.ai/en/stable/examples/embeddings/fireworks/)
- [MongoDB Atlas Vector Search](https://www.mongodb.com/products/platform/atlas-vector-search)
- [create-llama](https://www.llamaindex.ai/blog/create-llama-a-command-line-tool-to-generate-llamaindex-apps-8f7683021191)
