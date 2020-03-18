from datetime import datetime


from bs4 import BeautifulSoup
from requests.exceptions import HTTPError
import requests

import CalendarItem
import DatabaseConnection

def parse_date(node):
    day = node.find(class_="event-d").contents[0]

    month = node.find(class_="event-f").contents[0]

    if month.find("Janeiro") >= 0 or month.find("janeiro") >= 0:
        month = "01"
    elif month.find("Fevereiro") >= 0 or month.find("fevereiro") >= 0:
        month = "02"
    elif month.find("Março") >= 0 or month.find("março") >= 0:
        month = "03"
    elif month.find("Abril") >= 0 or month.find("abril") >= 0:
        month = "04"
    elif month.find("Maio") >= 0 or month.find("maio") >= 0:
        month = "05"
    elif month.find("Junho") >= 0 or month.find("junho") >= 0:
        month = "06"
    elif month.find("Julho") >= 0 or month.find("julho") >= 0:
        month = "07"
    elif month.find("Agosto") >= 0 or month.find("agosto") >= 0:
        month = "08"
    elif month.find("Setembro") >= 0 or month.find("setembro") >= 0:
        month = "09"
    elif month.find("Outubro") >= 0 or month.find("outubro") >= 0:
        month = "10"
    elif month.find("Novembro") >= 0 or month.find("novembro") >= 0:
        month = "11"
    elif month.find("Dezembro") >= 0 or month.find("dezembro") >= 0:
        month = "12"

    year = None
    if int(datetime.today().month) > int(month):
        year = datetime.today().year + 1
    else:
        year = datetime.today().year

    return str(day) + "-" + str(month) + "-" + str(year) 

def parse_node(node):
    item = CalendarItem.CalendarItem()

    date = parse_date(node)
    title = node.find(class_="mec-color-hover").contents[0]
    
    dictionary = inside_nodes_page(node)

    item.title = title
    item.start_date = date
    if "Place" in dictionary:
        item.place = dictionary["Place"]
    if "Hour" in dictionary:
        item.hour = dictionary["Hour"]

    return item



def inside_nodes_page(node):
    dictionary_to_return = {}
    try:
        response = requests.get(node.find(class_="mec-color-hover")["href"], timeout = (30, 30)) 
        response.raise_for_status()
        if response.status_code == 200: 
            soup = BeautifulSoup(response.content, 'html.parser')

            if len(soup.find_all(class_ = "mec-single-event-time")) > 0:
                dictionary_to_return["Hour"] = soup.find(class_ = "mec-single-event-time").find(class_ = "mec-events-abbr").contents[0]
            if len(soup.find_all(class_ = "mec-single-event-location")) > 0:
                place = ""
                if len(soup.find_all(class_ = "author fn org")) > 0:
                    place += soup.find(class_ = "author fn org").contents[0]
                if len(soup.find_all(class_ = "mec-address")) > 0:
                    if(place != ""): place += ", "
                    if(len(soup.find(class_ = "mec-address").contents) > 0):
                        place += soup.find(class_ = "mec-address").contents[0]
                dictionary_to_return["Place"] = place

    except Exception as err:
        print(f'Error occurred: {err}')
        DatabaseConnection.send_parsing_error('https://www.psd.pt/atualidade-agenda/', DatabaseConnection.entity_dictionary["PSD"], err)
        
    return dictionary_to_return