import hashlib
from datetime import datetime
from http import HTTPStatus
from typing import Set
from typing import Tuple
from urllib.parse import urlparse

import requests

from .models.block import Block
from .models.transaction import Transaction


class BlockChain:
    def __init__(self):
        self.chain: list[Block] = []
        self.transactions: list[Transaction] = []
        self.create_block(proof=1, previous_hash='0')
        self.nodes: Set[str] = set()

    def create_block(self, proof: int, previous_hash: str, data: str = '') -> Block:
        block = Block(
            index=len(self.chain) + 1,
            timestamp=datetime.now(),
            proof=proof,
            previous_hash=previous_hash,
            data=data,
            transactions=self.transactions,
        )
        self.transactions = []
        self.chain.append(block)
        return block

    def get_previous_block(self) -> Block:
        return self.chain[-1]

    def proof_of_work(self, previous_proof: int) -> int:
        new_proof = 1
        is_proof_valid = False
        while is_proof_valid is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                is_proof_valid = True
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
            if hash_operation[:4] != '0000':
                return False

            previous_block = block
            block_index += 1

        return True

    def is_valid(self) -> Tuple[str, bool]:
        if not self.is_chain_valid(self.chain):
            return 'Chain is invalid', False

        return '', True

    def add_transaction(self, sender: str, receiver: str, amount: float) -> int:
        self.transactions.append(
            Transaction(
                sender=sender,
                receiver=receiver,
                amount=amount,
            )
        )
        previous_block = self.get_previous_block()
        return previous_block.index + 1

    def add_node(self, address: str):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

    def replace_chain(self):
        network = self.nodes
        longest_chain: list[Block] = []
        max_length = len(self.chain)
        for node in network:
            with requests.get(f'http://{node}/get_chain') as response:
                if response.status_code == HTTPStatus.OK.value:
                    length = response.json()['length']
                    chain_raw: list[dict] = response.json()['chain']
                    chain: list[Block] = [Block.parse_obj(_) for _ in chain_raw]
                    if length > max_length and self.is_chain_valid(chain):
                        max_length = length
                        longest_chain = chain

        if longest_chain:
            self.chain = longest_chain
            return True

        return False
