from datetime import datetime
from src.models.block import Block
import hashlib


class BlockChain:
    def __init__(self):
        self.chain = []
        self.create_block(proof=1, previous_hash="0")

    def create_block(self, proof, previous_hash, data=""):
        block = Block(
            index=len(self.chain) + 1,
            timestamp=datetime.now(),
            proof=proof,
            previous_hash=previous_hash,
            data=data,
        )
        self.chain.append(block)
        return block

    def get_previous_block(self):
        return self.chain[-1]

    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
            
        return new_proof
