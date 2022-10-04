import os
import pymongo

connection_is_open = False
mongo_client = None
connection = None
database_name = "reddit_data"


def open_connection():
    global connection_is_open, connection
    if connection_is_open:
        pass
    else:
        mongo_client = pymongo.MongoClient(
            "mongodb://localhost:27017/")
        mongo_database = mongo_client[database_name]
        connection = mongo_database
        connection_is_open = True


def close_connection():
    global connection_is_open
    mongo_client.close()
    connection_is_open = False


def get_connection():
    if connection_is_open:
        return connection
    else:
        open_connection()
        return get_connection()


def get_connection_to_collection(connection, collection_name="default"):
    mongo_container = connection[collection_name]
    return mongo_container


def insert_to_collection(collection, obj):
    collection.insert_one(obj)


def insert_to_collection_if_not_exists(collection, obj, use_match_number_as_id=False):
    if use_match_number_as_id:
        obj["_id"] = obj["metadata"]["match_id"]
    found_one = collection.find_one({"_id": obj["_id"]})
    if found_one:
        print("match already in database")
        pass
    else:
        collection.insert_one(obj)


def found_in_collection(id, collection):
    found_one = collection.find_one({"_id": id})
    if found_one:
        return True
    return False

def get_one_document_of_collection(collection):
    return collection.find_one()