from zillow_search import ZillowSearch
from fill_form import FillForm

"""Objectives: Search Zillow for San Francisco rentals < $3k with 1 bedroom get:
 - price address and url
 - send to google form
 - and then to a spreadsheet
"""

zillow_data = ZillowSearch().gather_data()

fillform = FillForm()

fillform.open_data_entry_form()

fillform.add_data_from(zillow_data)
