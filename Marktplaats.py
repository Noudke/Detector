import urllib.request
import time
import random
import numpy as np
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from playsound import playsound


waiting_time_list = [i for i in range(200, 300)]

search_link = input("Welke link wilt u gebruiken om resultaten voor te zoeken?: ")

# Store 50 of the latest results in a list

result_history = []

while True:
    # Obtaining the search results and storing them in a list

    page = requests.get('http://econpy.pythonanywhere.com/ex/001.html')
    html = BeautifulSoup(requests.get(search_link).content, 'html.parser')

    found_new_results = False

    titles = html.find_all("h3", {"class": "mp-Listing-title"})
    descriptions = html.find_all("p", {"class": "mp-Listing-description mp-text-paragraph"})
    sellers = html.find_all("span", {"class": "mp-Listing-seller-name"})
    prices = html.find_all("span", {"class": "mp-Listing-price mp-text-price-label"})

    results = zip([i.text for i in titles], [i.text for i in descriptions],[i.text for i in sellers],
                  [i.text for i in prices])

    current_results = [result for result in set(results)]
    new_results = []

    for result in current_results:
        if result not in result_history:
            result_history.insert(0, result)
            new_results.append(result)
            if len(result_history) >= 50:
                result_history.pop()

    if len(new_results) > 0:
        found_new_results = True

    now = datetime.now()

    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)

    print("New results: ")
    for result in new_results:
        print("Titel: " + result[0] + "\n", "Beschrijving: " + result[1] + "\n", "Verkoper: " + result[2] + "\n",
              "Prijs: " + result[3] + "\n")

    # Play a sound when new results are found
    if found_new_results:
        playsound('ding.wav')

    time.sleep(random.choice(waiting_time_list))
