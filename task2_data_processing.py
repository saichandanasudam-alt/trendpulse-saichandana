import pandas as pd
import os

file_path = "data/trends_20260403.json"

if not os.path.exists(file_path):
    print("JSON file not found!")
    exit()

df = pd.read_json(file_path)

print(f"Loaded {len(df)} stories from {file_path}")

df = df.drop_duplicates(subset="post_id")
print(f"After removing duplicates: {len(df)}")

df = df.dropna(subset=["post_id", "title", "score"])
print(f"After removing nulls: {len(df)}")

df["score"] = df["score"].astype(int)
df["num_comments"] = df["num_comments"].astype(int)

df = df[df["score"] >= 5]
print(f"After removing low scores: {len(df)}")

df["title"] = df["title"].str.strip()

output_file = "data/trends_clean.csv"
df.to_csv(output_file, index=False)

print(f"\nSaved {len(df)} rows to {output_file}")

print("\nStories per category:")
print(df["category"].value_counts())