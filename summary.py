from google import genai

client = genai.Client(api_key="YOUR_GEMINI_API_KEY")

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents="""
    Summarize this financial news in 2 sentences:

    Infosys announced a new AI partnership and expanded its cloud services business. The company expects this move to strengthen its market position and create new revenue opportunities.
    """
)

print(response.text)