import requests
from bs4 import BeautifulSoup
import json

# Base URL of the website
base_url = 'https://books.toscrape.com/'

# Fetch the main page content
page = requests.get(base_url)
soup = BeautifulSoup(page.content, 'html.parser')

# Find the <ul> element with the class 'nav nav-list'
categories_list = soup.find('ul', class_='nav nav-list')

# Find all <li> elements within this <ul> (skipping the first one which is just a parent "Books")
categories = categories_list.find_all('li')[1:]

# Categories to scrape
categories_to_scrape = ['Travel', 'Mystery', 'Historical Fiction']

# List to store the result
result = []

# Extract category URLs directly for specified categories
category_urls = {}

for category in categories:
    category_name = category.find('a').text.strip()
    if category_name in categories_to_scrape:
        relative_url = category.find('a')['href']
        category_url = base_url + relative_url
        category_urls[category_name] = category_url

# Function to fetch book details from a category page (only the first page)
def get_books_from_category(category_url):
    books = []
    response = requests.get(category_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find all book elements on the page
    book_list = soup.find_all('article', class_='product_pod')
    
    for book in book_list:
        title = book.find('h3').find('a')['title']
        rating = book.find('p', class_='star-rating')['class'][1]  # Extracts the second class name for the rating
        price = book.find('p', class_='price_color').text
        availability = book.find('p', class_='availability').text.strip()
        
        books.append({
            "title": title,
            "rating": rating,
            "price": price,
            "availability": availability
        })
    
    return books

# Loop through each specified category and scrape the data
for category_name, category_url in category_urls.items():
    print(f"Scraping category: {category_name}")
    books = get_books_from_category(category_url)
    
    result.append({
        "data": books,
        "type": category_name
    })

# Save the result as a JSON file
with open('books.json', 'w') as f:
    json.dump(result, f, indent=4)

print("Data has been scraped and saved to books.json")
