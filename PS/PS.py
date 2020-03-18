# It’s a good idea to order imports
# alphabetically within each import group,
# as this makes finding particular imports much easier,
# especially when there are many imports in a file.


# Standard library imports
##########################
from enum import Enum
from datetime import date
import datetime

# Third party imports
#####################

# Local application imports
###########################
import PSSingleDay

# Main script
#############
NUMBER_OF_DAYS_AHEAD = 30
today = date.today()
today = today - datetime.timedelta(days=5)

d1 = today.strftime("%Y-%m-%d")

dates = [d1]

for it in range(1,NUMBER_OF_DAYS_AHEAD):
    dates.append((today + datetime.timedelta(days=it)).strftime("%Y-%m-%d"))

for it in dates:
    url = "https://ps.pt/index.php/events/"
    url += it + "/"
    print(url)
    PSSingleDay.do_day(url)