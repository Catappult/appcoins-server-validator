import logging

from classes.catappult_api import CatappultApi
from classes.purchase_entity import PurchaseEntity


class APIValidatorException(Exception):
    pass


class APIValidator:
    def __init__(self, catappult_api: CatappultApi):
        self.catappult_api = catappult_api
        self.logger = logging

    def validate(self, purchase: PurchaseEntity):
        self.logger.info("Received a new purchase to validate")
        self.logger.debug("packageName: '{}'".format(purchase.package_name))
        self.logger.debug("sku: '{}'".format(purchase.sku))
        self.logger.debug("purchaseToken: '{}'".format(purchase.purchase_token))
        return self.__validate_purchase(purchase)

    def __validate_purchase(self, purchase: PurchaseEntity) -> bool:
        purchase_status = self.catappult_api.get_purchase_status(
            purchase.package_name, purchase.sku, purchase.purchase_token)

        if purchase_status == 200:
            self.logger.debug("Purchase successfully validated!")
            return True
        elif purchase_status == -1:
            raise APIValidatorException("Unable to connect to Catappult API")
        else:
            self.logger.debug("Unable to find purchase!")
            return False

