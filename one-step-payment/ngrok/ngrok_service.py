import logging

from pyngrok import ngrok


class NgrokService:
    def __init__(self):
        self.ngrok_host = None
        self.logger = logging.getLogger("NgrokService")

    def start(self, port: int):
        self.ngrok_host = ngrok.connect(port, "http")
        self.logger.info("Started ngrok client at '{}'".format(self.ngrok_host))

    def get_url(self):
        return self.ngrok_host

    def stop(self):
        ngrok.kill()
