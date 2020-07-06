from flask import url_for
from flask_restx import Api

from src.flaskws.base_api import base_api
from src.flaskws.example_api import example_api


class SwaggerApi(Api):
    """
    This is a modification of the base Flask Restplus Api class due
    to the issue described here
    https://github.com/noirbizarre/flask-restplus/issues/223
    """

    @property
    def specs_url(self):
        """
        The Swagger specifications absolute url (ie. `swagger.json`)
        :rtype: str
        """
        return url_for(self.endpoint("specs"), _external=False)


class ApiFactory:
    def __init__(self):
        self.api = None

    def get_api(self):
        if not self.api:
            self.api = self.__create_api()
        return self.api

    def __create_api(self) -> SwaggerApi:
        api = SwaggerApi(
            version="1.0",
            title="API testing",
            description="One step payment with credits"
        )

        api.add_namespace(base_api, "/base")
        api.add_namespace(example_api, "/one-step")
        return api
