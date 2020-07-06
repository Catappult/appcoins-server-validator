from flask_restx import Namespace, Resource

base_api = Namespace("purchase", description="Purchase operations")


@base_api.route("/status")
class Status(Resource):
    def get(self):
        """Pings the server to ensure it is working as expected"""
        return {'status': 'OK'}
