import pymongo

myclient = pymongo.MongoClient('mongodb://MOONYOONHO:20171149@localhost:27017/')
mydb = myclient['Test']
mycol = mydb['test']
