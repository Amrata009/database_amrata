from pymongo import MongoClient

client = MongoClient("mongodb+srv://amrataailani1_db_student:Amrata_Ailani09@clusterincubien.016ut4y.mongodb.net/?appName=Clusterincubien")

db = client["Incubien_Foundaion"]

for doc in db["post_metrics"].find():
    print(doc)