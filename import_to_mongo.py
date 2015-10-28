__author__ = 'sjha1'
#!/usr/bin/env python

import sys, getopt, csv, pprint
from pymongo import MongoClient
from constants import *

global_mongo = None
global_db = None
global_coll = None

def usage(msg):
  if msg != None:
    print '\nError: {msg}'.format(msg=msg)

  print '\nUsage: {arg0} [options]\n'.format(arg0=sys.argv[0])
  print '  Options:\n'
  print '      -h ......................... Display this help message\n'
  print '      -f|--file=CSVFILE .......... The CSV file to load\n'
  print '      -m|--mongo=MONGOINSTANCE ... The mongo instance to load the file into\n'
  sys.exit(0)

def add_record_to_mongo(database,collection, record,text):
  global global_mongo
  global global_db
  global global_coll

  #mongo_bits = mongo.split('.')
  mongo_db = database#mongo_bits[0]
  mongo_coll = collection#mongo_bits[1]
  print 'Load a record!\n'
  pprint.pprint(record)

  if global_mongo == None: global_mongo = MongoClient()
  if global_db == None: global_db = global_mongo[mongo_db]
  if global_coll == None: global_coll = global_db[mongo_coll]

  # Now let's insert
  #print 'DB: {db} and COLL: {coll}'.format(db=global_db,coll=global_coll)
  doc = 'DB: {db} and COLL: {coll}'.format(db=global_db,coll=global_coll)
  writeCalculations(text,record,False,None)
  global_coll.insert(record)

def run_csv_file(csvfile, database,collection,text):
  print 'Gonna load the CSV file "{csvfile}" into mongodb "{mongo}"\n'.format(csvfile=csvfile, mongo=str(database)+":"+str(collection))
  with open(csvfile,'rb') as incsv:
    parsed = csv.DictReader(incsv, delimiter=',', quotechar='"')
    for record in parsed:
      add_record_to_mongo(database,collection, record,text)

def load_csv(csvfile,database,collection,text):

  #if csvfile == None: usage('Missing CSV file')
  #if mongo == None: usage('Missing mongo')

  run_csv_file(csvfile, database,collection,text)



