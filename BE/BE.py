# It’s a good idea to order imports
# alphabetically within each import group,
# as this makes finding particular imports much easier,
# especially when there are many imports in a file.


# Standard library imports
##########################
from enum import Enum
from time import sleep

# Third party imports
#####################
from bs4 import BeautifulSoup
from requests.exceptions import HTTPError
import requests

# Local application imports
###########################
import BEParsing
import DatabaseConnection
import Log


# External functions
####################

# Main script
#############
try:
    response = requests.get('https://www.esquerda.net/events', timeout = (30, 30)) # timeout is in seconds, first is connecting, second is reading
    response.raise_for_status()
    if response.status_code == 200: 
        soup = BeautifulSoup(response.content, 'html.parser')
        soup = soup.find(class_="view-agenda")
        #remove newlines from contents
        soup.contents[:] = (value for value in soup.contents if value != '\n')
        soup.contents.pop(0) #remove date filter

        out_going_to_database = []

        #for i in range(0, len(soup.contents), 2):
        #    out_going_to_database.append(BEParsing.parse_node(soup.contents[i], soup.contents[i + 1]))
        current_date_node = None
        soup.find(class_='item-list').decompose()
        for i in range(0, len(soup.contents)):
            if soup.contents[i].name == 'h3':
                current_date_node = soup.contents[i]
            elif soup.contents[i].name == 'div':
                out_going_to_database.append(BEParsing.parse_node(current_date_node, soup.contents[i]))
            
        DatabaseConnection.send_calendar_items(out_going_to_database, "BE")

except Exception as err:
    print(f'Error occurred: {err}')
    Log.log('BE', err, True)

    DatabaseConnection.send_parsing_error('https://www.esquerda.net/events', DatabaseConnection.entity_dictionary["BE"], err)