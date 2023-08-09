import requests
import pymongo
import json
from dotenv import load_dotenv
import os

import time

load_dotenv()
api_key=os.getenv('API_KEY')

def connectdb():
    from pymongo.mongo_client import MongoClient
    uri = "mongodb://sddeepakk0806:123@ac-znrzsk4-shard-00-00.x4poyk7.mongodb.net:27017,ac-znrzsk4-shard-00-01.x4poyk7.mongodb.net:27017,ac-znrzsk4-shard-00-02.x4poyk7.mongodb.net:27017/?ssl=true&replicaSet=atlas-n6vx3x-shard-0&authSource=admin&retryWrites=true&w=majority"
    
    client = MongoClient(uri)
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)
    return client


def insert():
    client=connectdb()
    city_name =["Toronto","Vancouver","Ottawa","Montreal","Calgary"]
    state_code=["ON","BC","ON","QC","AB"]
    country_code="Canada"
    for x in range(5):
        response=requests.get(f'http://api.openweathermap.org/geo/1.0/direct?q={city_name[x]},{state_code[x]},{country_code}&&appid={api_key}').json()
        data=response[0]
        lat,lon=data.get('lat'),data.get('lon')
        resp=requests.get(f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric').json()
        
        
        db=client.test
        collection=db[city_name[x]]
        count=collection.count_documents({})
        if count>=10:
            documentid=collection.find_one()
            collection.delete_one({"_id": documentid["_id"]})
        collection.insert_one(resp)
        
  
def getdata(city):
    client=connectdb()
    db=client.test
    collection=db[city]
    # documents = collection.find()
    # json_data = json.dumps([doc for doc in documents], default=str, indent=2)
    # print(json_data)
    documents = collection.find()
    dict = {}
    for doc in documents:
        dict[doc["_id"]] = doc
    # print(dict)

    return dict
#     keys_view = dict.keys()

# # Convert the view to a list if needed
    
#     keys_list = list(keys_view)
#     for key in keys_list:
        # print(dict.get(key).get('name'))
        # print(dict.get(key).get('main').get('temp'))
    # print(dict.get('ObjectId')[0].get('weather')[0].get('main'))
    # print(dict.get('ObjectId')[0].get('weather')[0].get('main'))

