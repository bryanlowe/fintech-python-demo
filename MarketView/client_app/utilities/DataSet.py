from pymongo import MongoClient


class DataSet():

    def __init__(self, dataset):
        self.client = MongoClient()
        self.database = self.client.market_view
        self.collection = self.database[dataset]

    # adds a market report to the overall report
    def add_report(self, report):
        self.collection.insert_one(report)




