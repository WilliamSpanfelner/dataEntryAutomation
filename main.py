from bs4 import BeautifulSoup
import requests

# Search Zillow for San Francisco rentals < $3k with 1 bedroom get:
# - price address and url
# - send to google form
# and then to a spreadsheet

FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSdXvhrvVZ0-nBnYvSJdkrzCoCLJsNut-IO5xn-bDlm_5drWiA/viewform?usp" \
           "=sf_link "
ZILLOW_URL = "https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C" \
             "%22mapBounds%22%3A%7B%22west%22%3A-122.67022170019531%2C%22east%22%3A-122.19643629980469%2C%22south%22" \
             "%3A37.68079477398145%2C%22north%22%3A37.869667504276016%7D%2C%22mapZoom%22%3A11%2C%22isMapVisible%22" \
             "%3Atrue%2C%22filterState%22%3A%7B%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1" \
             "%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22auc%22%3A%7B" \
             "%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C" \
             "%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22fsba%22%3A%7B" \
             "%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%7D"

# Read Zillow content
response = requests.get(ZILLOW_URL)
zillow_page = response.text

# Make soup
soup = BeautifulSoup(zillow_page, "html.parser")
print(soup)

properties = soup.find_all(name="a", id="top")
print("properties: ", properties)
