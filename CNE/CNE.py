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
import CNEParsing
import DatabaseConnection
import Log


# External functions
####################

# Main script
#############
try:
    response = requests.get('http://www.cne.pt/content/calendario', timeout = (30, 30)) # timeout is in seconds, first is connecting, second is reading
    response.raise_for_status()
    if response.status_code == 200: 
        soup = BeautifulSoup(response.content, 'html.parser')
        out_going_to_database = []    
        for it in range(1, len(soup.find(class_="default").tbody.contents)):
            node = soup.find(class_="default").tbody.contents[it]
            temp = CNEParsing.return_calendar_item(node)
            if temp != "ABORT": out_going_to_database.append(temp)

        DatabaseConnection.send_calendar_items(out_going_to_database, "CNE")

except Exception as err:
    print(f'Error occurred: {err}')
    DatabaseConnection.send_parsing_error('http://www.cne.pt/content/calendario', DatabaseConnection.entity_dictionary["CNE"], err)
    Log.log("CNE", err, True)