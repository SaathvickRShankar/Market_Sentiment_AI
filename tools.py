import os
import requests
from dotenv import load_dotenv
from langchain_core.tools import tool

# Load the API key from your .env file
load_dotenv()
ALPHA_VANTAGE_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")

@tool
def fetch_market_news(ticker: str) -> str:
    """
    Fetches the latest financial news and sentiment for a given stock or crypto ticker.
    Use this tool whenever a user asks about the market sentiment or news for an asset.
    """
    # We limit to 5 articles to keep the LLM context window small and fast
    url = f"https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={ticker}&limit=5&apikey={ALPHA_VANTAGE_KEY}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        # Alpha Vantage returns an informational message if the free API limit is hit
        if "Information" in data:
            return f"API Limit Reached: {data['Information']}"
            
        if "feed" not in data:
            return f"No recent news found for {ticker}."
            
        news_summary = ""
        for article in data["feed"]:
            title = article.get("title", "No Title")
            summary = article.get("summary", "No Summary")
            sentiment_label = article.get("overall_sentiment_label", "Neutral")
            
            news_summary += f"- Title: {title}\n  Summary: {summary}\n  Sentiment: {sentiment_label}\n\n"
            
        return news_summary
        
    except requests.exceptions.RequestException as e:
        return f"Error fetching news: {str(e)}"