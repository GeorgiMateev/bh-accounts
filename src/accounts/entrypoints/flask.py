from flask import Flask, jsonify, request
from accounts import bootstrap
from accounts.domain import commands, queries
from accounts.services import customers

app = Flask(__name__)

bus = bootstrap.bootstrap()

@app.route("/<id>/open", methods=["POST"])
def openAccount(id: str):
    initialCredit = request.json['credit']
    cmd = commands.OpenAccount(id, initialCredit)
    try:
        bus.handle(cmd)
    except customers.InvalidAmount as e:
        return {"message": str(e)}, 400

    return "OK", 201


@app.route("/<id>", methods=["GET"])
def accountDetails(id: str):
    query = queries.CustomerHistory(id)
    result = bus.handle(query)
    if not result:
        return {"message": "Not found"}, 404

    return jsonify(result), 200