from enum import Enum

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

from classes.cache import Cache


class CatappultApiErrorCodes(Enum):
    API_UNAVAILABLE_CODE = -1


class CatappultApi:
    MAX_RETRIES = 3
    DELAY_SECONDS_BETWEEN_REQUESTS = 1
    PRODUCT_PATH = ("/product/8.20191001/inapp/google/v3/applications/"
                    "{package_name}/purchases/products/{sku}/tokens/"
                    "{purchase_token}")

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

    def get_purchase_status(self, package_name: str, sku: str,
                            purchase_token: str) -> int:
        key = "token/" + purchase_token
        if not self.cache.contains(key):
            url = self.__build_url(package_name, sku, purchase_token)
            purchase_status = self.__make_request(url)
            self.cache.put(key, purchase_status)
        return self.cache.get(key)

    def __build_url(self, package_name: str, sku: str,
                    purchase_token: str) -> str:
        return self.catappult_host + self.PRODUCT_PATH.format(
            package_name=package_name, sku=sku, purchase_token=purchase_token)

    def __make_request(self, url: str) -> int:
        try:
            response = requests.get(url, timeout=self.timeout)
            return response.status_code
        except requests.exceptions.RequestException:
            return CatappultApiErrorCodes.API_UNAVAILABLE_CODE.value
