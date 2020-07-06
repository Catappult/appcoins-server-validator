from flask_restx import reqparse


class ExampleParser:
    def __init__(self):
        pass

    def get_parser_adder(self) -> reqparse:
        parser = reqparse.RequestParser()
        parser.add_argument("token", help="purchaseToken")
        parser.add_argument("product", help="sku")
        return parser
