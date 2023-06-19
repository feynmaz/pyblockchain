from sanic import exceptions
from sanic import json
from sanic import Request
from sanic import Sanic
from sanic import text
from sanic.exceptions import BadRequest
from sanic.exceptions import SanicException
from sanic.response import HTTPResponse
from sanic_ext import openapi

from .models import requests
from .models import responses
from src.app.blockchain import BlockChain
from src.app.models.transaction import Transaction

blockchain = BlockChain()

app = Sanic('blockchain')


@app.get('/mine_block')
@openapi.response(
    200,
    {
        'application/json': responses.MineBlock,
    },
)
async def mine_block(request: Request):
    if len(blockchain.transactions) == 0:
        raise BadRequest(message='failed to create new block: no transactions created')

    previous_block = blockchain.get_previous_block()
    prev_proof = previous_block.proof
    proof = blockchain.proof_of_work(prev_proof)
    previous_hash = blockchain.hash(previous_block)

    block = blockchain.create_block(proof, previous_hash)

    response = responses.MineBlock(
        message='block mined',
        index=block.index,
        timestamp=block.timestamp,
        proof=block.proof,
        previous_hash=block.previous_hash,
        transactions=block.transactions,
    )

    return HTTPResponse(
        body=response.json(),
        content_type='application/json',
    )


@app.get('/get_chain')
@openapi.response(
    200,
    {
        'application/json': responses.GetChain,
    },
)
async def get_chain(request):
    response = responses.GetChain(
        chain=blockchain.chain,
    )

    return HTTPResponse(
        body=response.json(),
        content_type='application/json',
    )


@app.get('/is_valid')
@openapi.response(
    200,
    {
        'application/json': responses.IsValid,
    },
)
async def is_valid(request):
    message, is_valid = blockchain.is_valid()
    response = responses.IsValid(
        is_valid=is_valid,
        message=message if message else None,
    )
    return json(response.dict(exclude_none=True))


@app.post('/add_transaction')
@openapi.body({'application/json': Transaction})
async def add_transaction(request: Request):
    body_raw = request.json
    try:
        transaction = Transaction.parse_obj(body_raw)
    except ValueError as err:
        raise exceptions.SanicException(
            message=f'bad request body: {err}',
            status_code=422,
        )

    index = blockchain.add_transaction(
        transaction.sender,
        transaction.receiver,
        transaction.amount,
    )
    return text(
        body=f'transaction will be added to the block {index}',
        status=201,
    )


@app.post('/connect_node')
@openapi.body({'application/json': requests.ConnectNodes})
@openapi.response(
    201,
    {
        'application/json': responses.ConnectNodes,
    },
)
async def connect_node(request: Request):
    body_raw = request.json
    try:
        nodes = requests.ConnectNodes.parse_obj(body_raw)
    except ValueError as err:
        raise SanicException(
            message=f'bad request body: {err}',
            status_code=422,
        )

    if nodes.IsEmpty():
        raise BadRequest(message='no nodes provided')

    for node in nodes.GetNodes():
        blockchain.add_node(node)

    response = responses.ConnectNodes(
        message=f'nodes are connected: {blockchain.nodes}',
        total_nodes=len(blockchain.nodes),
    )
    return json(
        body=response.dict(),
        status=201,
    )


@app.get('/replace_chain')
@openapi.response(
    200,
    {
        'application/json': responses.ReplaceChain,
    },
)
def replace_chain(request):
    is_chain_replaced = blockchain.replace_chain()
    if is_chain_replaced:
        response = responses.ReplaceChain(
            message='nodes had different chains, so the chain was replaced by the longest one', chain=blockchain.chain
        )

    else:
        response = responses.ReplaceChain(message='the chain is the largest', chain=blockchain.chain)

    return HTTPResponse(
        body=response.json(),
        content_type='application/json',
    )
