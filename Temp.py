__author__ = 'sjha1'
#Code For Neo4j

import pymongo
from neo4jrestclient.client import GraphDatabase
db = GraphDatabase("http://localhost:7474", username="neo4j", password="sagar123")

conn = pymongo.MongoClient("localhost:27017")
db1 = conn['Elections']
coll = db1['results']
docs = coll.find({"text":{"$regex":"^RT"}})#.limit(1000)
i = 1
user = db.labels.create("User")
mylist = []
for doc in docs:
    mylist.append(doc['text'])

f = open("resulttt.txt",'w')
for each in mylist:
    f.write(each)
f.close()
    #print doc
    # try:
    #     actual_user = doc['user_name']
    #     text = doc['text']
    #     text_list = text.split(":")
    #     retweet_User = text_list[0]
    #     retweet_User_id = retweet_User[4:]
    #
    #     u1 = db.nodes.create(name=actual_user)
    #     user.add(u1)
    #     u2 = db.nodes.create(name=retweet_User_id)
    #     user.add(u2)
    #     u1.relationships.create("elects",u2)
    #
    #
    #     print i,doc['user_name']," Retweets ",retweet_User_id
    #     #doc['TEXT'].split(":")[0][4:]
    #     i += 1
    # except:
    #     print i,"-"*30
    #     i+=1
