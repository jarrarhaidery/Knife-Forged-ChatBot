# fetch_wp.py

import os
import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup

load_dotenv()

# WooCommerce API credentials from .env
consumer_key = os.getenv("WC_CONSUMER_KEY")
consumer_secret = os.getenv("WC_CONSUMER_SECRET")
base_url = "https://www.knifeforged.shop/wp-json/wc/v3/products"

auth = (consumer_key, consumer_secret)

def clean_html(raw_html):
    """Remove HTML tags from product description."""
    return BeautifulSoup(raw_html, "html.parser").get_text()

def fetch_all_woocommerce_products(per_page=100):
    """Handles pagination and fetches all products."""
    page = 1
    all_products = []

    while True:
        response = requests.get(base_url, auth=auth, params={"per_page": per_page, "page": page})
        if response.status_code != 200:
            raise Exception(f"Failed to fetch WooCommerce products (Page {page}): {response.status_code}")

        products = response.json()
        if not products:
            break  # No more products to fetch

        all_products.extend(products)
        page += 1

    return all_products

def format_product_data(products):
    """Format and clean product data."""
    all_text = []

    for product in products:
        title = product.get("name", "")
        description = clean_html(product.get("description", ""))
        price = product.get("price", "")
        sku = product.get("sku", "")
        category_names = ", ".join(cat["name"] for cat in product.get("categories", []))

        all_text.append(
            f"Product: {title}\nSKU: {sku}\nCategory: {category_names}\nPrice: ${price}\nDescription: {description}"
        )

    return all_text

def save_products_to_file(formatted_data, filepath="data/products.txt"):
    """Save formatted data to a text file."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n\n".join(formatted_data))
    print(f"✅ Saved {len(formatted_data)} products to {filepath}")

def fetch_wordpress_data():
    """Main entry to fetch, clean, save, and return product data."""
    products = fetch_all_woocommerce_products()
    formatted_data = format_product_data(products)
    save_products_to_file(formatted_data)
    return "\n\n".join(formatted_data)

if __name__ == "__main__":
    fetch_wordpress_data()
