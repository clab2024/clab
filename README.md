# 🚀 LlamaWorksDB from Team CLAB

## 📅 Event Details
**Event**: MongoDB GenAI Hackathon SF Project  
**Date**: April 20, 2024

The MongoDB GenAI Hackathon SF Project was a grand event with over 100+ participants forming 20+ teams. The teams competed fiercely, showcasing their innovative projects and technical prowess.

LlamaWorksDB is a Retrieval Augmented Generation (RAG) product designed to interact with the documentation of various products such as LlamaIndex, Fireworks, MongoDB, git repositories, and cookbooks. This project was developed by team CLAB (Chris, Leo, Andrew, Barath)

## 🏆 Award

Our project, **"LlamaWorksDB"** ,was awarded 🏆 the  **"Best use of LlamaIndex"**  during the MongoDB GenAI Hackathon SF. We are proud of our achievement and grateful for the recognition, with cash prize of 500 USD, we are excited to continue our journey in the world of AI and ML.

## Table of Contents
- [Project Overview](#project-overview)
- [Team Members](#team-members)
- [Presentation](#presentation)
- [Application Screenshots](#application-screenshots)
- [Data Sources](#data-sources)
- [References](#references)

## 📚 Project Overview

LlamaWorksDB leverages the LlamaIndex, Fireworks, MongoDB documentation, git repositories, and cookbooks, along with the llamaParse API, to parse and represent files for efficient retrieval and context augmentation. The Fireworks model(nomic-ai/nomic-embed-text-v1.5) is used for embeddings with a dimension of 768.

## 👥 Team Members

![Team Picture](https://github.com/clab2024/clab/assets/2089311/55c4ac49-67bc-42ed-b486-3bf9710ace94)

- Chris
- Leo
- Andrew
- Barath -  [Twitter](https://twitter.com/baraths84)

## 🎥 Presentation

You can view our project presentation [here](https://docs.google.com/presentation/d/1Lrh9lr5KSHSxeS6SAg3rC75AUWI0VYrKnUFPUV93jBg/edit?usp=sharing).

## 📸 Application Screenshots

Here is screenshot of the application:

![ChatBot](https://github.com/clab2024/clab/assets/2089311/648f3e62-daa3-4f0b-af78-22c2e64ab525)


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