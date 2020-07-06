import json
import logging

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

from classes.cache import Cache


class CatappultApi:
    MAX_RETRIES = 3
    DELAY_SECONDS_BETWEEN_REQUESTS = 1
    GET_TRANSACTIONS_PATH = "/broker/8.20200101/transactions/"
    ADD_TRANSACTIONS_PATH = ("/broker/8.20180518/gateways/appcoins_credits/"
                             "transactions")
    GET_STATUS_PATH = "/broker/8.20180518/gateways/appcoins_credits/"

    def __init__(self, catappult_host: str, cache: Cache, timeout=5):
        self.catappult_host = catappult_host
        self.cache = cache
        self.timeout = timeout
        self.session = self.__get_session()

    def __get_session(self):
        session = requests.Session()
        retry = Retry(connect=self.MAX_RETRIES,
                      backoff_factor=self.DELAY_SECONDS_BETWEEN_REQUESTS)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)

        return session

    def purchase(self, wallet_address: str, wallet_signature: str, data: dict):
        params = {"wallet.address": wallet_address,
                  "wallet.signature": wallet_signature}
        url = self.catappult_host + self.ADD_TRANSACTIONS_PATH
        return self.__post_request(url, params, data)

    def __post_request(self, url: str, params: dict, data: dict) -> json:
        try:
            response = requests.post(url, params=params, data=data,
                                     timeout=self.timeout)
            if response.status_code in (200, 201):
                return response.json()
            else:
                return dict()
        except requests.exceptions.RequestException:
            return dict()

    def get_transaction(self, uid: str) -> json:
        key = "transactions/" + uid
        if not self.cache.contains(key):
            url = self.catappult_host + self.GET_TRANSACTIONS_PATH + uid
            transaction = self.__get_request(url)
            self.cache.put(key, transaction)
        return self.cache.get(key)

    def get_status(self, wallet_address: str, wallet_signature: str, uid: str):
        params = {"wallet.address": wallet_address,
                  "wallet.signature": wallet_signature}
        url = self.catappult_host + self.GET_STATUS_PATH + uid
        transaction = self.__get_request(url, params)
        return transaction["status"] if transaction else ""

    def __get_request(self, url: str, params: dict = None) -> json:
        try:
            response = requests.get(url, params=params, timeout=self.timeout)
            if response.status_code in (200, 201):
                return response.json()
            else:
                return dict()
        except requests.exceptions.RequestException:
            return dict()
