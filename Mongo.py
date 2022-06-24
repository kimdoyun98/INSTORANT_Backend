import pymongo

myclient = pymongo.MongoClient('mongodb://175.106.96.235:27017/')
mydb = myclient['Test']
mycol = mydb['test']
