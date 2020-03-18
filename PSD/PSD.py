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

# Local application imports
###########################
import CalendarItem
import PSDParsing
import DatabaseConnection
import PSDJSHandling
import Log


# External functions
####################

# Main script
#############
try:
    soup = BeautifulSoup(PSDJSHandling.ret_html(), 'html.parser')
    out_going_to_database = []
    
    nodes = soup.find_all(class_="mec-event-article mec-clear")
    
    for node in nodes:
        out_going_to_database.append(PSDParsing.parse_node(node))

    DatabaseConnection.send_calendar_items(out_going_to_database, "PSD")

except Exception as err:
    print(f'Error occurred: {err}')
    Log.log("PSD", err, True)
    DatabaseConnection.send_parsing_error('https://www.psd.pt/atualidade-agenda/', DatabaseConnection.entity_dictionary["PSD"], err)
    