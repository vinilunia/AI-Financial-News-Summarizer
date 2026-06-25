import requests

API_KEY = "YOUR_NEWSAPI_KEY"

url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={API_KEY}"

response = requests.get(url)

data = response.json()

import pandas as pd

articles = data["articles"]

news_list = []

for article in articles[:5]:
    news_list.append({
        "Title": article["title"],
        "Source": article["source"]["name"]
    })

df = pd.DataFrame(news_list)

print(df)

df.to_csv("news.csv", index=False)