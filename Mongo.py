import pymongo

myclient = pymongo.MongoClient('mongodb://localhost:27017/')
mydb = myclient['Test']
mycol = mydb['test']