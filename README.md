# Trump Tracker

**Track executive orders and get professional summaries at a glance.**

---

## Project Overview

**Trump Tracker** is a web-based dashboard that allows you to view, analyze, and summarize executive orders fetched from the Federal Register. Using the Groq API, the project provides concise, professional summaries of executive orders while also displaying detailed metadata and agency information. Whether you're tracking changes in policy or analyzing decision-making trends, Trump Tracker keeps you informed with organized data and powerful search and sorting capabilities.

---

## Features

- **Dashboard View:** Browse all cached executive orders with sortable columns by signing or publication date.
- **Detailed Order View:** View an executive order's full metadata, including title, document number, publication date, signing date, and agency information.
- **Summarization:** Automatically generate professional summaries for executive orders using the Groq API.
- **Data Fetching:** Retrieve and save executive order data from the Federal Register with a dedicated script.
- **Modular Organization:** Separate scripts for fetching (`fetch_eos.py`), summarizing (`summarizer.py`), and displaying (`dashboard.py`) executive orders.
- **Screenshots:** Visual aids (to be added later) for both dashboard and order detail views are included under the `screenshots` folder.

---

## Installation & Setup

### Prerequisites

- **Python:** Python 3.8 or higher is required.
- **Package Manager:** Use `uv` for dependency installation.
- **Dependencies:** All required dependencies are listed in the [`requirements.txt`](requirements.txt) file.
- **Environment Variables:** Configure your Groq API key (see below).

### Cloning the Repository

```bash
git clone https://github.com/ghsaboias/trump-tracker.git
cd trump-tracker
```

### Installing Dependencies

If you're using `uv`, install the required packages with:

```bash
uv pip install --requirements requirements.txt
```

Alternatively, if you prefer using `pip`, you can install the dependencies with:

```bash
pip install -r requirements.txt
```

---

## Configuration

Create a `.env` file in the project root with the following content:

```bash
GROQ_API_KEY=your_groq_api_key_here
```

This file should contain the Groq API key necessary for fetching summaries via the Groq API.

---

## Usage

Trump Tracker is organized into several key scripts. Below are detailed instructions for each:

### 1. Dashboard (`dashboard.py`)

**Description:**  
Runs a Flask web server that serves the dashboard interface. Users can view all cached executive orders, sort them, and click to see detailed information and summaries.

**How to Run:**

```bash
python dashboard.py
```

**Details:**

- **Home Page:** Lists all executive orders with sorting links for signing and publication dates.
- **Order Detail:** Clicking on an order shows detailed metadata, agency information, and options to view the full text or download the PDF.
- **Summarization:** The dashboard includes a "Summarize Text" button that triggers an AJAX call to generate and display a professional summary using the Groq API.

---

### 2. Fetch Executive Orders (`fetch_eos.py`)

**Description:**  
Fetches executive orders from the Federal Register and saves their full details as JSON files within the `executive_orders` directory.

**How to Run:**

```bash
python fetch_eos.py
```

**Details:**

- Fetches orders with a signing date on or after a specified start date.
- Saves each order's basic data and full content (including metadata and additional details) into the `executive_orders` folder.
- Logs progress and handles pagination automatically.

---

### 3. Summarizer (`summarizer.py`)

**Description:**  
Contains helper functions to generate a concise summary of the executive order text using the Groq API.

**Details:**

- **`summarize_text(text: str) -> str`:**  
  Accepts raw text, cleans it (removing content between `<think>` tags), and uses the Groq API to produce a professional summary.
  
- **`format_summary(summary: str) -> str`:**  
  Formats the generated summary (for example, converting markdown-like bold text to HTML `<strong>` tags) for improved readability.

---

## Screenshots

*(Images will be added later in the `screenshots` folder.)*

- **Dashboard View:** `screenshots/dashboard.png`
- **Order Detail View:** `screenshots/order_detail.png`

---

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Commit your changes following the project's code style.
4. Submit a pull request for review.

If you have any questions or suggestions, please open an issue in the repository.

---

## License

This project is licensed under the [MIT License](LICENSE).

---

## Example Usage

After setting up your environment and installing dependencies, simply start the application:

1. Run the dashboard with:
   
   ```bash
   python dashboard.py
   ```
   
   Then navigate to `http://127.0.0.1:5000` in your browser to interact with the executive orders interface.

2. To update the data, run the fetch script:

   ```bash
   python fetch_eos.py
   ```

Happy tracking!
