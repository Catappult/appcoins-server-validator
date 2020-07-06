import argparse
import logging
import random
import string

from ngrok.ngrok_service import NgrokService
from src import settings
from src.classes.cache import Cache
from src.classes.catappult_api import CatappultApi
from src.classes.one_step_validator import OneStepPaymentValidator, \
    ValidatorException
from src.classes.postback_api import PostbackApi
from src.classes.purchase_entity import PurchaseEntity


def generate_reference() -> str:
    length_string = 32
    alphanumeric = string.ascii_letters + string.digits
    return ''.join((random.choice(alphanumeric) for i in range(length_string)))


def get_purchase_info(_postback_host: str):
    if settings.ENVIRONMENT == settings.Environments.PRODUCTION:
        return PurchaseEntity(
            wallet_address="0xA7397b8098DA7544B9cF456A76892D75707e2518",
            wallet_signature=("f275c365efef8b74d476c0c90ac8db1e42e1a5dca43beae"
                              "23a8ece63ea6100f5239ecab270a160d2e517d9a8e0dad1"
                              "0a6b90b52e2b0f240592fe3b713dce341300"),
            purchase_data={
                "origin": "BDS",
                "domain": "com.test.generatedapks587",
                "price.value": 0.01,
                "price.currency": "APPC",
                "product": "gas",
                "type": "INAPP_UNMANAGED",
                "wallets.developer": "0x18d2de7e886fe29491b15442b4b43203c65a4cfa",
                "wallets.store": "0xc41b4160b63d1f9488937f7b66640d2babdbf8ad",
                "wallets.oem": "0x0965b2a3e664690315ad20b9e5b0336c19cf172e",
                "callback_url": _postback_host + "/one-step/payment",
                "reference": generate_reference()
            }
        )
    else:
        return PurchaseEntity(
            wallet_address="0xbb83e699f1188baabea820ce02995c97bd9b510f",
            wallet_signature=("5f17a0df29c298e59056377a6926e3eed8134644b6e15a7"
                              "84d7c82888496d93e05628b50253bbeab10cbc230b5c50f"
                              "acb135c8886b3f20c6c96860e50638353000"),
            purchase_data={
                "origin": "BDS",
                "domain": "com.appcoins.trivialdrivesample.test",
                "price.value": 0.01,
                "price.currency": "APPC",
                "product": "gas",
                "type": "INAPP_UNMANAGED",
                "wallets.developer": "0x123c2124b7f2c18b502296ba884d9cde201f1c32",
                "wallets.store": "0xc41b4160b63d1f9488937f7b66640d2babdbf8ad",
                "wallets.oem": "0x0965b2a3e664690315ad20b9e5b0336c19cf172e",
                "callback_url": _postback_host + "/one-step/payment",
                "reference": generate_reference()
            }
        )


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-d", "--debug", dest="log_level", action="store_const",
                    const=logging.DEBUG, default=logging.INFO,
                    help="Show debug log messages")
    args = ap.parse_args()
    logging.getLogger().setLevel(args.log_level)

    ngrok_service = NgrokService()
    ngrok_service.start(settings.API_PORT)
    ngrok_url = ngrok_service.get_url()

    postback_api = PostbackApi(ngrok_url)
    catappult_api = CatappultApi(settings.CATAPPULT_API_HOST, Cache())
    one_step_validator = OneStepPaymentValidator(postback_api, catappult_api)

    logging.info("Testing One-Step Payment...")
    purchase_info = get_purchase_info(ngrok_url)
    try:
        is_verified = one_step_validator.validate(purchase_info)
    except ValidatorException as e:
        logging.error(e)
        is_verified = False

    if is_verified:
        logging.info("Transaction: '{}' was successfully verified".format(purchase_info))
    else:
        logging.error("Unable to verify transaction: '{}'".format(purchase_info))

    ngrok_service.stop()
