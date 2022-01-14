
import os
from functools import wraps
from P4 import P4, P4Exception


_P4_INSTANCE = None


# 0 No exceptions, 1 Errors as exceptions, 2 Warnings as exceptions
EXCEPTION_LEVEL = 1


DEFAULT_DESCRIPTION = "Automated changelist"


def getP4Instance(refresh=False):
    """Grab the global p4 instance with an option force refresh

    Using a global allows for context managers and decorators

    Args:
        refresh (bool, optional): Force return a new instance or not

    Returns:
        P4 Instance

    """

    global _P4_INSTANCE
    if refresh or not _P4_INSTANCE:
        _P4_INSTANCE = P4()
    if not _P4_INSTANCE:
        raise P4Exception("Can't find a valid P4 Instance")
    return _P4_INSTANCE


# connect context manager
class P4Connect(object):
    """ Context manager to handle connect/disconnect to P4 instanct

    Enusres a connection on enter, disconnects on exit

    Args:
        p4instance (P4 Instance)
    """

    def __init__(self, p4instance, exception_level=EXCEPTION_LEVEL):
        if not p4instance or not hasattr(p4instance, 'connect'):
            raise TypeError("Invalid P4 instance or is missing a 'connect' attr")
        self._p4instance = p4instance
        self._exception_level = exception_level

    def __enter__(self):
        if not self._p4instance.connected():
            self._p4instance.exception_level = self._exception_level
            try:
                self._p4instance.connect()
            except P4Exception:
                if self._p4instance:
                    for e in self._p4instance.errors:
                        print(e)

    def __exit__(self, excType, excValue, traceback):
        self._p4instance.disconnect()


# Decorator to wrap a command in a try/except and connect
def peefourcommand(func):
    """ Decorator to handle executing a function within a try/except
    """
    @wraps(func)
    def _wrapper(*args, **kwargs):
        out = None
        _p4 = getP4Instance()
        with P4Connect(_p4):
            try:
                out = func(*args, **kwargs)
            except P4Exception:
                for e in _p4.errors:
                    print(e)
                out = None
        return out
    return _wrapper


# TODO give the appropriate user based on current prefs

@peefourcommand
def addNewFiles(files):
    p4 = getP4Instance()
    # TODO create and submit changelist at the same time?
    for f in files:
        p4.run("add", f)

@peefourcommand
def submit(description):
    p4 = getP4Instance()
    change = p4.run_change( "-o" )[0]
    change[ "Description" ] = description
    p4.input = change
    p4.run_submit( "-i" )

@peefourcommand
def checkOutFiles(files, version=None):
    """ Create a changelist and edit the given files

    Args:
        files ([str]): List of file paths
        version (int): Specify a version to revise
    """
    p4 = getP4Instance()
    
    for f in files:
        if not version:
            p4.run("sync", f)
        # else get the selected version and checkout TODO
        p4.run("edit", f)

@peefourcommand
def checkInFiles(files, description):
    """ Check in new/updated files

    Args:
        files ([str]): List of files
        description (str): Changelog description
    """

    p4 = getP4Instance()
    changeList = p4.fetch_change()
    changeList._description = description
    changeList._files = files
    p4.run_submit(changeList)

@peefourcommand
def getLatestRevision(asset):
    """ Get the latest of the selected file and elements
    """
    p4 = getP4Instance()
    results = p4.run("sync", asset)
    return results

@peefourcommand
def getVersionHistory(perforceFile):
    """ Return the version history of the selected file

    Args:
        perforceFile (str): Depot file path
    
    Returns:
        Dict
    """
    p4 = getP4Instance()
    return(p4.run_filelog(perforceFile))

@peefourcommand
def getFileStatus(files):
    """ Get the status of the given files

    Args:
        files ([str]): List of files

    Returns:
        ([str])
    """
    p4 = getP4Instance()
    results = []
    """
    for f in files:
        results.append(p4.run_status(f))
    """
    # results = p4.run_filelog(files)
    results = p4.run_status(files)
    return results

@peefourcommand
def isFileLocal(f):
    """ Is the file in the local workspace

    Args:
        f (str): Depot file path

    Returns:
        [dict]
    """
    p4 = getP4Instance()
    result = p4.run_have(f)
    return result

@peefourcommand
def getConnectionInfo():
    p4 = getP4Instance()
    info = p4.run("info")
    return info


