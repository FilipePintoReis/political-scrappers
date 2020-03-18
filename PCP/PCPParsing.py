# Standard library imports
##########################
import datetime
import copy

# Third party imports
#####################

# Local application imports
###########################
import CalendarItem


# External functions
####################

def format_date(date):

    date = date.strip()
    day = date[0:2]
    day = day.strip()

    month = "error"

    if date.find("Janeiro") >= 0 or date.find("janeiro") >= 0 or date.find("Jan") >= 0 or date.find("jan") >= 0:
        month = "01"
    elif date.find("Fevereiro") >= 0 or date.find("fevereiro") >= 0 or date.find("Fev") >= 0 or date.find("fev") >= 0:
        month = "02"
    elif date.find("Março") >= 0 or date.find("março") >= 0 or date.find("Mar") >= 0 or date.find("mar") >= 0:
        month = "03"
    elif date.find("Abril") >= 0 or date.find("abril") >= 0 or date.find("Abr") >= 0 or date.find("abr") >= 0:
        month = "04"
    elif date.find("Maio") >= 0 or date.find("maio") >= 0 or date.find("Mai") >= 0 or date.find("mai") >= 0:
        month = "05"
    elif date.find("Junho") >= 0 or date.find("junho") >= 0 or date.find("Jun") >= 0 or date.find("jun") >= 0:
        month = "06"
    elif date.find("Julho") >= 0 or date.find("julho") >= 0 or date.find("Jul") >= 0 or date.find("jul") >= 0:
        month = "07"
    elif date.find("Agosto") >= 0 or date.find("agosto") >= 0 or date.find("Ago") >= 0 or date.find("ago") >= 0:
        month = "08"
    elif date.find("Setembro") >= 0 or date.find("setembro") >= 0 or date.find("Set") >= 0 or date.find("set") >= 0:
        month = "09"
    elif date.find("Outubro") >= 0 or date.find("outubro") >= 0 or date.find("Out") >= 0 or date.find("out") >= 0:
        month = "10"
    elif date.find("Novembro") >= 0 or date.find("novembro") >= 0 or date.find("Nov") >= 0 or date.find("nov") >= 0:
        month = "11"
    elif date.find("Dezembro") >= 0 or date.find("dezembro") >= 0 or date.find("Dez") >= 0 or date.find("dez") >= 0:
        month = "12"

    try: 
        if month == "error":
            raise Exception("Error parsing month, an error should be inserted into database")
    except Exception as err:
        print(f'Error occurred: {err}')

    year = date[len(date) - 4 : len(date)]

    return str(day) + "-" + str(month) + "-" + str(year) 

def parse_node(node):
    item = CalendarItem.CalendarItem()
    item.title = node.find(class_="corpo").find('a').decode_contents()
    item.place = node.find(class_="local-hora").contents[0].strip()
    item.start_date = node.find(class_="date-display-single").decode_contents().strip()
    item.hour = node.find(class_='local-hora').find(class_="date-display-single").decode_contents().strip()
    
    if item.place[len(item.place) - 1] == ',': item.place = item.place[:len(item.place) - 1] ; item.place.strip() 
    if len(item.place) == 0: item.place = None
    item.start_date = format_date(item.start_date)
    
    return item