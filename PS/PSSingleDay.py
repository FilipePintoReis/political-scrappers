# It’s a good idea to order imports
# alphabetically within each import group,
# as this makes finding particular imports much easier,
# especially when there are many imports in a file.


# Standard library imports
##########################
from time import sleep
from enum import Enum

# Third party imports
#####################
from bs4 import BeautifulSoup
from requests.exceptions import HTTPError
import requests

# Local application imports
###########################
import CalendarItem
import PSParsing
import DatabaseConnection
import Log

# External functions
####################
def do_day(url):
    try:
        response = requests.get(url, timeout = (30,30)) # timeout is in seconds, first is connecting, second is reading
        response.raise_for_status()
        if response.status_code == 200: 
            soup = BeautifulSoup(response.content, 'html.parser')
            # Check if day has no calendar items
            for it in soup.find_all(class_ = "tribe-events-notices"):
                if(it.find("ul").find("li").contents[0] == 'Não há eventos agendados para '):
                    print("Day has no items")
                    return None

            day_string = soup.find(id="tribe-bar-date")["value"]

            out_going_to_database = []

            for it in soup.find_all(class_ = "type-tribe_events"):
                    item_to_append = PSParsing.parse_event(it,day_string)
                    out_going_to_database.append(item_to_append)

            DatabaseConnection.send_calendar_items(out_going_to_database, "PS")

    except Exception as err:
        print(f'Error occurred: {err}')
        DatabaseConnection.send_parsing_error(url, DatabaseConnection.entity_dictionary["PS"], err)
        Log.log("PS", err, True)