import os
import datetime

def log(entity, error, inDB):
    f = open(entity + ".txt", "a")

    message = 'Entity: ' + entity
    message += '\nError: ' + str(error)
    message += '\nDatetime: ' + str(datetime.datetime.now()) + '\n\n'

    f.write(message)

    f.close