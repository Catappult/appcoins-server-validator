class ExampleDumper:
    def __init__(self):
        pass

    def create_output(self, result: bool) -> dict:
        return dict(status="SUCCESS" if result else "FAILED")
