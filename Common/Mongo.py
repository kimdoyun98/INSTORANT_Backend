import pymongo

myclient = pymongo.MongoClient('mongodb://MOONYOONHO:20171149@localhost:27017/')

mydb = myclient['Test']
mycol = mydb['test']


# mycol.insert_one({
#     "name": "Central Park",
#     "location": {"type": "Point", "coordinates": [-73.97, 40.77]},
#     "category": "Parks"
# })
#
# mycol.insert_one( {
#    "name": "Sara D. Roosevelt Park",
#    "location": { "type": "Point", "coordinates": [ -73.9928, 40.7193 ] },
#    "category": "Parks"
# });
# mycol.insert_one( {
#    "name": "Polo Grounds",
#        "location": { "type": "Point", "coordinates": [ -73.9375, 40.8303 ] },
#    "category": "Stadiums"
# } );
#
# mycol.create_index([('location', '2dsphere')])

# a = mycol.find({
#      "location":
#        { "$near":
#           {
#             "$geometry": { "type": "Point",  "coordinates": [ -73.9667, 40.78 ] },
#             "$minDistance": 1000,
#             "$maxDistance": 5000
#           }
#        }
#    }
# )
# print(a)
# b = []
# for i in a:
#     b.append(i)
#
# print(b)