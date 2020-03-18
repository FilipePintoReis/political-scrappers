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
import EUPParsing
import DatabaseConnection
import Log


# External functions
####################

# Main script
#############
try:
    #IMPORTANT
    #using week 30 because it has data, when testing is finished, delete the 2019-30 from the url 
    response = requests.get('http://www.europarl.europa.eu/news/en/agenda/weekly-agenda', timeout = (30, 30)) # timeout is in seconds, first is connecting, second is reading
    response.raise_for_status()
    if response.status_code == 200: 
        soup = BeautifulSoup(response.content, 'html.parser')
        out_going_to_database = []

        EUPParsing.parse_nodes(soup, out_going_to_database)

        DatabaseConnection.send_calendar_items(out_going_to_database, "EUP")

except Exception as err:
    print(f'Error occurred: {err}')
    DatabaseConnection.send_parsing_error('http://www.europarl.europa.eu/news/en/agenda/weekly-agenda', DatabaseConnection.entity_dictionary["EUP"], err)
    Log.log("EUP", err, True)