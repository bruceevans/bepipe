# JSON interaction here

import os
import json

from bepipe.core import bepeefour as BP4


def catToJson(catFile):
    """ Replace the file extension
    """
    directory = os.path.dirname(bepFile)
    fileName = os.path.basename(bepFile)
    extension = os.path.splitext(bepFile)[1]
    fileName = fileName.replace(extension, ".json")
    jsonFile = os.path.join(directory, fileName)
    os.rename(catFile, jsonFile)

def readJsonFile(jsonFile):
    """ Open a json file and return all data

        args:
            jsonFile (str): path to json file

        returns:
            dict
    """
    # BP4.checkOutFiles([jsonFile])
    with open(jsonFile, 'r') as readFile:
        data=json.load(readFile)
    return data

def jsonToCat(jsonFile):
    """ Rename the file to .cat

        args:
            jsonFile: path to jason file
    """
    directory = os.path.dirname(jsonFile)
    fileName = os.path.basename(jsonFile)
    extension = os.path.splitext(jsonFile)[1]
    fileName = fileName.replace(extension, ".cat")
    bepFile = os.path.join(directory, fileName)
    os.rename(jsonFile, bepFile)

def writeJson(fileName, data):
    """General write to json file helper

        args:
            fileName (str): Name of the json file
            data (dict): Dict elements to write

        returns;
            bool
    """

    with open(fileName, 'w') as f:
        try:
            json.dump(data, f, indent=4)
        except OSError as e:
            print(e)
            print("Unable to write the JSON file")
            return False
        return True

def writeToExistingJson(jsonFile, newData):
    """ Write data to an existing json file

        args:
            jsonFile (str): path to json file
            newData (dict): new json entry

        returns:
            bool
    """
    BP4.checkOutFiles([jsonFile])
    with open(jsonFile) as readFile:
        data=json.load(readFile)
        data.append(newData)
        return writeJson(data, jsonFile)
