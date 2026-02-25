import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import SystemMessage
from tools import fetch_market_news

# Load environment variables
load_dotenv()

# 1. Initialize Gemini
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)

# 2. Give the agent access to your tool
tools = [fetch_market_news]

# 3. Construct the LangGraph Agent (No system prompt here anymore)
agent_executor = create_react_agent(llm, tools)

# 4. Define the System Prompt
sys_prompt = (
    "You are a highly logical Senior Financial Analyst. "
    "Always use the fetch_market_news tool to get the latest data before answering. "
    "Your final answer MUST include a 1-word sentiment (Bullish, Bearish, or Neutral) "
    "and exactly 3 bullet points summarizing the key drivers."
)

def analyze_asset(ticker: str):
    print(f"\n--- Starting AI analysis for {ticker} using Gemini & LangGraph ---")
    try:
        # Inject the SystemMessage directly into the conversation history
        response = agent_executor.invoke({
            "messages": [
                SystemMessage(content=sys_prompt),
                ("user", f"What is the market sentiment for {ticker}?")
            ]
        })
        # Get the raw final content
        final_content = response["messages"][-1].content
        
        # THE FIX: If Gemini returns a complex list block, extract just the text
        if isinstance(final_content, list):
            return final_content[0].get("text", "Error: Could not extract text.")
        # The final answer is stored in the content of the very last message
        return final_content
    except Exception as e:
        return f"Agent failed to process the request: {str(e)}"

# --- Quick Local Test ---
if __name__ == "__main__":
    test_ticker = "BTC" 
    result = analyze_asset(test_ticker)
    print("\n=== FINAL AI OUTPUT ===")
    print(result)