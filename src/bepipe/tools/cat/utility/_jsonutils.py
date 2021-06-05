# JSON interaction here

import os
import json
import pprint as pp

def bepToJson(bepFile):
    """ Replace the file extension
    """
    directory = os.path.dirname(bepFile)
    fileName = os.path.basename(bepFile)
    extension = os.path.splitext(bepFile)[1]
    fileName = fileName.replace(extension, ".json")
    jsonFile = os.path.join(directory, fileName)
    os.rename(bepFile, jsonFile)

def readJsonFile(jsonFile):
    """ Open a json file and return all data

        args:
            jsonFile (str): path to json file

        returns:
            dict
    """

    with open(jsonFile, 'r') as readFile:
        data=json.load(readFile)
    return data

def jsonToBep(jsonFile):
    """ Rename the file to .bep

        args:
            jsonFile: path to jason file
    """
    directory = os.path.dirname(jsonFile)
    fileName = os.path.basename(jsonFile)
    extension = os.path.splitext(jsonFile)[1]
    fileName = fileName.replace(extension, ".bep")
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
        except Exception as e:
            print(e)
            print("Unable to write the JSON file")
            return False
        print("Successfully wrote {}".format(fileName))
        return True

def writeToExistingJson(jsonFile, newData):
    """ Write data to an existing json file

        args:
            jsonFile (str): path to json file
            newData (dict): new json entry

        returns:
            bool
    """

    with open(jsonFile) as readFile:
        data=json.load(readFile)
        data.append(newData)
        return writeJson(data, jsonFile)
