import json
from abc import ABC, abstractmethod
from mongo import MongoDatabase

class StorageAbstract(ABC):

    @abstractmethod
    def store(self, data, *args):
        pass

    @abstractmethod
    def load(self, *args, **kwargs):
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

    def load(self, collection_name, filter_data=None):
        collection = self.mongo.database[collection_name]
        if filter_data is not None:
            data = collection.find(filter_data)
        else:
            data = collection.find()
        return data

    def update_flag(self, data):
        """
        get a link with flag=False variable, and change flag to True

        :param data: a data with url parameter
        :return: Flag:True
        """
        return self.mongo.database.adv_links.find_one_and_update(
            {'_id': data['_id']},
            {'$set': {'flag': 'True'}}
        )


class FileStore(StorageAbstract):

    def store(self, data, filename, *args):
        with open(f'fixtures/advs/{filename}.json', 'w') as f:
            f.write(json.dumps(data))
            print(f"saved in {filename}")
        print('finished')

    @staticmethod
    def load():
        with open('fixtures/links.json', 'r') as f:
            result = json.loads(f.read())
            print(f"{result} \n")
        return result

    def update_flag(self):
        pass


