#Code For Neo4j

import pymongo
from neo4jrestclient.client import GraphDatabase
db = GraphDatabase("http://localhost:7474", username="neo4j", password="sagar123")

conn = pymongo.MongoClient("localhost:27017")
db1 = conn['Wild']
coll = db1['RockyFire']
docs = coll.find({"TEXT":{"$regex":"^RT"}})#.limit(3)
i = 1
user = db.labels.create("User")
#retweet = db.labels.create("Retweet")
for doc in docs:
    try:

        actual_user = doc['USERNAME']
        text = doc['TEXT']
        text_list = text.split(":")
        retweet_User = text_list[0]
        retweet_User_id = retweet_User[4:]



        u1 = db.nodes.create(name=actual_user)
        user.add(u1)
        u2 = db.nodes.create(name=retweet_User_id)
        user.add(u2)
        u1.relationships.create("retweets",u2)


        print i,doc['USERNAME']," Retweets ",retweet_User_id#doc['TEXT'].split(":")[0][4:]
        i += 1
    except:
        print "-"*30
        #i+=1

# from neo4jrestclient.client import GraphDatabase
#
# db = GraphDatabase("http://localhost:7474", username="neo4j", password="sagar123")
#
# # Create some nodes with labels
# user = db.labels.create("User")
# u1 = db.nodes.create(name="Marco")
# user.add(u1)
# u2 = db.nodes.create(name="Daniela")
# user.add(u2)
#
# beer = db.labels.create("Beer")
# b1 = db.nodes.create(name="Punk IPA")
# b2 = db.nodes.create(name="Hoegaarden Rosee")
# # You can associate a label with many nodes in one go
# beer.add(b1, b2)