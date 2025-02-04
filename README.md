# Trump Tracker

## Overview

Trump Tracker is a Python-based web application for retrieving, storing, and analyzing executive orders from the Federal Register. The project uses Flask for web interface, provides a systemized approach to executive order data management, and leverages the Groq API for text summarization.

## Technical Components

### Project Structure
- `dashboard.py`: Flask web server for displaying executive orders
- `fetch_eos.py`: Script for retrieving executive orders from Federal Register
- `summarizer.py`: Utility for generating text summaries

### Technical Requirements
- Python 3.8+
- Dependencies listed in `requirements.txt`
- Groq API key for text summarization

## Installation

### Dependencies
```bash
uv pip install --requirements requirements.txt
# or
pip install -r requirements.txt
```

### Configuration
Create `.env` file:
```bash
GROQ_API_KEY=your_api_key
```

## Usage Scripts

### Dashboard
```bash
python dashboard.py
```
Starts web interface at `http://127.0.0.1:5000`

### Fetch Executive Orders
```bash
python fetch_eos.py
```
Retrieves and stores executive order data

## Technical Features
- Federal Register data retrieval
- JSON-based data storage
- Flask web interface
- API-powered text summarization
- Sortable executive order listing

## Development
- Contributions via pull requests
- Follow existing code style
- Open issues for questions/suggestions

## License
MIT License

## Technical Dependencies
- Flask
- Requests library
- Groq API client
- Python 3.8+

## Notes
Designed for programmatic access and analysis of executive order documentation.