from sanic import exceptions
from sanic import json
from sanic import Request
from sanic import Sanic
from sanic import text
from sanic.response import HTTPResponse
from sanic_ext import openapi

from .models.responses import GetChain
from .models.responses import IsValid
from .models.responses import MineBlock
from src.app.blockchain import BlockChain
from src.app.models.transaction import Transaction
from src.settings import settings

# from src.app.models.transaction import Transaction

blockchain = BlockChain()

app = Sanic('blockchain')


@app.get('/mine_block')
@openapi.response(
    200,
    {
        'application/json': MineBlock,
    },
)
async def mine_block(request: Request):
    previous_block = blockchain.get_previous_block()
    prev_proof = previous_block.proof
    proof = blockchain.proof_of_work(prev_proof)
    previous_hash = blockchain.hash(previous_block)

    blockchain.add_transaction(
        sender=settings.node_address,
        receiver='Nikolai',
        amount=143,
    )
    block = blockchain.create_block(proof, previous_hash)

    response = MineBlock(
        message='Congratulations! You just mined a block!',
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
        'application/json': GetChain,
    },
)
async def get_chain(request):
    response = GetChain(
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
        'application/json': IsValid,
    },
)
async def is_valid(request):
    message, is_valid = blockchain.is_valid()
    response = IsValid(
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
        body=f'This transaction will be added to the block {index}',
        status=201,
    )
