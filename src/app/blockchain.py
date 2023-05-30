import hashlib
from datetime import datetime
from typing import Tuple

from .models.block import Block


class BlockChain:
    def __init__(self):
        self.chain: list[Block] = []
        self.create_block(proof=1, previous_hash="0")

    def create_block(self, proof: int, previous_hash: str, data: str = "") -> Block:
        block = Block(
            hash="",
            index=len(self.chain) + 1,
            timestamp=datetime.now(),
            proof=proof,
            previous_hash=previous_hash,
            data=data,
        )
        self.chain.append(block)
        return block

    def get_previous_block(self) -> Block:
        return self.chain[-1]

    def proof_of_work(self, previous_proof: int) -> int:
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == "0000":
                check_proof = True
            else:
                new_proof += 1

        return new_proof

    def hash(self, block: Block) -> str:
        encoded_block = block.json(sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def is_chain_valid(self, chain: list[Block]) -> bool:
        previous_block = chain[0]
        block_index = 1

        while block_index < len(chain):
            block = chain[block_index]
            if block.previous_hash != self.hash(previous_block):
                return False

            previous_proof = previous_block.proof
            proof = block.proof
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != "0000":
                return False

            previous_block = block
            block_index += 1

        return True

    def is_valid(self) -> Tuple[str, bool]:
        if not self.is_chain_valid(self.chain):
            return "Chain is invalid", False

        return "", True
