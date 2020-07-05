class Cache:
    def __init__(self):
        self.cache = {}

    def contains(self, key):
        return key in self.cache

    def put(self, key, value):
        self.cache[key] = value

    def get(self, key):
        return self.cache[key]
