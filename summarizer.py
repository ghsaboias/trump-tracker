import os
import re
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq()

def summarize_text(text: str) -> str:
    """
    Uses Groq API to produce a concise summary of the provided executive order text.
    Automatically removes any content between <think> and </think> tags before summarization.
    """
    
    prompt = f"Summarize the following executive order in a professional manner, with a focus on the key points and objectives:\n\n{text}"
    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="deepseek-r1-distill-llama-70b",
        max_tokens=4000,
    )

    # Remove content between <think> and </think> tags (including the tags themselves)
    cleaned_response = re.sub(r'<think>.*?</think>', '', chat_completion.choices[0].message.content, flags=re.DOTALL).strip()
    return cleaned_response

def format_summary(summary: str) -> str:
    """
    Formats the summary to be more readable.
    """
    # Turn content between ** into bold.
    summary = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', summary)
    return summary