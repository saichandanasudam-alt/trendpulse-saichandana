import pandas as pd
import matplotlib.pyplot as plt
import os

file_path = "data/trends_analysed.csv"

if not os.path.exists(file_path):
    print("File not found!")
    exit()

df = pd.read_csv(file_path)

if not os.path.exists("outputs"):
    os.makedirs("outputs")

top_stories = df.sort_values(by="score", ascending=False).head(10)
titles = top_stories["title"].apply(lambda x: x[:50] + "..." if len(x) > 50 else x)

plt.figure()
plt.barh(titles, top_stories["score"])
plt.xlabel("Score")
plt.ylabel("Title")
plt.title("Top 10 Stories by Score")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig("outputs/chart1_top_stories.png")
plt.close()

category_counts = df["category"].value_counts()

plt.figure()
plt.bar(category_counts.index, category_counts.values)
plt.xlabel("Category")
plt.ylabel("Number of Stories")
plt.title("Stories per Category")
plt.tight_layout()
plt.savefig("outputs/chart2_categories.png")
plt.close()

plt.figure()
popular = df[df["is_popular"] == True]
not_popular = df[df["is_popular"] == False]

plt.scatter(popular["score"], popular["num_comments"], label="Popular")
plt.scatter(not_popular["score"], not_popular["num_comments"], label="Not Popular")

plt.xlabel("Score")
plt.ylabel("Number of Comments")
plt.title("Score vs Comments")
plt.legend()
plt.tight_layout()
plt.savefig("outputs/chart3_scatter.png")
plt.close()

fig, axs = plt.subplots(1, 3, figsize=(18, 5))

axs[0].barh(titles, top_stories["score"])
axs[0].set_title("Top Stories")
axs[0].invert_yaxis()

axs[1].bar(category_counts.index, category_counts.values)
axs[1].set_title("Categories")

axs[2].scatter(popular["score"], popular["num_comments"], label="Popular")
axs[2].scatter(not_popular["score"], not_popular["num_comments"], label="Not Popular")
axs[2].set_title("Score vs Comments")
axs[2].legend()

fig.suptitle("TrendPulse Dashboard")
plt.tight_layout()
plt.savefig("outputs/dashboard.png")
plt.close()

print("Charts saved in outputs/ folder")