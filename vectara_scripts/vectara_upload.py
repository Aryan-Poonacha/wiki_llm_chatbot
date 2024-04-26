#Refactored from https://github.com/vectara/getting-started
import os
import json
import logging
import requests
from dotenv import load_dotenv

def _get_create_corpus_json():
    """ Returns a create corpus json. """
    corpus = {}
    corpus["name"] = "Vectara Test Corpus(Python)"
    corpus["description"] = "An example corpus generated via REST API from Python code."

    return json.dumps({"corpus":corpus})

def create_corpus(customer_id: int, admin_address: str, jwt_token: str):
    """Create a corpus.
    Args:
        customer_id: Unique customer ID in vectara platform.
        admin_address: Address of the admin server. e.g., api.vectara.io
        jwt_token: A valid Auth token.

    Returns:
        (response, True) in case of success and returns (error, False) in case of failure.
    """

    post_headers = {
        "customer-id": f"{customer_id}",
        "Authorization": f"Bearer {jwt_token}"
    }
    response = requests.post(
        f"https://{admin_address}/v1/create-corpus",
        data=_get_create_corpus_json(),
        verify=True,
        headers=post_headers)

    if response.status_code != 200:
        logging.error("Create Corpus failed with code %d, reason %s, text %s",
                       response.status_code,
                       response.reason,
                       response.text)
        return response, False

    message = response.json()
    if message["status"] and message["status"]["code"] != "OK":
        logging.error("Create Corpus failed with status: %s", message["status"])
        return message["status"], False

    return message, True

def upload_file(customer_id: int, corpus_id: int, idx_address: str, jwt_token: str, file_path: str):
    """Uploads a file to the corpus.

    Args:
        customer_id: Unique customer ID in vectara platform.
        corpus_id: ID of the corpus to which data needs to be indexed.
        idx_address: Address of the indexing server. e.g., api.vectara.io
        jwt_token: A valid Auth token.
        file_path: Path to the file to be uploaded.

    Returns:
        (response, True) in case of success and returns (error, False) in case of failure.
    """
    post_headers = {
        "Authorization": f"Bearer {jwt_token}"
    }
    with open(file_path, 'r') as file:
        file_data = file.read()
    response = requests.post(
        f"https://{idx_address}/v1/upload?c={customer_id}&o={corpus_id}",
        files={"file": (os.path.basename(file_path), file_data, "application/json")},
        verify=True,
        headers=post_headers)

    if response.status_code != 200:
        logging.error("REST upload failed with code %d, reason %s, text %s",
                       response.status_code,
                       response.reason,
                       response.text)
        return response, False

    message = response.json()["response"]
    # An empty status indicates success.
    if message["status"] and message["status"]["code"] not in ("OK", "ALREADY_EXISTS"):
        logging.error("REST upload failed with status: %s", message["status"])
        return message["status"], False

    return message, True

def vectara_upload(customer_id: int, admin_address: str, idx_address: str, jwt_token: str, data_dir: str):
    """Creates a new Vectara corpus and uploads all files in the local Data directory.

    Args:
        customer_id: Unique customer ID in vectara platform.
        admin_address: Address of the admin server. e.g., api.vectara.io
        idx_address: Address of the indexing server. e.g., api.vectara.io
        jwt_token: A valid Auth token.
        data_dir: Path to the local Data directory.
    """
    corpus_response, success = create_corpus(customer_id, admin_address, jwt_token)
    if not success:
        return

    corpus_id = corpus_response["corpus"]["id"]
    for file_name in os.listdir(data_dir):
        file_path = os.path.join(data_dir, file_name)
        upload_file(customer_id, corpus_id, idx_address, jwt_token, file_path)

#Example usage
load_dotenv()
customer_id = os.getenv('VECTARA_CUSTOMER_ID')
corpus_id = os.getenv('VECTARA_CORPUS_ID')
api_key = os.getenv('VECTARA_YAKUZA_WIKI_API_KEY')