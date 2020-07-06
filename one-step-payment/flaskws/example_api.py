import json
import logging

from flask import request, jsonify
from flask_restx import Namespace, Resource

import settings
from classes.cache import Cache
from classes.catappult_api import CatappultApi
from classes.transaction_repository import TransactionRepository

example_api = Namespace("one-step", description="One-Step operations")
catappult_api = CatappultApi(settings.CATAPPULT_API_HOST, Cache())
transaction_repo = TransactionRepository(catappult_api)

verified_transactions = []


@example_api.route("/payment")
class Payment(Resource):
    def post(self):
        global verified_transactions
        """Pings the server when a callback is done"""
        if len(verified_transactions) > 100:
            del verified_transactions[:]

        notification = json.loads(request.json["transaction"])
        uid = notification["uid"]

        ws_transaction = transaction_repo.get_transaction_response(uid)

        if transaction_repo.is_valid(notification, ws_transaction):
            verified_transactions.insert(0, uid)
        else:
            logging.error("Transaction info did not match info from callback")

        return 200


@example_api.route("/verify/<string:uid>")
class Verify(Resource):
    def get(self, uid):
        global verified_transactions
        """Check if the transaction is verified"""
        for tran_uid in verified_transactions:
            if tran_uid == uid:
                return jsonify({"verified": True})
        return jsonify({"verified": False})

