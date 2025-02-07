import os
import re
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq()

# Conservative token limit to stay well under the 6000 TPM limit
MAX_TOKENS = 5500


def truncate_text(text: str) -> tuple[str, bool]:
    """
    Truncates text to roughly stay within token limits.
    Returns tuple of (truncated_text, was_truncated).
    Using simple ratio of ~4 chars per token as rough estimate.
    """
    char_limit = MAX_TOKENS * 4
    if len(text) <= char_limit:
        return text, False

    truncated = text[:char_limit] + "..."
    return truncated, True


def summarize_text(text: str) -> str:
    """
    Uses Groq API to produce a concise summary of the provided executive order text.
    Automatically removes any content between <think> and </think> tags before summarization.
    """
    text, was_truncated = truncate_text(text)

    prompt = f"Your goal is to summarize the following executive order in a professional manner, with a focus on the key points and objectives.:\n\n{text}"
    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="deepseek-r1-distill-llama-70b",
        max_tokens=MAX_TOKENS,
    )

    # Remove content between <think> and </think> tags (including the tags themselves)
    cleaned_response = re.sub(
        r"<think>.*?</think>",
        "",
        chat_completion.choices[0].message.content,
        flags=re.DOTALL,
    ).strip()

    if was_truncated:
        cleaned_response += "\n\n<small class='text-muted'>Note: This summary is based on a portion of the full text due to length constraints.</small>"

    return cleaned_response


def format_summary(summary: str) -> str:
    """
    Formats the summary to be more readable.
    """
    # Turn content between ** into bold.
    summary = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", summary)
    return summary
