import requests
from bs4 import BeautifulSoup

def find_lowest_price(product_name):
    url = f"https://www.crewai.com/search?q={product_name}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    prices = soup.find_all('span', class_='price')
    
    if prices:
        lowest_price = min(prices, key=lambda x: float(x.text.strip().replace(',', '')))
        return lowest_price.text.strip()
    else:
        return "No prices found for the product."

product_name = input("Enter the product name: ")
lowest_price = find_lowest_price(product_name)
print(f"The lowest price for {product_name} is {lowest_price}")