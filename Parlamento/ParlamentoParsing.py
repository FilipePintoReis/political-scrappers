# Standard library imports
##########################
import datetime
import copy

# Third party imports
#####################

# Local application imports
###########################


# External functions
####################

def format_date(date):
    if date.find("Dia") != -1:
        date = date[date.find("Dia") + 4:]
    if date.find("DIA") != -1:
        date = date[date.find("DIA") + 4:]
        

    date = date.strip()
    day = date[0:date.find(" ")]
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

def ensure_colon(subtitle): # This function exists to ensure consistency, since some times the data to be scraped is missing the colon after the field
    for x in range(0, len(subtitle)):
        if subtitle[x].isupper() and subtitle[x + 1] == " ":
            subtitle = subtitle[:x + 1] + ":" + subtitle[x + 1:]
    if subtitle.find("Dia") >= 0:
        subtitle = subtitle[0:subtitle.find("Dia") + 3] + ":" + subtitle[subtitle.find("Dia") + 3:]

    return subtitle

def subtitle_parsing(subtitle):
    subtitle = ensure_colon(subtitle)

    day_index = subtitle.find("DIA")
    hour_index = subtitle.find("HORA")
    place_index = subtitle.find("LOCAL")
    type_index = subtitle.find("TIPO")

    try:
        if day_index < 0:
            raise Exception("Day is mandatory, an error should be inserted into database")
    except Exception as err:
        print(f'Error occurred: {err}')

    # extracting day field
    next = subtitle.find("|", day_index)
    # following structure is getting the substring from start to end indexes: string[start:end]
    day = subtitle[day_index + len("DIA: "): (len(subtitle), next)[next > 0]]  # ternary operator is deciding the end index (if_test_is_false, if_test_is_true)[test]
    day = day.strip()
    day = format_date(day)
    subtitleDictionary = { "day": day }

    # extracting hour field
    next = subtitle.find("|", hour_index)
    if hour_index > 0:
        hour = subtitle[hour_index + len("HORA: "): (len(subtitle), next)[next > 0]]
        hour = hour.strip()
        subtitleDictionary["hour"] = hour

    # extracting place field
    next = subtitle.find("|", place_index)
    if place_index > 0:
        place = subtitle[place_index + len("LOCAL: "): (len(subtitle), next)[next > 0]]
        place = place.strip()
        subtitleDictionary["place"] = place

    # extracting type field
    next = subtitle.find("|", type_index)
    if type_index > 0: 
        typee = subtitle[type_index + len("TIPO: "): (len(subtitle), next)[next > 0]] # I used typee variable because type is a keyword in python
        typee = typee.strip()
        subtitleDictionary["type"] = typee

    return subtitleDictionary

def return_calendar_items(temporary_item, decoded_contents):
    contents_array = decoded_contents.split("<br/>")
    items_to_be_returned = []
    for content in contents_array:
        content = content.strip()
        if(content == ""): return items_to_be_returned
            
        content = parse_conteudo_texto(content)
        new_item = copy.deepcopy(temporary_item)
        new_item.hour = content["Hour"]
        new_item.title = new_item.title + ", " + content["Title"]
        items_to_be_returned.append(new_item)
    return items_to_be_returned

def parse_conteudo_texto(content):
    dic = {"Hour": content[:content.find(" ")].strip()}
    dic["Title"] = content[content.find("-") + 1:].strip()
    return dic


def get_title_and_subtitle(node):
    title = node.find(class_="ConteudoTitulo").decode_contents()
    subtitle = node.find(class_="ConteudoSubtitulo").decode_contents()
    title = title.strip()  # strip trailing and following whitespaces
    subtitle = subtitle.strip()
    return { "title": title, "subtitle": subtitle }


def calendar_item_add_fields(calendar_item, dictionary, title):
    calendar_item.start_date = dictionary["day"]
    calendar_item.place = "Assembleia da República"
    finalTitle = title
    if "hour" in dictionary:
        calendar_item.hour = dictionary["hour"]
    if "place" in dictionary: # Adicionar em vez de substituir
        calendar_item.place = calendar_item.place + ", " + dictionary["place"]
    if "type" in dictionary:
        finalTitle += ", " + dictionary["type"]
    calendar_item.title = finalTitle