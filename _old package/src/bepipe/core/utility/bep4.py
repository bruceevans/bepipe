
import os
from P4 import P4, P4Exception

def checkOut(files):
    """ checkout workspace files
    """
    # changelist stuff TODO

def createNewChangelist(p4, description):
    p4.input = description
    p4.run("changelist", "-i")
    # return changelist?

def createP4Instance(port = None, user = None, client = None):
    p4 = P4()

    if port:
        p4.port = port 
    if user:
        p4.user = user
    if client:
        p4.client = client

    p4.connect()
    return p4

def submitChangelist(p4, files, description):
    """ submit changelist for files
    """

    change = p4.fetch_change()
    change._description = description
    change._files = files
    p4.run_submit(change)

def sync(p4, file):
    p4.run("sync", file)
