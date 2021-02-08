from pymongo import MongoClient


class MongoDatabase:
    instance = None

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super().__new__(*args, **kwargs)
        return cls.instance

    def __init__(self):
        self.mongo = MongoClient()
        self.database = self.mongo['crawler']