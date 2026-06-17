from pymongo import MongoClient

MONGO_URI = "mongodb+srv://amrataailani1_db_student:Amrata_Ailani09@clusterincubien.016ut4y.mongodb.net/?appName=Clusterincubien"

client = MongoClient(MONGO_URI)

db = client["Incubien_Foundaion"]

collection = db["social_media_analytics"]

print("Documents:", collection.count_documents({}))
print(collection.count_documents({}))