import logging
import time

from classes.catappult_api import CatappultApi
from classes.postback_api import PostbackApi
from classes.purchase_entity import PurchaseEntity


class ValidatorException(Exception):
    pass


class OneStepPaymentValidator:
    MAX_RETRIES = 3
    DEFAULT_WAITING_TIME_SEC = 15

    def __init__(self, postback_api: PostbackApi, catappult_api: CatappultApi):
        self.postback_api = postback_api
        self.catappult_api = catappult_api
        self.logger = logging.getLogger("OneStepPaymentValidator")

    def validate(self, purchase_info: PurchaseEntity) -> bool:
        wallet_address = purchase_info.wallet_address
        wallet_signature = purchase_info.wallet_signature
        purchase_data = purchase_info.purchase_data

        transaction = self.catappult_api.purchase(
            wallet_address, wallet_signature, purchase_data)
        if not transaction:
            raise ValidatorException("Unable to reach Catappult API to purchase")

        uid, status = transaction["uid"], transaction["status"]

        if "COMPLETED" not in status:
            self.__get_transaction_status(uid, wallet_address, wallet_signature)

        time.sleep(self.DEFAULT_WAITING_TIME_SEC)
        return self.postback_api.verify(uid)

    def __get_transaction_status(self, uid, wallet_address, wallet_signature):
        status = ""
        num_retries = 0
        while "COMPLETED" not in status:
            time.sleep(self.DEFAULT_WAITING_TIME_SEC)
            if num_retries > self.MAX_RETRIES:
                raise ValidatorException("Unable to get transaction status")
            status = self.catappult_api.get_status(
                wallet_address, wallet_signature, uid)
