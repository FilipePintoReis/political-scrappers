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
def parse_node(node):
    item = CalendarItem.CalendarItem()
    parse_hour(node, item)
    parse_name(node, item)
    parse_place(node, item)
    parse_date(node, item)
    return item

def parse_hour(node, item):
    node = node.find(class_='ep_title')
    item.hour = node.time.decode_contents()

def parse_name(node, item):
    node = node.find_all(class_='ep_title')[1]
    item.title = node.find_all(class_='ep_name')[1].decode_contents()

def parse_place(node, item):
    node = node.find(class_='ep_subtitle')
    item.place = node.find(class_='ep_name').decode_contents()
def parse_date(node, item):
    upper_node = node.parent.parent.parent.parent.parent.parent.parent
    raw_data = upper_node.find(class_="ep-layout_header").time.decode_contents()
    item.start_date = raw_data[len(raw_data) - 10:]


def parse_nodes(soup, out_going_to_database):
    nodes = []
    temp = soup.find_all(class_='ep-layout_event_committee-meetings')
    for t in temp:
        temp2 = t.find('ol').find_all('li', recursive=False)
        for t2 in temp2:
            nodes.append(t2)
            
    for node in nodes:
        out_going_to_database.append(parse_node(node))
