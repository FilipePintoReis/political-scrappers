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
import ParlamentoParsing
import DatabaseConnection
import Log


# External functions
####################
class States(Enum):
    Normal = 1
    Skipping = 2
    Special = 3 # State for grupos parlamentares
    Dead = 4

# Main script
#############
try:
    response = requests.get('http://app.parlamento.pt/BI2/', timeout = (30, 30)) # timeout is in seconds, first is connecting, second is reading
    response.raise_for_status()
    if response.status_code == 200: 
        soup = BeautifulSoup(response.content, 'html.parser')
        nodes = soup.find_all(class_="TabTitulBolInf2")

        state_machine_var = States.Normal # used to know in which section we are in i.e. Plenário - Agendamentos Futuros, Comissões Parlamentares...
        temporary_item = None # will be used in the seventh section
        out_going_to_database = []

        for i in range(0, len(nodes)):
            if nodes[i].has_attr('summary'):  # skipping title and updating section
                if nodes[i].find(class_ = "Seccao").contents[0].strip() == "Resumo da Calendarização":
                    state_machine_var = States.Skipping
                elif nodes[i].find(class_ = "Seccao").contents[0].strip() == "Grupos Parlamentares":
                    state_machine_var = States.Special
                elif state_machine_var == States.Special or state_machine_var == States.Dead:
                    state_machine_var = States.Dead
                else: state_machine_var = States.Normal

            if len(nodes[i].find_all(class_="ConteudoTitulo"))  == 0: # skipping nodes that don't contain a title
                if state_machine_var != States.Special:
                    continue

            if state_machine_var == States.Normal:

                item = CalendarItem.CalendarItem()
                titleAndSubtitle = ParlamentoParsing.get_title_and_subtitle(nodes[i])
                subtitleDictionary = ParlamentoParsing.subtitle_parsing(titleAndSubtitle["subtitle"]) 
                ParlamentoParsing.calendar_item_add_fields(item, subtitleDictionary, titleAndSubtitle["title"])
                out_going_to_database.append(item)
                
            elif state_machine_var == States.Skipping: # this element is a summary of other elements
                continue

            elif state_machine_var == States.Special: #
                if len(nodes[i].find_all(class_="ConteudoTitulo"))  != 0:
                    temporary_item = CalendarItem.CalendarItem()
                    temporary_item.title = nodes[i].find(class_="ConteudoTitulo").decode_contents().strip()
                    subtitle = nodes[i].find(class_="ConteudoSubtitulo").decode_contents().strip()
                    date = ParlamentoParsing.ensure_colon(subtitle)
                    date = ParlamentoParsing.format_date(date)
                    temporary_item.start_date = date
                elif len(nodes[i].find_all(class_="ConteudoTexto"))  != 0:
                    decoded_contents = nodes[i].find(class_="ConteudoTexto").span.decode_contents()
                    calendar_items = ParlamentoParsing.return_calendar_items(temporary_item, decoded_contents)
                    for item in calendar_items:
                        out_going_to_database.append(item)
                
        DatabaseConnection.send_calendar_items(out_going_to_database, "Assembleia da Republica")

except Exception as err:
    print(f'Error occurred: {err}')
    DatabaseConnection.send_parsing_error('http://app.parlamento.pt/BI2/', DatabaseConnection.entity_dictionary["Assembleia da Republica"], err)
    Log.log("Parlamento", err, True)