import requests
from datetime import datetime
import json
from typing import Dict, List
import time
from urllib.parse import urlencode
import os
import logging

# Set up basic logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class FederalRegisterAPI:
    def __init__(self):
        self.base_url = "https://www.federalregister.gov/api/v1"
        self.session = requests.Session()
        # Create directory if it doesn't exist
        self.save_dir = "executive_orders"
        os.makedirs(self.save_dir, exist_ok=True)
        logging.info("Initialized FederalRegisterAPI. Save directory: %s", self.save_dir)

    def fetch_all_executive_orders(self, start_date: str = "2025-01-20") -> List[Dict]:
        """
        Fetch all executive orders that have a signing date on or after the given start_date.
        This method iterates over the paginated results until all orders are fetched.
        """
        orders = []
        page = 1
        logging.info("Starting to fetch executive orders with signing date >= %s", start_date)
        while True:
            params = {
                # Filter to presidential documents of type executive order using signing_date.
                "conditions[presidential_document_type][]": "executive_order",
                "conditions[signing_date][gte]": start_date,
                "per_page": 20,  # Adjust per_page if needed (max 1000)
                "page": page
            }
            url = f"{self.base_url}/documents.json"
            logging.info("Fetching page %s", page)
            response = self.session.get(url, params=params)
            if response.status_code != 200:
                logging.error("Error: Received status code %s for page %s", response.status_code, page)
                break

            data = response.json()
            results = data.get("results", [])
            if not results:
                logging.info("No results found on page %s; ending pagination.", page)
                break

            orders.extend(results)
            total_count = data.get("count", len(orders))
            logging.info("Fetched page %s: %s orders (Total fetched: %s of %s)", page, len(results), len(orders), total_count)
            if len(orders) >= total_count:
                logging.info("All orders fetched: %s orders total.", len(orders))
                break

            page += 1

        return orders

    def fetch_executive_order_details(self, document_number: str) -> Dict:
        """
        Fetch the full content/details of an executive order by its document number.
        """
        url = f"{self.base_url}/documents/{document_number}.json"
        logging.info("Fetching details for document %s", document_number)
        response = self.session.get(url)
        if response.status_code != 200:
            logging.error("Error fetching details for document %s: Status %s", document_number, response.status_code)
            return {}
        return response.json()

    def save_executive_order(self, eo_data: Dict) -> None:
        """
        Save a single executive order (including its full content) as a JSON file.
        The identifier is taken from 'executive_order_number' if present;
        otherwise, it falls back to 'document_number'.
        """
        eo_number = eo_data.get('executive_order_number') or eo_data.get('document_number')
        if not eo_number:
            logging.warning("No identifier found in executive order data; skipping saving.")
            return

        # Fetch the full content/details
        details = self.fetch_executive_order_details(eo_number)

        data_to_save = {
            "metadata": {
                "saved_at": datetime.now().isoformat(),
                "last_updated": datetime.now().isoformat()
            },
            "data": eo_data,
            "content": details
        }

        filename = os.path.join(self.save_dir, f"{eo_number}.json")
        with open(filename, 'w') as f:
            json.dump(data_to_save, f, indent=2)
        logging.info("Saved executive order %s to %s", eo_number, filename)

    def display_executive_orders(self, orders: List[Dict]) -> None:
        """
        Display a summary of the executive orders and save their full content.
        """
        if not orders:
            logging.info("No executive orders to display.")
            return

        logging.info("Displaying executive orders:")
        print("\nEXECUTIVE ORDERS")
        print("=" * 80)

        for eo in orders:
            self.save_executive_order(eo)
            identifier = eo.get('executive_order_number') or eo.get('document_number') or "N/A"
            title = eo.get("title", "No title")
            pub_date = eo.get("publication_date", "Unknown date")
            output = f"{identifier}: {title} (Published: {pub_date})"
            logging.info("Processed executive order: %s", output)
            print(output)
            print("-" * 80)

        logging.info("Total executive orders processed: %s", len(orders))
        print(f"\nTotal executive orders: {len(orders)}")

def main():
    fr_api = FederalRegisterAPI()
    # Fetch all executive orders with a signing date on or after January 20th, 2025.
    executive_orders = fr_api.fetch_all_executive_orders()
    # Display the orders and save each with its full content.
    fr_api.display_executive_orders(executive_orders)

if __name__ == "__main__":
    main()