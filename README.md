# Wiki Chatbot

This project provides a general way to convert any wiki knowledge base into a chatbot that you can talk to and ask questions. This repository is an example/proof of concept of how to do so, applied to the Yakuza wiki. Chat about anything in the Yakuza wiki with the chatbot (here)[https://yakuza.streamlit.app]!

## Project Description

The objective of this project is to develop a functioning "proof of concept" application which uses a deep learning model to generate predictions or perform analysis on real-world data. The data used in this project is extracted from the Yakuza wiki.

## Getting Started

1. Clone this repository.
2. Install the required dependencies listed in `requirements.txt`.

## Project Pipeline

The project pipeline involves the following steps:

0. **Setup**

This project uses [Vectara](https://vectara.com/) and [Pinecone](https://www.pinecone.io/) as two potential options for backend vector databases. The first step is to go their websites, make an account and save your relevant credentials (API keys, corpus IDs, customer ID, etc.) in a .env file in the root directory. Additionally, a HuggingFace inference endpoint is used to host the model. Follow [these](https://huggingface.co/docs/inference-endpoints/en/guides/create_endpoint) steps to host a HuggingFace model inference endpoint - a base Llama-3-8B-Instruct model from Meta is used for this project. Also remember to save your HF_token credentials to the .env file. When configuring the HuggingFace model, be sure to use the custom prompt from the custom_prompt.txt as the baseline context of the model.

1. **Data Acquisition**: To get the data from the relevant wiki/knowledge base, follow the steps for the following sources:

Wikipedia: You can get the download URLs for Wikipedia pages in XML format from [this](https://en.wikipedia.org/wiki/Wikipedia:Database_download) guide. A text dump of relevant Wikipedia articles is also easy to access.
[Fandom](https://wikis.fandom.com/wiki/List_of_Wikia_wikis): The URL to download the relevant wiki's entire knowledge base as a single XML file can be found in the Sepcial:Statistics page of that wiki. For example, [this](https://yakuza.fandom.com/wiki/Special:Statistics) is the page that contains the download URLs to Yakuza's wiki,
[Internet Archive](https://archive.org/details/wikiteam?tab=collection): Contains a number of archived wikis from a broad range of topics. Use the URL for the 7Z option in the Download options for the wiki you desire.

Save these URLs and replace the URL list in `extract_data.py`.
Then run `extract_data.py` to download, process and save the data in the Data directory.
If the data is not accessible/difficult to obtain a download link for, you can also manually save the Data from your relevant source and put it into the Data directory.

2. **Data Loading**: Run `vectara_setup.py` and `pinecone_setup.py` to load all of the data files in the Data directory and put it into the Vectara/Pinecone backend, where it's processed and vectorized for efficient semantic search. These scripts use the helper pipeline scripts in the `vectara_scripts` and `pinecone_scripts` directories, respectively. The Vectara script leverages the dyanmic Vectara API to dynamically embed and ingest any and all popular file formats with good performance in its backend. The pinecone script currently only supports XML documents via langchain for their embedding, but can be easily modified to account for any other filetypes.

3. **HuggingFace Model Endpoint**: With the HF_token of the HuggingFace inference endpoint you wish to use, embed the custom prompt into the model. 

4. **Deploy on Streamlit**: Go to the [Streamlit Community](https://streamlit.io/cloud) cloud and make a new app. Use your clone of this repo for the new app and target the app.py file to use for the streamlit interface. Add the relevant keys from Pinecone/Vectara and HuggingFace from the .env file to the secret keys section of your app.

Voila! Your chatbot should be deployed and be able to answer complex queries about your knowledge base.

## Models

### Llama-3-8B

Llama-3-8B was used as the main model for this project as it represents the current SOTA for OS models. Two main variations of the model were used:

1. Base Llama-3-8B-Instruct
2. Base Llama-3-8B finetuned on [RAG instruct-tuning dataset](https://huggingface.co/datasets/llmware/rag_instruct_benchmark_tester) 

## Evaluation

We want to compare and see which combination of embedding & RAG Mechanism and Model produce the best overall result to fetch most relevant information and effectively summarize it (integration test?); not just individual base model or RAG performance.

I manually compiled a list of complex queries and questions as the test dataset in `questions.txt`. I then manually did human-evaluated comparisons of responses with the different 4 combinations of embedding systems and model used.

For the RAG comparisons, to set a baseline, the baseline mean model approach is to simply search the XML document for relevant information from the search query to use as context. For the non-deep learning approach to use as a comparison, TF-IDF was used to similarly find relevant results to use as context to pass to the model. The scripts for these are in the `non-dl-models` directory.

Ultimately, the Base Llama-38B-Instruct with the Vectara RAG mechanism performed best and was used for the final deployed model.

## Project Structure

The project repo is organized as follows:

├── README.md <- description of project and how to set up and run it
├── requirements.txt <- requirements file to document dependencies
├── vectara_setup.py <- script to set up project (load data from Data directory into Vectara backend)
├── pinecone_setup.py <- script to set up project (load data from Data dir into Pinecone backend)
── app.py <- streamlit frontend interface component
├── scripts <- misc scripts for loading data
├── pinecone_scripts <- directory for pipeline & utility scripts for pinecone
├── vectara_scripts <- directory for pipeline & utility scripts for vectara
├── finetuning <- scripts for finetuning of llama-3 model
├── llama3 <- model used in this project
├── non-dl-models <- directory for scripts used for baseline and non-deep learning approaches
├── Data <- directory for project data
├── Experiments <- different scripts for different components experimented with (like using pubnub as intermediary messenger between Vectara backend, HuggingFace endpoint and streamlit frontend)
├── questions.txt <- test dataset of manually compiled complex queries
├── .gitignore <- git ignore file

## License

This project is licensed under the terms of the MIT license. See the LICENSE file.

## Contact

If you have any questions, feel free to open an issue or submit a pull request.