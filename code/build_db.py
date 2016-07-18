import csv, ujson
from pymongo import MongoClient

def insert_classifications(file, collection):
    
    with open(file,"rb") as csvFile:
        reader = csv.reader(csvFile)
        for line in reader:
            if "classification_id" in line:
                keys = line
                continue

            doc = {}
            for i,key in enumerate(keys):
                try:
                    doc[key] = ujson.loads(line[i])
                except ValueError:
                    doc[key] = line[i]
            result = collection.insert_one(doc)
            print result.inserted_id
    return True

def insert_subjects(file, collection):
    
    with open(file,"rb") as csvFile:
        reader = csv.reader(csvFile)
        for line in reader:
            if "subject_id" in line:
                keys = line
                continue
            
            doc = {}
            for i,key in enumerate(keys):
                try:
                    doc[key] = ujson.loads(line[i])
                except ValueError:
                    doc[key] = line[i]
            result = collection.insert_one(doc)
            print result.inserted_id
    return True

def insert_aggregations(file, collection):
    
    with open(file,"rb") as csvFile:
        reader = csv.reader(csvFile)
        for line in reader:
            if "subject_id" in line:
                keys = line
                continue
            
            doc = {}
            for i,key in enumerate(keys):
                try:
                    doc[key] = ujson.loads(line[i])
                except ValueError:
                    doc[key] = line[i]
            result = collection.insert_one(doc)
            print result.inserted_id
    return True

def build_classifications_collection(client, db):
    file = "../data/supernova-hunters-classifications.csv"
    
    collection = db["classifications"]
    
    insert_classifications(file, collection)
    
    cursor = collection.find()
    print cursor.count()

def build_subjects_collection(client, db):
    file = "../data/supernova-hunters-subjects.csv"
    
    collection = db["subjects"]
    
    insert_subjects(file, collection)
    
    cursor = collection.find()
    print cursor.count()

def build_aggregations_collection(client, db):
    file = "../data/2455/1737_Real_or_Bogus/" +\
           "T1Does_the_source_centred_in_the_green_crosshairs_in_summary.csv"
    
    collection = db["aggregations"]
    
    insert_subjects(file, collection)
    
    cursor = collection.find()
    print cursor.count()

def main():

    client = MongoClient()
    
    db = client.SNHunters
    
    #build_classifications_collection(client, db)

    #build_subjects_collection(client, db)

    #build_aggregations_collection(client, db)

    cursor = db["aggregations"].find()
    print cursor.count()
    
    #for doc in cursor:
    #    print doc

if __name__ == "__main__":
    main()