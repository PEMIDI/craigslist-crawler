import json
from abc import ABC, abstractmethod


class StorageAbstract(ABC):

    @abstractmethod
    def store(self, data, *args):
        pass

class MongoStore(StorageAbstract):

    def store(self, data, *args):
        raise NotImplementedError


class FileStore(StorageAbstract):

    def store(self, data, filename, *args):
        with open(f'fixtures/advs/{filename}.json', 'w') as f:
            f.write(json.dumps(data))
            print(f"saved in {filename}")
        print('finished')

