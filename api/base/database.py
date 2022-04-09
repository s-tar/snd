import asyncio

from motor import motor_asyncio
from odmantic import AIOEngine


class MongoDatabase:
    def __init__(self):
        self.client = None
        self.engine = None

    def init(self, host, port, dbname):
        self.client = motor_asyncio.AsyncIOMotorClient(host, port)
        self.client.get_io_loop = asyncio.get_running_loop
        self.engine = AIOEngine(motor_client=self.client, database=dbname)

    def __getattr__(self, item):
        if item in self.__dict__:
            return self.__dict__[item]
        else:
            return getattr(self.engine, item)


database = MongoDatabase()
