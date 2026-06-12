from pymongo import MongoClient

client = MongoClient("mongodb+srv://amrataailani1_db_student:Amrata_Ailani09@clusterincubien.016ut4y.mongodb.net/?appName=Clusterincubien")

db = client["Incubien_Foundaion"]

print("Documents in post_metrics:",
      db["post_metrics"].count_documents({}))