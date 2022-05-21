import time
import random
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
from playsound import playsound
import urllib.parse


waiting_time_list = [i for i in range(200, 300)]

search_link = input("Welke link wilt u gebruiken om resultaten voor te zoeken?: ")

if search_link[:2] == "www":
    search_link = "http://" + search_link

# Store 50 of the latest results in a list

result_history = []

while True:
    try:
        # Obtaining the search results and storing them in a list

        page = requests.get('http://econpy.pythonanywhere.com/ex/001.html')
        html = BeautifulSoup(requests.get(search_link).content, 'html.parser')

        found_new_results = False

        # Verzamelt alle informatie over de resultaten en slaat deze gezamenlijk op in "results"

        titles = html.find_all("h3", {"class": "mp-Listing-title"})
        descriptions = html.find_all("p", {"class": "mp-Listing-description mp-text-paragraph"})
        sellers = html.find_all("span", {"class": "mp-Listing-seller-name"})
        prices = html.find_all("span", {"class": "mp-Listing-price mp-text-price-label"})
        links = html.find_all("a", {"class": "mp-Listing-coverLink"})

        # Formatteren van de links om klikbaar te zijn

        for link in range(len(links)):
            links[link] = "http://marktplaats.nl/v" + links[link].get('href')[2:]

        results = zip([i.text for i in titles], [i.text for i in descriptions],[i.text for i in sellers],
                      [i.text for i in prices], [i for i in links])

        # De verzamelde resultaten binnen deze dataverzameling

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

        # Geeft de tijd van de verzameling van resultaten weer

        now = datetime.now()

        current_time = now.strftime("%H:%M:%S")
        print("Current Time =", current_time)

        # Geeft alle nieuwe resultaten weer

        print("Nieuwe resultaten: " + str(len(new_results)) + "\n")
        for result in new_results:
            print("Titel: " + result[0] + "\n", "Beschrijving: " + result[1] + "\n", "Verkoper: " + result[2] + "\n",
                  "Prijs: " + result[3] + "\n", "Link: " + result[4] + "\n")

        # Speelt een geluid af als er nieuwe resultaten zijn
        if found_new_results:
            playsound('ding.wav')

        # Geeft aan hoe lang wordt gewacht tot de volgende dataverzameling

        waiting_time_seconds = random.choice(waiting_time_list)
        waiting_full_time = now + timedelta(seconds=waiting_time_seconds)
        print("Volgende dataverzameling: " + waiting_full_time.strftime('%H:%M:%S') + "\n")
        time.sleep(waiting_time_seconds)

    except requests.exceptions.MissingSchema:
        print("De link die u heeft ingevoerd is niet correct. Probeer het opnieuw.")
        break
