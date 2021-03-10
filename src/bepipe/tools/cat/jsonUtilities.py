# JSON interaction here

import os
import json
import pprint as pp

def readJsonFile(jsonFile):
    """ Open a json file and return all data

        args:
            jsonFile (str): Path to json file

        returns:
            dict
    """

    with open(jsonFile, 'r') as readFile:
        data=json.load(readFile)
    return data

def writeJson(fileName, data):
    """General write to json file helper

        args:
            data (dict): Dict elements to write
            fileName (str): Name of the json file

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
    