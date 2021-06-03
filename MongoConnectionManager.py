import board_utils
import pymongo


class MongoConnectionManager:
    MONGO_PASS = board_utils.MONGO_PASS
    MONGO_USER = board_utils.MONGO_USER

    mongo_client = None

    def get_database(self):
        if self.mongo_client is None:
            self.mongo_client = pymongo.MongoClient(
                "mongodb+srv://" + self.MONGO_USER + ":" + self.MONGO_PASS + "@cluster0.wyf78.mongodb.net/DevopsEx?retryWrites=true&w=majority")
        return self.mongo_client['DevopsEx']
