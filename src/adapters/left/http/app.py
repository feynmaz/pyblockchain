from sanic import Request
from sanic import Sanic
from sanic.response import HTTPResponse
from sanic_ext import openapi

from .models.responses import GetChain
from .models.responses import MineBlock
from src.app.blockchain import BlockChain

blockchain = BlockChain()

app = Sanic("blockchain")


@app.get("/mine_block")
@openapi.response(
    200,
    {
        "application/json": MineBlock,
    },
)
async def mine_block(request: Request):
    previous_block = blockchain.get_previous_block()
    prev_proof = previous_block.proof
    proof = blockchain.proof_of_work(prev_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash)

    response = MineBlock(
        message="Congratulations! You just mined a block!",
        index=block.index,
        timestamp=block.timestamp,
        proof=block.proof,
        previous_hash=block.previous_hash,
    )

    return HTTPResponse(
        body=response.json(),
        content_type="application/json",
    )


@app.get("/get_chain")
def get_chain(request):
    response = GetChain(
        chain=blockchain.chain,
    )

    return HTTPResponse(
        body=response.json(),
        content_type="application/json",
    )
