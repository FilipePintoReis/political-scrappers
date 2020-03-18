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

def parse_node(date_node, body_node):
    item = CalendarItem.CalendarItem()

    item.start_date = date_node.find(class_="date-display-single").decode_contents()
    item.start_date = format_date(item.start_date)
    
    item.title = body_node.find(class_="agenda-home").find('a').decode_contents().strip()
    #Funciona para a maioria dos casos, no entanto, às vezes, alteram o local e a hora de sitio.
    #parse_time_and_place(item, body_node.find(class_="field-content").contents[1])
    
    return item


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

    if int(datetime.datetime.now().month) > int(month):
        year += 1

    return str(day) + "-" + str(month) + "-" + str(year) 



def parse_time_and_place(item_to_ret, node):
    while node.contents.count('.') != 1: node.contents.pop(0)
    
    for br in node.find_all('br'):
        br.decompose()

    nodeIndex = 0
    if(len(node.find_all('strong')) > 0):
        nodeIndex = node.contents.index(node.find_all('strong')[0])
    
    if(len(node.find_all('strong')) == 2):
        item_to_ret.hour = node.find_all('strong')[1].decode_contents()
    
    if(len(node.find_all('strong')) > 0):
        item_to_ret.place = node.find_all('strong')[0].decode_contents()

    while nodeIndex != 0:
        nodeIndex += -1
        node.contents.pop(0)

    if(len(node.find_all('strong')) > 0):
        if node.contents[1] == ', ': 
            item_to_ret.place += ', ' + node.contents[2].decode_contents()
        else:
            item_to_ret.place += node.contents[1]

    if item_to_ret.place is not None:
        item_to_ret.place = item_to_ret.place.strip()

    if item_to_ret.hour is not None:
        item_to_ret.hour = item_to_ret.hour.strip()

    if item_to_ret.place is not None and item_to_ret.place[len(item_to_ret.place) - 1] == ",":
        item_to_ret.place = item_to_ret.place[0:len(item_to_ret.place) - 1]

    return item_to_ret

