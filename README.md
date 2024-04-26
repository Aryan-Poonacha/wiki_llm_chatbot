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

This project uses (Vectara)[https://vectara.com/] and (Pinecone)[https://www.pinecone.io/] as two potential options for backend vector databases. The first step is to go their websites, make an account and save your relevant credentials (API keys, corpus IDs, customer ID, etc.) in a .env file in the root directory. Additionally, a HuggingFace inference endpoint is used to host the model. Follow (these)[https://huggingface.co/docs/inference-endpoints/en/guides/create_endpoint] steps to host a HuggingFace model inference endpoint - a base Llama-3-8B-Instruct model from Meta is used for this project. Also remember to save your HF_token credentials to the .env file.

1. **Data Acquisition**: To get the data from the relevant wiki/knowledge base, follow the steps for the following sources:

Wikipedia: You can get the download URLs for Wikipedia pages in XML format from (this)[https://en.wikipedia.org/wiki/Wikipedia:Database_download] guide. A text dump of relevant Wikipedia articles is also easy to access.
(Fandom)[https://wikis.fandom.com/wiki/List_of_Wikia_wikis]: The URL to download the relevant wiki's entire knowledge base as a single XML file can be found in the Sepcial:Statistics page of that wiki. For example, (this)[https://yakuza.fandom.com/wiki/Special:Statistics] is the page that contains the download URLs to Yakuza's wiki,
(Internet Archive)[https://archive.org/details/wikiteam?tab=collection]: Contains a number of archived wikis from a broad range of topics. Use the URL for the 7Z option in the Download options for the wiki you desire.

Save these URLs and replace the URL list in `extract_data.py`.
Then run `extract_data.py` to download, process and save the data in the Data directory.
If the data is not accessible/difficult to obtain a download link for, you can also manually save the Data from your relevant source and put it into the Data directory.

2. **Data Loading**: Run `vectara_setup.py` and `pinecone_setup.py` to load all of the data files in the Data directory and put it into the Vectara/Pinecone backend, where it's processed and vectorized for efficient semantic search. These scripts use the helper pipeline scripts in the `vectara_scripts` and `pinecone_scripts` directories, respectively. The Vectara script leverages the dyanmic Vectara API to dynamically embed and ingest any and all popular file formats with good performance in its backend. The pinecone script currently only supports XML documents via langchain for their embedding, but can be easily modified to account for any other filetypes.

3. **HuggingFace Model Endpoint**: 

## Project Structure

The project repo is organized as follows:

├── README.md <- description of project and how to set up and run it
├── requirements.txt <- requirements file to document dependencies
├── vectara_setup.py <- script to set up project (load data from Data directory into Vectara backend)
├── pinecone_setup.py <- script to set up project (load data from Data dir into Pinecone backend)
── app.py <- streamlit frontend interface component
├── scripts <- directory for pipeline & utility scripts
├── llama3 <- model used in this project
├── Data <- directory for project data
├── Experiemnts <- different scripts for different components experimented with (like using pubnub as intermediary messenger between Vectara backend, HuggingFace endpoint and streamlit frontend)
├── .gitignore <- git ignore file

## License

This project is licensed under the terms of the MIT license. See the LICENSE file.

## Contact

If you have any questions, feel free to open an issue or submit a pull request.