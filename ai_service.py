import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analyse_email(email_body):
    prompt=f"""
        Analyze the following cutomer email and return a STRICT JSON.
        Allowerd intents:
        - refund
        - complain
        - delivery issue
        - cancellation
        - general inquiry
        Sentiment must be:
        - positive
        - neutral
        - negative
        Priority rules:
        - negative sentiment = high
        - neutral = medium
        - positive = low
        Return format for json:
        {{{
            "intent":"...",
            "sentiment":"...",
            "priority":"...",
            "draft_reply":"..."
        }}}
        Email:
        {email_body}
        """
    
    response = client.chat.completions.create(
        model="gpt-40-mini",
        messages=[
            {"role":"system","content":"You are a professional curtomer support AI."},
            {"role":"user","content":prompt}
        ],temperature=0

    )
    content = response.coices[0].message.content

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        return{
            "intent": "General Inquiry",
                "sentiment": "Neutral",
                "priority": "Medium",
                "draft_reply": "Thank you for reaching out. Our support team will get back to you shortly."
        }