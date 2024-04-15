from pymongo import MongoClient
import datetime

DB_NAME = "CPP"
DB_HOST = "localhost"
DB_PORT = 27017


# method to connect to MongoDB
def connectDataBase():
    try:
        client = MongoClient(host=DB_HOST, port=DB_PORT)
        db = client[DB_NAME]
        return db

    except:
        print("Database not connected successfully")


# creates a new document within the database
def createDocument(col, docId, docText, docTitle, docDate, docCat):

    # splits text into separate words and makes all words lowercase.
    newDoc = docText.lower().split()

    # holds all lowercase words in string excluding punctuation
    word = []

    # gets all words and gets rid of punctuation marks
    for words in newDoc:
        words = words.replace(".", "")
        words = words.replace(",", "")
        words = words.replace("!", "")
        words = words.replace("?", "")
        word.append(words)

    # dictionary to get each word and its count throughout the document
    combination = {}

    # place-holder to hold words that have already been accounted for
    holder = []

    # For loop which gets word and its word count
    for term in word:
        wordcount = 0
        for index in word:
            if term == index:
                if index in holder:
                    wordcount = wordcount + 1
                else:
                    wordcount = wordcount + 1
                    holder.append(index)
            combination[term] = wordcount

    # create a list of objects to include full term objects.
    newlist = []

    # creates element of the list of objects
    for term in combination:
        item = {
            "term": term,
            "count": combination[term],
            "num_char": len(term)
        }
        newlist.append(item)

    # document that will be inserted in the database
    doc = {
        "_id": docId,
        "docText": docText,
        "docTitle": docTitle,
        "docDate": docDate,
        "docCat": docCat,
        "terms": newlist
    }

    # command to input doc into the database
    col.insert_one(doc)


# deletes a document
def deleteDocument(col, docId):
    col.delete_one({"_id": docId})


# updates a document
def updateDocument(col, docId, docText, docTitle, docDate, docCat):
    # Delete Document
    deleteDocument(col, docId)

    # Create new with the same ID
    createDocument(col, docId, docText, docTitle, docDate, docCat)


# gets index of each document
def getIndex(col):

    # gets the embedded document of terms
    pipeline = [{"$unwind": {"path": "$terms"}}]

    # assigns query to index
    index = col.aggregate(pipeline)

    indicies = ""

    # loops through index and gets term, document title, and count
    for doc in index:
        indicies += "'" + doc["terms"]["term"] + "'" + ":" + doc["docTitle"] + ":" + str(doc["terms"]["count"]) + ", "

    return indicies
