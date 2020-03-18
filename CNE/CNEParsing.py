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

    year = datetime.datetime.now().year
    if date.find("de 20") > 0:
        year = date[date.find("de 20") + 3: date.find("de 20") + 7]
    
    return str(day) + "-" + str(month) + "-" + str(year) 

def return_calendar_item(node):
    to_ret = CalendarItem.CalendarItem()
    year = node.contents[0].contents[1].contents[0]
    date = node.contents[2].contents[0].strip()
    if(not date[0].isdigit()): return "ABORT"
    date += "de " + year
    date = format_date(date)

    title = node.contents[6].contents[0].strip()

    to_ret.start_date = date
    to_ret.title = title
    return to_ret