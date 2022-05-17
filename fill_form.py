import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSdXvhrvVZ0-nBnYvSJdkrzCoCLJsNut-IO5xn-bDlm_5drWiA/viewform?usp" \
           "=sf_link "

chrome_driver_path = "/Users/william/Developer/Python/chromedriver"


class FillForm:
    def __init__(self):
        self.s = Service(chrome_driver_path)
        self.browser = webdriver.Chrome(service=self.s)
        # self.browser = webdriver.Firefox()
        self.wait = WebDriverWait(self.browser, 30)

    def open_data_entry_form(self):
        """
        Open the form url
        :return: no return
        """
        self.browser.get(FORM_URL)
        time.sleep(3)

    def add_data_to_form(self, rental_list):
        """
        Open form and enter data
        :param rental_list: property data collected
        :return: no return
        """
        for i in range(len(rental_list)):
            rental_price = rental_list[i][0]
            rental_address = rental_list[i][1]
            rental_link = rental_list[i][2]

            # address_field = self.browser.find_element(By.XPATH, "/html/body/div/div[2]/form/div[2]/div/div[2]/div["
            #                                                     "1]/div/div/div[2]/div/div[1]/div/div[1]/input")
            address_field = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div/div[2]/form/div[2]/div/div[2]/div["
                                                      "1]/div/div/div[2]/div/div[1]/div/div[1]/input")))
            address_field.click()
            address_field.send_keys(rental_address)

            # Tab to price field
            address_field.send_keys(Keys.TAB)
            price_field = self.browser.find_element(By.XPATH, "/html/body/div/div[2]/form/div[2]/div/div[2]/div["
                                                              "2]/div/div/div[2]/div/div[1]/div/div[1]/input")
            price_field.send_keys(rental_price)

            # Tab to link field
            price_field.send_keys(Keys.TAB)
            link_field = self.browser.find_element(By.XPATH, "/html/body/div/div[2]/form/div[2]/div/div[2]/div["
                                                             "3]/div/div/div[2]/div/div[1]/div/div[1]/input")
            link_field.send_keys(rental_link)

            # Submit entry
            link_field.send_keys(Keys.TAB, Keys.ENTER)

            if i < (len(rental_list) - 1):
                add_another_entry = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[2]/div[1]/div/div[4]/a")))
                # add_another_entry = self.browser.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[1]/div/div[
                # 4]/a")
                add_another_entry.click()

            time.sleep(3)
