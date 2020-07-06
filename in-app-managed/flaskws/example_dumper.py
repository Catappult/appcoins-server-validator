from json import dumps

from flask import Response


class ExampleDumper:
    def __init__(self):
        pass

    def get_output(self, result: bool) -> dict:
        return_code, return_json = self.__build_response(result)
        return Response(dumps(return_json), status=return_code,
                        mimetype='application/json')

    def __build_response(self, result: bool) -> (int, dict):
        if result:
            return 200, dict(status="SUCCESS")
        else:
            return 404, dict(status="FAILED")
