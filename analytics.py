from pymongo import MongoClient
import pandas as pd

# =========================

# MongoDB Connection

# =========================
MONGO_URI = "mongodb+srv://amrataailani1_db_student:Amrata_Ailani09@clusterincubien.016ut4y.mongodb.net/?appName=Clusterincubien"

client = MongoClient(MONGO_URI)

db = client["Incubien_Foundaion"]
collection = db["post_metrics"]

# =========================

# Fetch Data

# =========================

data = list(collection.find())

if len(data) == 0:
    print("No data found in database!")
    exit()

df = pd.DataFrame(data)

# =========================

# Handle Missing Values

# =========================

for col in ["likes", "comments", "shares", "reach", "impressions", "views"]:

    if col not in df.columns:
        df[col] = 0

df["likes"] = df["likes"].fillna(0)
df["comments"] = df["comments"].fillna(0)
df["shares"] = df["shares"].fillna(0)
df["reach"] = df["reach"].fillna(1)
df["impressions"] = df["impressions"].fillna(0)
df["views"] = df["views"].fillna(0)

# =========================

# Dashboard Analytics

# =========================

print("\n========== ANALYTICS DASHBOARD ==========\n")

print("Total Posts:", len(df))
print("Total Likes:", df["likes"].sum())
print("Average Reach:", round(df["reach"].mean(), 2))
print("Total Impressions:", df["impressions"].sum())
print("Total Views:", df["views"].sum())

# =========================

# Engagement Rate

# =========================

df["engagement_rate"] = (
(df["likes"] + df["comments"] + df["shares"])
/ df["reach"]
) * 100

print("\n========== ENGAGEMENT RATE ==========\n")
print(df[["post_id", "engagement_rate"]])

# =========================

# Viral Score

# =========================

df["viral_score"] = (
(df["likes"] * 0.4)
+ (df["comments"] * 0.3)
+ (df["shares"] * 0.3)
)

print("\n========== VIRAL SCORE ==========\n")
print(df[["post_id", "viral_score"]])

# =========================

# Best Post

# =========================

best_post = df.loc[df["engagement_rate"].idxmax()]

print("\n========== BEST POST ==========\n")
print("Post ID:", best_post["post_id"])
print("Platform:", best_post["platform"])
print("Engagement Rate:", round(best_post["engagement_rate"], 2), "%")

# =========================

# Worst Post

# =========================

worst_post = df.loc[df["engagement_rate"].idxmin()]

print("\n========== WORST POST ==========\n")
print("Post ID:", worst_post["post_id"])
print("Platform:", worst_post["platform"])
print("Engagement Rate:", round(worst_post["engagement_rate"], 2), "%")

# =========================

# Improvement Suggestions

# =========================

print("\n========== IMPROVEMENT SUGGESTIONS ==========\n")

for index, row in df.iterrows():
    print(f"\nPost: {row['post_id']}")

    if row["engagement_rate"] < 3:
        print("Status: Weak Post")
        print("Suggestion: Better hashtags use karo")
        print("Suggestion: Strong CTA add karo")
        print("Suggestion: College-specific audience target karo")

    elif row["engagement_rate"] < 6:
        print("Status: Average Post")
        print("Suggestion: Caption improve karo")
        print("Suggestion: Trending hashtags add karo")
        print("Suggestion: More shares generate karo")

    else:
        print("Status: Good Post")
        print("Suggestion: Similar content aur banao")


print("\n========== ANALYSIS COMPLETED ==========")
