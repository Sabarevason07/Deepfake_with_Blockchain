import hashlib
import json
from time import time

class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []

        # Create the genesis block
        self.new_block(previous_hash='1', proof=100)

    def new_block(self, proof, previous_hash=None):
        """
        Create a new block in the blockchain.
        """
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        # Reset the current list of transactions
        self.current_transactions = []

        self.chain.append(block)
        return block

    def new_transaction(self, video_name, video_accuracy, audio_accuracy, file_hash, uploader='Guest', location='Unknown'):
        """
        Add a new transaction to the list of transactions.
        """
        self.current_transactions.append({
            'video_name': video_name,
            'video_accuracy': video_accuracy,
            'audio_accuracy': audio_accuracy,
            'file_hash': file_hash,
            'uploader': uploader,
            'location': location,
            'timestamp': time(),
        })

        return self.last_block['index'] + 1

    def log_ai_model(self, model_name, dataset, version):
        """
        Log AI model metadata on the blockchain.
        """
        self.current_transactions.append({
            'model_name': model_name,
            'dataset': dataset,
            'version': version,
            'timestamp': time(),
        })

        return self.last_block['index'] + 1

    @staticmethod
    def hash(block):
        """
        Create a SHA-256 hash of a block.
        """
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        """
        Return the last block in the chain.
        """
        return self.chain[-1]
