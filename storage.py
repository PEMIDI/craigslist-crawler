import json
from abc import ABC, abstractmethod
from mongo import MongoDatabase

class StorageAbstract(ABC):

    @abstractmethod
    def store(self, data, *args):
        pass


class MongoStore(StorageAbstract):

    def __init__(self):
        self.mongo = MongoDatabase()

    def store(self, data, collection, *args):
        collection = getattr(self.mongo.database, collection)
        if isinstance(data, list) and len(data) > 1:
            collection.insert_many(data)
        else:
            collection.insert_one(data)


class FileStore(StorageAbstract):

    def store(self, data, filename, *args):
        with open(f'fixtures/advs/{filename}.json', 'w') as f:
            f.write(json.dumps(data))
            print(f"saved in {filename}")
        print('finished')


