from flask import Flask
from gevent.pywsgi import WSGIServer

import settings
from flaskws.api_factory import ApiFactory

api_factory = ApiFactory()
api = api_factory.get_api()

app = Flask(__name__)
api.init_app(app)


if __name__ == "__main__":
    if settings.ENVIRONMENT == settings.Environments.PRODUCTION:
        http_server = WSGIServer((settings.API_HOST, settings.API_PORT),
                                 application=app)
        http_server.serve_forever()
    else:
        app.run(host=settings.API_HOST, port=settings.API_PORT, debug=settings.DEBUG)