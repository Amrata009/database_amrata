from pymongo import MongoClient
import pandas as pd
import matplotlib.pyplot as plt

# =========================
# MongoDB Connection
# =========================

MONGO_URI = "mongodb+srv://amrataailani1_db_student:Amrata_Ailani09@clusterincubien.016ut4y.mongodb.net/?appName=Clusterincubien"

client = MongoClient(MONGO_URI)

db = client["Incubien_Foundaion"]
collection = db["social_media_analytics"]

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

required_columns = [
    "content_id",
    "platform",
    "likes",
    "comments",
    "shares",
    "saves",
    "views",
    "followers",
    "growth_rate",
    "ctr",
    "consistency_score"
]

for col in required_columns:
    if col not in df.columns:
        df[col] = 0

df["likes"] = df["likes"].fillna(0)
df["comments"] = df["comments"].fillna(0)
df["shares"] = df["shares"].fillna(0)
df["saves"] = df["saves"].fillna(0)
df["views"] = df["views"].fillna(1)
df["followers"] = df["followers"].fillna(0)
df["growth_rate"] = df["growth_rate"].fillna(0)
df["ctr"] = df["ctr"].fillna(0)
df["consistency_score"] = df["consistency_score"].fillna(0)

# =========================
# Dashboard Analytics
# =========================

print("\n========== ANALYTICS DASHBOARD ==========\n")

print("Total Content:", len(df))
print("Total Likes:", df["likes"].sum())
print("Total Comments:", df["comments"].sum())
print("Total Shares:", df["shares"].sum())
print("Total Saves:", df["saves"].sum())
print("Total Views:", df["views"].sum())
print("Average Followers:", round(df["followers"].mean(), 2))

# =========================
# Engagement Rate
# =========================

df["engagement_rate"] = (
    (
        df["likes"]
        + df["comments"]
        + df["shares"]
        + df["saves"]
    )
    / df["views"]
) * 100

print("\n========== ENGAGEMENT RATE ==========\n")
print(df[["content_id", "engagement_rate"]])

# =========================
# Viral Score
# =========================

df["viral_score"] = (
    (df["likes"] * 0.4)
    + (df["comments"] * 0.2)
    + (df["shares"] * 0.3)
    + (df["saves"] * 0.1)
)

print("\n========== VIRAL SCORE ==========\n")
print(df[["content_id", "viral_score"]])

# =========================
# Performance Score
# =========================

df["performance_score"] = (
    (df["engagement_rate"] * 0.4)
    + (df["growth_rate"] * 0.3)
    + (df["ctr"] * 0.2)
    + (df["consistency_score"] * 0.1)
)

print("\n========== PERFORMANCE SCORE ==========\n")
print(df[["content_id", "performance_score"]])

# =========================
# Best Content
# =========================

best_content = df.loc[df["performance_score"].idxmax()]

print("\n========== BEST CONTENT ==========\n")

print("Content ID:", best_content["content_id"])
print("Platform:", best_content["platform"])
print("Performance Score:",
      round(best_content["performance_score"], 2))

# =========================
# Worst Content
# =========================

worst_content = df.loc[df["performance_score"].idxmin()]

print("\n========== WORST CONTENT ==========\n")

print("Content ID:", worst_content["content_id"])
print("Platform:", worst_content["platform"])
print("Performance Score:",
      round(worst_content["performance_score"], 2))

# =========================
# Platform Analysis
# =========================

print("\n========== PLATFORM ANALYSIS ==========\n")

platform_summary = (
    df.groupby("platform")
    .agg({
        "likes": "sum",
        "views": "sum",
        "performance_score": "mean"
    })
)

print(platform_summary)

# =========================
# Improvement Suggestions
# =========================

print("\n========== IMPROVEMENT SUGGESTIONS ==========\n")

for index, row in df.iterrows():

    print(f"\nContent: {row['content_id']}")
    print(f"Platform: {row['platform']}")

    score = row["performance_score"]

    if score < 10:

        print("Status: Weak Content")
        print("Suggestion: Better hashtags use karo")
        print("Suggestion: Strong CTA add karo")
        print("Suggestion: Posting frequency increase karo")
        print("Suggestion: Audience targeting improve karo")

    elif score < 12:

        print("Status: Average Content")
        print("Suggestion: Caption improve karo")
        print("Suggestion: Trending hashtags add karo")
        print("Suggestion: More shares generate karo")

    else:

        print("Status: High Performing Content")
        print("Suggestion: Similar content aur banao")
        print("Suggestion: Promote this content")
        print("Suggestion: Reuse successful strategy")

print("\n========== ANALYSIS COMPLETED ==========")
# =========================
# VISUALIZATION
# =========================

# Engagement Rate Chart

plt.figure(figsize=(10,5))
plt.bar(df["content_id"], df["engagement_rate"])

plt.title("Engagement Rate by Content")
plt.xlabel("Content ID")
plt.ylabel("Engagement Rate (%)")

plt.show()

# Performance Score Chart

plt.figure(figsize=(10,5))
plt.bar(df["content_id"], df["performance_score"])

plt.title("Performance Score by Content")
plt.xlabel("Content ID")
plt.ylabel("Performance Score")

plt.show()

# Platform Views Pie Chart

platform_views = df.groupby("platform")["views"].sum()

plt.figure(figsize=(8,8))

plt.pie(
    platform_views,
    labels=platform_views.index,
    autopct="%1.1f%%"
)

plt.title("Platform Wise Views Distribution")

plt.show()