import requests
import time
import json
import os
from datetime import datetime

TOP_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"

headers = {"User-Agent": "TrendPulse/1.0"}

CATEGORIES = {
    "technology": ["ai", "software", "tech", "code", "computer", "data", "cloud", "api", "gpu", "llm"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports": ["nfl", "nba", "fifa", "sport", "game", "team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "nasa", "genome"],
    "entertainment": ["movie", "film", "music", "netflix", "game", "book", "show", "award", "streaming"]
}

def get_category(title):
    title = title.lower()
    for category, keywords in CATEGORIES.items():
        for word in keywords:
            if word in title:
                return category
    return None

def main():
    all_posts = []
    category_count = {cat: 0 for cat in CATEGORIES}

    try:
        response = requests.get(TOP_URL, headers=headers)
        story_ids = response.json()[:1000]
    except:
        print("Error fetching top stories")
        return

    print("Fetching and processing stories...")

    for story_id in story_ids:
        try:
            url = ITEM_URL.format(story_id)
            res = requests.get(url, headers=headers)
            story = res.json()

            if story is None or "title" not in story:
                continue

            title = story["title"]
            category = get_category(title)

            if category and category_count[category] < 25:
                chosen_category = category
            else:
                chosen_category = min(category_count, key=category_count.get)
                if category_count[chosen_category] >= 25:
                    continue

            post = {
                "post_id": story.get("id"),
                "title": title,
                "category": chosen_category,
                "score": story.get("score", 0),
                "num_comments": story.get("descendants", 0),
                "author": story.get("by", "unknown"),
                "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            all_posts.append(post)
            category_count[chosen_category] += 1

            print(f"Added ({chosen_category}): {title}")

            if len(all_posts) >= 110:
                break

        except:
            print(f"Error fetching story {story_id}")
            continue

    time.sleep(2)

    if not os.path.exists("data"):
        os.makedirs("data")

    filename = f"data/trends_{datetime.now().strftime('%Y%m%d')}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(all_posts, f, indent=4)

    print(f"\nCollected {len(all_posts)} stories. Saved to {filename}")

if __name__ == "__main__":
    main()