import os
from dotenv import load_dotenv
from vectara_upload import create_corpus, upload_file
from vectara_query import VectaraAPI

class VectaraSetup:
    def __init__(self):
        load_dotenv()
        self.customer_id = os.getenv('VECTARA_CUSTOMER_ID')
        self.admin_address = os.getenv('VECTARA_ADMIN_ADDRESS')
        self.idx_address = os.getenv('VECTARA_IDX_ADDRESS')
        self.jwt_token = os.getenv('VECTARA_JWT_TOKEN')
        self.data_dir = os.getenv('VECTARA_DATA_DIR')

    def setup(self):
        # Create a new corpus
        corpus_response, success = create_corpus(self.customer_id, self.admin_address, self.jwt_token)
        if not success:
            return

        # Get the corpus ID
        corpus_id = corpus_response["corpus"]["id"]

        # Upload all files in the data directory
        for file_name in os.listdir(self.data_dir):
            file_path = os.path.join(self.data_dir, file_name)
            upload_file(self.customer_id, corpus_id, self.idx_address, self.jwt_token, file_path)

# Usage
# vectara_setup = VectaraSetup()
# vectara_setup.setup()
