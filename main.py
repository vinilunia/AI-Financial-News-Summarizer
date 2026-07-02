import streamlit as st
import requests
import pandas as pd
from google import genai

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(
    page_title="AI Financial News Summarizer",
    page_icon="📰",
    layout="wide"
)

st.title("📰 AI Financial News Summarizer")
st.markdown("Get the latest news about any company and generate AI summaries.")

# -------------------------------
# SIDEBAR
# -------------------------------
st.sidebar.header("Settings")

news_api_key = st.sidebar.text_input(
    "NewsAPI Key",
    type="password"
)

gemini_api_key = st.sidebar.text_input(
    "Gemini API Key",
    type="password"
)

company = st.text_input(
    "Enter Company Name",
    placeholder="Tesla, Apple, Infosys, Microsoft..."
)

# -------------------------------
# FETCH NEWS
# -------------------------------
if st.button("Fetch News"):

    if not news_api_key:
        st.error("Please enter your NewsAPI key.")
        st.stop()

    url = (
        f"https://newsapi.org/v2/everything?"
        f"q={company}&language=en&sortBy=publishedAt&apiKey={news_api_key}"
    )

    with st.spinner("Fetching latest news..."):
        response = requests.get(url)
        data = response.json()

    articles = data.get("articles", [])

    if not articles:
        st.warning("No news found.")
        st.stop()

    news_data = []

    for article in articles[:10]:
        news_data.append({
            "Title": article["title"],
            "Source": article["source"]["name"],
            "URL": article["url"]
        })

    df = pd.DataFrame(news_data)

    st.subheader("Latest Headlines")
    st.dataframe(df, use_container_width=True)

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "Download CSV",
        csv,
        file_name="financial_news.csv",
        mime="text/csv"
    )

    # -------------------------------
    # AI SUMMARY
    # -------------------------------
    if gemini_api_key:

        client = genai.Client(api_key=gemini_api_key)

        headline_text = "\n".join(df["Title"].tolist())

        prompt = f"""
        Summarize the following financial news headlines about {company}
        in 5 concise bullet points:

        {headline_text}
        """

        with st.spinner("Generating AI Summary..."):
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt
            )

        st.subheader("🤖 AI Summary")
        st.write(response.text)
