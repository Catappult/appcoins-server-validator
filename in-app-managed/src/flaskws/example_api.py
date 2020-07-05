import re
from json import dumps

from flask import Response, request
from flask_restx import Resource, abort, Namespace

from src import settings
from src.classes.api_validator import (
    APIValidator, APIValidatorException
)
from src.classes.cache import Cache
from src.classes.catappult_api import CatappultApi
from src.classes.purchase_entity import PurchaseEntity
from src.flaskws.example_dumper import ExampleDumper
from src.flaskws.example_parser import ExampleParser

example_api = Namespace("purchase", description="Purchase operations")
example_parser = ExampleParser()
catappult_api = CatappultApi(settings.CATAPPULT_API_HOST, Cache())
api_validator = APIValidator(catappult_api)
dumper = ExampleDumper()


def parse_purchase_check_url(url):
    match = re.fullmatch(
        r"http.*://(?P<domain>[0-9a-zA-Z.:-]+)/purchase/(?P<package>["
        r"0-9a-zA-Z.]+)/check",
        url)
    return match.group("domain"), match.group("package")


@example_api.route("/com.appcoins.trivialdrivesample/check")
@example_api.route("/com.appcoins.sample/check")
@example_api.route("/test.unity.serverside/check")
@example_api.route("/com.appcoins.trivialdrivesample.test/check")
class ExampleCheck(Resource):
    @example_api.expect(example_parser.get_parser_adder())
    @example_api.response(200, "Success")
    @example_api.response(400, "Bad purchase")
    @example_api.response(503, "Service Unavailable")
    @example_api.response(504, "Gateway timeout")
    def get(self):
        args = example_parser.get_parser_adder().parse_args()
        _, package_name = parse_purchase_check_url(request.base_url)

        purchase = PurchaseEntity(package_name, args.token, args.product)

        if not purchase.package_name or not purchase.sku \
                or not purchase.purchase_token:
            abort(code=400, error="ERROR-400-1", status=None,
                  message="A valid purchase must be provided")

        try:
            raw_result = api_validator.validate(purchase)
            parsed_result = dumper.create_output(raw_result)

            return Response(dumps(parsed_result), status=200,
                            mimetype='application/json')
        except APIValidatorException as e:
            abort(code=503, error="ERROR-503-1", status=None, message=str(e))
