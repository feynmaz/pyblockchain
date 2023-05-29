import json

from sanic import Sanic
from sanic.response import json

from src.models.blockchain import BlockChain

blockchain = BlockChain()

app = Sanic("blockchain")


@app.get("/mine_block")
async def mine_block(request):
    prev_block = blockchain.get_previous_block()
    prev_proof = prev_block["proof"]
    proof = blockchain.proof_of_work(prev_proof)
    previous_hash = blockchain.hash(prev_block)
    block = blockchain.create_block(proof, previous_hash)

    response = {
        "message": "Congratulations! You just mined a block!",
        "index": block["index"],
        "timestamp": block["timestamp"],
        "proof": block["proof"],
        "previous_hash": block["previous_hash"],
    }

    return json(
        body=response,
    )


@app.get("/get_chain")
def get_chain(request):
    response = {"chain": blockchain.chain, "length": len(blockchain.chain)}
    return json(body=response)
