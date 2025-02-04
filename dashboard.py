import os
import json
import logging
import requests  # add requests to fetch raw text if needed
from flask import Flask, render_template, abort, request, jsonify
from summarizer import summarize_text, format_summary  # import our summary helper and format_summary

# Set up basic logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

app = Flask(__name__)

# Directory where cached executive order JSON files are stored
EXECUTIVE_ORDERS_DIR = os.path.join(os.getcwd(), "executive_orders")

@app.route('/')
def index():
    """
    Main route that lists all cached executive orders.
    Reads the 'executive_orders' directory, loads each JSON file,
    and extracts summary information (document number, title, signing date,
    and publication date). Supports sorting by 'signing_date' or 'publication_date'
    using query parameters 'sort_by' and 'sort_order'.
    """
    orders = []
    if os.path.exists(EXECUTIVE_ORDERS_DIR):
        for filename in os.listdir(EXECUTIVE_ORDERS_DIR):
            if filename.endswith(".json"):
                filepath = os.path.join(EXECUTIVE_ORDERS_DIR, filename)
                try:
                    with open(filepath, 'r') as f:
                        order_data = json.load(f)
                    # Use document_number as the unique identifier and get additional info
                    doc_number = order_data.get('data', {}).get('document_number', 'Unknown')
                    title = order_data.get('data', {}).get('title', 'No Title')
                    publication_date = order_data.get('data', {}).get('publication_date', 'N/A')
                    signing_date = order_data.get('content', {}).get('signing_date', 'N/A')
                    orders.append({
                        "doc_number": doc_number,
                        "title": title,
                        "publication_date": publication_date,
                        "signing_date": signing_date,
                        "filename": filename  # can be used to fetch details
                    })
                except Exception as e:
                    logging.error("Error loading JSON from file %s: %s", filename, e)
    else:
        logging.warning("Executive orders directory does not exist: %s", EXECUTIVE_ORDERS_DIR)

    sort_by = request.args.get("sort_by")
    sort_order = request.args.get("sort_order", "asc")
    if sort_by in ("signing_date", "publication_date"):
        orders = sorted(orders, key=lambda order: order.get(sort_by, ""), reverse=(sort_order == "desc"))

    logging.info("Loaded %s executive orders from cache.", len(orders))
    return render_template("index.html", orders=orders, sort_by=sort_by, sort_order=sort_order)

@app.route('/order/<document_number>')
def order_detail(document_number):
    """
    Route to display detailed information for a specific executive order.
    Attempts to load the JSON file from cache using the document_number.
    """
    filepath = os.path.join(EXECUTIVE_ORDERS_DIR, f"{document_number}.json")
    if not os.path.exists(filepath):
        logging.error("Requested executive order %s not found in cache.", document_number)
        abort(404)
    try:
        with open(filepath, 'r') as f:
            order_data = json.load(f)
    except Exception as e:
        logging.error("Error loading executive order %s: %s", document_number, e)
        abort(500)
    logging.info("Loaded details for executive order %s", document_number)
    return render_template("order_detail.html", order=order_data)

@app.route('/order/<document_number>/summarize')
def summarize_order(document_number):
    """
    Route to summarize the original text of a specific executive order using Groq.
    If the request is AJAX (via X-Requested-With header), return a JSON response.
    Otherwise, fall back to rendering a summary page.
    """
    filepath = os.path.join(EXECUTIVE_ORDERS_DIR, f"{document_number}.json")
    if not os.path.exists(filepath):
        logging.error("Requested executive order %s not found for summarization.", document_number)
        abort(404)
    try:
        with open(filepath, 'r') as f:
            order_data = json.load(f)
    except Exception as e:
        logging.error("Error loading executive order %s: %s", document_number, e)
        abort(500)
    
    # Extract the text for summarization.
    explanation = order_data.get("content", {}).get("explanation")
    if not explanation:
        explanation = order_data.get("data", {}).get("abstract", "")
    
    # If still empty, try fetching the raw text from raw_text_url.
    if not explanation:
        raw_text_url = order_data.get("content", {}).get("raw_text_url")
        if raw_text_url:
            try:
                response = requests.get(raw_text_url)
                if response.status_code == 200:
                    explanation = response.text
                    logging.info("Fetched raw text from %s", raw_text_url)
            except Exception as e:
                logging.error("Error fetching raw text from %s: %s", raw_text_url, e)
    
    if not explanation:
        summary = "No text available for summarization."
    else:
        # First get the raw summary.
        summary_raw = summarize_text(explanation)
        # Now format the raw summary using format_summary.
        summary = format_summary(summary_raw)
    
    # Return JSON if the request is AJAX.
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return jsonify({"summary": summary})
    else:
        return render_template("summary.html", order=order_data, summary=summary)

if __name__ == '__main__':
    # Run the Flask app in debug mode for development
    app.run(debug=True)
