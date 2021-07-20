"""
helpful links:
https://docs.mongodb.com/manual/reference/operator/
https://pymongo.readthedocs.io/en/stable/

"""

import datetime

from pymongo import MongoClient

cluster = 'mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&ssl=false'

client = MongoClient(cluster)

# print(client.list_database_names())
""" База с которой работаю """
db = client["test"]

# print(db.list_collection_names())
""" Таблица с которой работаю"""
todos = db.todos

todo1 = {
    "id": 1,
    "name": "Patrick",
    "text": "My second todo!",
    "status": "open",
    "tags": [
        "C++",
        "coding"
    ],
    "date": datetime.datetime.utcnow()
}

""" Insert a single document. """
# result = todos.insert_one(todo1)

todo2 = [{
    "id": 1,
    "name": "Sam",
    "text": "My first todo!",
    "status": "open",
    "tags": [
        "Java",
        "coding"
    ],
    "date": datetime.datetime.utcnow()
    },
    {
    "id": 1,
    "name": "Mary",
    "text": "My third todo!",
    "status": "open",
    "tags": [
        "JS",
        "coding"
    ],
    "date": datetime.datetime.utcnow()
    }
]

"""---------- Insert an iterable of documents ----------"""
# result = todos.insert_many(todo2)

"""---------- Get a single document from the database ----------"""
# result = todos.find_one({"name": "Sam"})
# print(result)

"""---------- many fields example ----------"""
# result = todos.find_one({"name": "Sam", "text": "My first todo!"})
# print(result)

"""---------- example for list, look at the tags ----------"""
# result = todos.find_one({"tags": "JS"})
# print(result)

"""---------- how to find for ObjectId ----------"""
# from bson.objectid import ObjectId
# result = todos.find_one({"_id": ObjectId("60aa95413d236b803d6f0884")})
# print(result)

"""---------- find() ----------"""
# results = todos.find({"name": "Mary"})
# # print(list(results)) # ! так делать нельзя
# for result in results:
#     print(result)

"""---------- Count the number of documents in this collection ----------"""
# print(todos.count_documents({})) # Output: 3

# print(todos.count_documents({"tags": "JS"})) # Output: 1

#############################
""" ADD todo4 document"""
todo4 = {
    "id": 1,
    "name": "Andy",
    "text": "My fourth todo!",
    "status": "open",
    "tags": [
        "Go",
        "coding"
    ],
    "date": datetime.datetime(2021, 1, 1, 10, 45)
}
# result = todos.insert_one(todo4)


"""---------- $lt меньше чем ----------"""
# print("---------- $lt меньше чем ----------")
#
# d = datetime.datetime(2021, 2, 1)
# # fin date less than "$lt"
# results = todos.find({"date": {"$gt": d}})
#
# for result in results:
#     print(result)


"""---------- $gt ----------"""
# print('---------- $gt ----------')
#
# d = datetime.datetime(2021, 2, 1)
# # fin date less than "$lt"
# results = todos.find({"date": {"$gt": d}})
#
# for result in results:
#     print(result)



"""---------- SORT ----------"""
# print("---------- SORT ----------")
#
# d = datetime.datetime(2021, 2, 1)
# # fin date less than "$lt"
# results = todos.find({"date": {"$gt": d}}).sort("name")
#
# for result in results:
#     print(result)


"""---------- delete_one ----------"""
# from bson.objectid import ObjectId
# result = todos.delete_one({"_id": ObjectId("60aa99a79afe035bc9d159bb")})


"""---------- delete_many ----------"""
# result = todos.delete_many({"name": "Andy"})


"""---------- delete_all ----------"""
# leave empty brackets
# result = todos.delete_many({})

"""---------- update_one - set ----------"""
result = todos.update_one({"tags": "Go"}, {"$set": {"status": "done"}})

"""---------- update_one - unset ----------"""
# result = todos.update_one({"tags": "Go"}, {"$unset": {"status": None}})
