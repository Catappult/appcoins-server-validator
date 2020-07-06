from src.classes.catappult_api import CatappultApi


class TransactionRepository:
    def __init__(self, catappult_api: CatappultApi):
        self.catappult_api = catappult_api

    def get_transaction_response(self, uid: str) -> dict:
        return self.catappult_api.get_transaction(uid)

    @staticmethod
    def is_valid(notification: dict, ws_transaction: dict) -> bool:
        return notification['uid'] == ws_transaction['uid'] and \
               notification['domain'] == ws_transaction['domain'] and \
               notification['product'] == ws_transaction['product'] and \
               notification['status'] == ws_transaction['status'] and \
               notification['price'] == ws_transaction['price'] and \
               notification['reference'] == ws_transaction['reference'] and \
               notification['price']['currency'] == ws_transaction['price']['currency'] and \
               notification['price']['value'] == ws_transaction['price']['value'] and \
               notification['price']['appc'] == ws_transaction['price']['appc']
