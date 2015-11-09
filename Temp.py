#Code For Neo4j

import pymongo
from neo4jrestclient.client import GraphDatabase
db = GraphDatabase("http://localhost:7474", username="neo4j", password="sagar123")

conn = pymongo.MongoClient("localhost:27017")
db1 = conn['Wild']
coll = db1['Fire1']
docs = coll.find({"TEXT":{"$regex":"^RT"}})
i = 1
user = db.labels.create("User")
#retweet = db.labels.create("Retweet")

dict_users = {}
follower = {}

for doc in docs:
    try:

        actual_user = doc['USERNAME']
        text = doc['TEXT']
        text_list = text.split(":")
        retweet_User = text_list[0]
        retweet_User_id = retweet_User[4:]

        if actual_user not in dict_users.keys():
            #u1 = db.nodes.create(name=actual_user)
            #user.add(u1)
            #dict_users[actual_user]= u1
            follower[actual_user] = []

        #if retweet_User_id not in dict_users.keys():
            #u2 = db.nodes.create(name=retweet_User_id)
            #user.add(u2)
            #dict_users[retweet_User_id]= u2
            #u1.relationships.create("retweets",u2)

        #print i,doc['USERNAME']," Retweets ",retweet_User_id#doc['TEXT'].split(":")[0][4:]
        #i += 1
    except Exception as e:
        print e
        print "Issue in creating node"
        #i+=1

#print dict_users

i = 1

docs = coll.find({"TEXT":{"$regex":"^RT"}})
for doc in docs:
    try:

        actual_user = doc['USERNAME']
        text = doc['TEXT']
        text_list = text.split(":")
        retweet_User = text_list[0]
        retweet_User_id = retweet_User[4:]
        follower[actual_user].append(retweet_User_id)
        #dict_users[actual_user].relationships.create("retweets",dict_users[retweet_User_id])
        #print i,doc['USERNAME']," Retweets ",retweet_User_id#doc['TEXT'].split(":")[0][4:]
        #i += 1
    except Exception as e:
        print e
        print "Issue in creating relationship   "

for key,value in follower.items():
    print key , value
