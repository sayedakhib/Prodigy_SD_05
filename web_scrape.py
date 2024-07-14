import requests
from bs4 import BeautifulSoup
import csv

# Function to get the HTML content of a page
def get_html(url):
    response = requests.get(url)
    return response.text

# Function to extract product information from a single page
def extract_product_info(html):
    soup = BeautifulSoup(html, 'html.parser')
    products = []

    for product in soup.select('article.product_pod'):
        name = product.h3.a['title']
        price = product.select_one('p.price_color').text
        availability = product.select_one('p.instock.availability').text.strip()
        products.append((name, price, availability))

    return products

# Function to scrape multiple pages
def scrape_books(base_url, num_pages):
    all_products = []
    for page in range(1, num_pages + 1):
        url = f"{base_url}/catalogue/page-{page}.html"
        html = get_html(url)
        products = extract_product_info(html)
        all_products.extend(products)
    return all_products

# Function to save product information to a CSV file
def save_to_csv(products, filename):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Price", "Availability"])
        writer.writerows(products)

# Main script
base_url = "http://books.toscrape.com"
num_pages = 5  # Number of pages to scrape
products = scrape_books(base_url, num_pages)
save_to_csv(products, 'products.csv')
print(f"Scraped {len(products)} products and saved to products.csv")