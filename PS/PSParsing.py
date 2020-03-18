import CalendarItem

def parse_event(node, date):
    item = CalendarItem.CalendarItem()
    item.title = node.find(class_= "url")["title"]
    
    day = date[8:]
    month = date[5:7]
    year = date[:4]
    item.start_date = day + "-" + month + "-" + year

    meta = node.find(class_ = "tribe-events-event-meta")
    start_hour_str = meta.find(class_ = "tribe-event-date-start").contents[0]
    
    if start_hour_str.find("@") > 0:
        start_hour = start_hour_str[start_hour_str.find("@") + 1:].strip()
        item.hour = start_hour
    
    end_hour = meta.find(class_ = "tribe-event-time")

    if (end_hour is not None): end_hour = end_hour.contents[0] ; item.hour = item.hour + "-" + end_hour
    
    place = None
    if(meta.find(class_ = "tribe-events-venue-details") is not None): place = meta.find(class_ = "tribe-events-venue-details").contents[0].strip() + " "
    
    if(meta.find(class_ = "tribe-street-address") is not None): place += meta.find(class_ = "tribe-street-address").contents[0].strip() + " "
    
    if(meta.find(class_ = "tribe-locality") is not None): place += meta.find(class_ = "tribe-locality").contents[0].strip() 
    else: place = place[:len(place) - 1] + ", "

    if(meta.find(class_ = "tribe-delimiter") is not None): place += meta.find(class_ = "tribe-delimiter").contents[0].strip() + " "
    if(meta.find(class_ = "tribe-country-name") is not None): place += meta.find(class_ = "tribe-country-name").contents[0].strip()

    item.place = place
    
    return item