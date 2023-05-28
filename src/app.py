import hashlib
import datetime
import json
from flask import Flask, jsonify, request

from src.models.blockchain import BlockChain


app = Flask(__name__)

blockchain = BlockChain()


@app.route("/mine_block", methods=["GET"])
def mine_block():
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

    return jsonify(response), 200


@app.route("/get_chain", methods=["GET"])
def get_chain():
    response = {"chain": blockchain.chain, "length": len(blockchain.chain)}
    return jsonify(response), 200
