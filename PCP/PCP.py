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
import PCPParsing
import DatabaseConnection
import Log


# External functions
####################

# Main script
#############
try:
    response = requests.get('http://www.pcp.pt/agenda', timeout = (30, 30)) # timeout is in seconds, first is connecting, second is reading
    response.raise_for_status()
    if response.status_code == 200: 
        soup = BeautifulSoup(response.content, 'html.parser')
        out_going_to_database = []

        nodes = soup.find_all(class_="views-row")
        for node in nodes:
            out_going_to_database.append(PCPParsing.parse_node(node))

        DatabaseConnection.send_calendar_items(out_going_to_database, "PCP")

except Exception as err:
    print(f'Error occurred: {err}')
    DatabaseConnection.send_parsing_error('http://www.pcp.pt/agenda', DatabaseConnection.entity_dictionary["PCP"], err)
    Log.log("PCP", err, True)