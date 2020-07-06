import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry


class PostbackApi:
    MAX_RETRIES = 3
    DELAY_SECONDS_BETWEEN_REQUESTS = 1
    VERIFY_PATH = "/one-step/verify/"

    def __init__(self, postback_host: str, timeout=5):
        self.postback_host = postback_host
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

    def verify(self, uid: str) -> bool:
        try:
            url = self.postback_host + self.VERIFY_PATH + uid
            response = requests.get(url)
            if response.status_code == 200:
                return response.json()["verified"]
            else:
                return False
        except requests.exceptions.RequestException:
            return False
