import pandas as pd
import numpy as np
import os

file_path = "data/trends_clean.csv"

if not os.path.exists(file_path):
    print("CSV file not found!")
    exit()

df = pd.read_csv(file_path)

print("Loaded data:", df.shape)

print("\nFirst 5 rows:")
print(df.head())

avg_score = df["score"].mean()
avg_comments = df["num_comments"].mean()

print(f"\nAverage score   : {int(avg_score)}")
print(f"Average comments: {int(avg_comments)}")

scores = df["score"].values

print("\n--- NumPy Stats ---")
print("Mean score   :", int(np.mean(scores)))
print("Median score :", int(np.median(scores)))
print("Std deviation:", int(np.std(scores)))
print("Max score    :", int(np.max(scores)))
print("Min score    :", int(np.min(scores)))

category_counts = df["category"].value_counts()
top_category = category_counts.idxmax()
top_count = category_counts.max()

print(f"\nMost stories in: {top_category} ({top_count} stories)")

max_comments_row = df.loc[df["num_comments"].idxmax()]
print(f"\nMost commented story: \"{max_comments_row['title']}\" — {int(max_comments_row['num_comments'])} comments")

df["engagement"] = df["num_comments"] / (df["score"] + 1)
df["is_popular"] = df["score"] > avg_score

output_file = "data/trends_analysed.csv"
df.to_csv(output_file, index=False)

print(f"\nSaved to {output_file}")