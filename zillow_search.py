from bs4 import BeautifulSoup
import requests

ROOT_URL = 'https://www.zillow.com'
ZILLOW_URL = "https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C" \
             "%22mapBounds%22%3A%7B%22west%22%3A-122.67022170019531%2C%22east%22%3A-122.19643629980469%2C%22south%22" \
             "%3A37.68079477398145%2C%22north%22%3A37.869667504276016%7D%2C%22mapZoom%22%3A11%2C%22isMapVisible%22" \
             "%3Atrue%2C%22filterState%22%3A%7B%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1" \
             "%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22auc%22%3A%7B" \
             "%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C" \
             "%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22fsba%22%3A%7B" \
             "%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%7D"
""" Add headers to circumvent captcha throws as per Max Bade (Scraping Zillow with Python and BeautifulSoup)[
https://blog.devgenius.io/scraping-zillow-with-python-and-beautifulsoup-bbc7e581c218]
"""
headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.8',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
}

class ZillowSearch:
    def __init__(self):
        with requests.Session() as session:
            response = session.get(ZILLOW_URL, headers=headers)
        zillow_page = response.text

        self.soup = BeautifulSoup(zillow_page, "html.parser")
        self.cards = self.soup.select("ul > li > article > div.list-card-info")
        self.properties = []
        self.rent = ''
        self.address = ''
        self.url = ''

    def extract_rent_from(self, bs4_rent):
        """
        Returns a string representing the monthly rent clear of
        extraneous text
        :param bs4_rent: the BeautifulSoup object containing the rent;
        :return: monthly rent as string
        """
        self.rent = ''
        price: str = bs4_rent[0].get_text()
        if "/" in price:
            price = price.split('/')[0]
        elif "+" in price:
            price = price.split('+')[0]
        return price

    def extract_address_from(self, bs4_address, rent):
        """
        Returns a clean address string

        :param bs4_address: a BeautifulSoup object containing the address;
        :param rent: a string representing the rent;
        :return: an address string.
        """
        self.address = ''
        address = bs4_address[0].get_text()
        if rent in address:
            # print(f"adrress must be split: {address.split(rent)}")
            address = address.split(rent + ', ')[1]
        return address

    def extract_url_from(self, bs4_url):
        """
        Returns a url as a string from a BeautifulSoup object
        :param bs4_url: a BeautifulSoup object containing the url;
        :return: a url as a string.
        """
        self.url = ''
        url = bs4_url[0].get('href')
        if url[:2] == "/b":
            url = ROOT_URL + url
        return url

    def gather_data(self):
        """
        Extract and format data to a list
        :return: a list of prices, addresses and property links.
        """
        for card in self.cards:
            bs4_rent = card.select("div.list-card-price")
            bs4_address = card.select("address")
            bs4_url = card.select("a.list-card-link")

            if bs4_rent:
                self.rent = self.extract_rent_from(bs4_rent)

            if bs4_address:
                self.address = self.extract_address_from(bs4_address, self.rent)

            if bs4_url:
                self.url = self.extract_url_from(bs4_url)

            if self.rent and self.address and self.url:
                self.properties.append((self.rent, self.address, self.url))
        self.properties.pop()

        return self.properties