"""Wrapper around P4 for easier use and error tracking
"""

import os
import getpass
from functools import wraps

from P4 import P4, P4Exception

import bepipe.core.path as path


class BP4(object):
    def __init__(self, client=None, port=None, user=None):
        """P4 wrapper class to manage common actions and the active connection

        Args:
            client (str): Local client
            port (str): Server port
            user (str): User
        """
        self._p4 = self._connectP4(client, port, user)
    
    def _connectP4(self, client=None, port=None, user=None):
        """Debug connection for testing purposes
        
        Args:
            client (str): P4 client
            port (str): Server port
            user (str): User

        """
        return P4(client=client, port=port, user=user)

    # TODO not working yet...
    def BP4Connect(func):
        """class level decorator to manage connection

        Args:
            func (function): Function to run once P4 connects

        Returns:
            wrapper function
        """

        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            with self._p4.connect():
                print("ATTEMPTING TO CONNECT")
                try:
                    func(*args, **kwargs)
                except P4Exception as e:
                    print(e)
        return wrapper
        """

    @property
    def client(self):
        """Get the actice client
        """
        return self._p4.client

    def getClients(self, user=None):
        """Get a list of client dicts for all or a specific user
        
        Args:
            user (str): P4 user name
        
        Returns:
            ([client descriptions])

        """
        with self._p4.connect():
            if user:
                return [cl for cl in self._p4.run_clients() if cl.get("Owner") == user]
            return list(self._p4.run_clients())

    def hasRevisions(self, depotPath):
        """Checks if the given file has revisions aka out of date
        
        Args:
            depotPath (str): Path to server depot file

        Returns:
            (bool)

        """
        with self._p4.connect():
            revisions = None
            try:
                # TODO double check this
                revisions = self._p4.run_files(depotPath)
            except P4Exception as e:
                print(e)
                return False
            return True if revisions else False

    def getRevisions(self, depotPath):
        """Get a list of revisions of the given depot file
        
        Args:
            depotPath (str): Path to the depot file

        Returns:
            ([P4.Revision]): Revisions, newest first [0]
        """

        with self._p4.connect():
            try:
                result = self._p4.run_filelog(depotPath)
            except P4Exception:
                return []

            revisions = []
            for f in result:
                for revision in f.revisions:
                    revisions.append(revision)
            return revisions

    def createChangelist(self, description=None):
        """Create a new changelist with an option description
        
        Args:
            description (str): Changelist description

        Returns:
            (int): Changelist ID
        """

        with self._p4.connect():
            changelist = self._p4.save_change({
                "Change": "new",
                "Description": str(description) or ""
            })
            return int(changelist[0].split()[1])

    def addFileToChangelist(self, localPath, changelist=None):
        """Add a local file to the specified changelist
        
        Args:
            localPath (str): Path to a file in the client's root
            changelist (int): Changelist ID or None, 
                            if None the default changelist will be used
            
        Returns:
            (dict): Dictionary with 
        """
        with self._p4.connect():
            if not changelist:
                changelist = "default"
            try:
                # TODO may need to make the path a unix path
                result = self._p4.run_add("-c", changelist, os.path.normpath(localPath))
            except P4Exception as e:
                raise ValueError(e.value)
            return result[0]

    # TODO rename function? or implement a 'checkout' in CAT API/elsewhere?
    def editFile(self, depotPath, changelist=None):
        """Exclusive checkout of a depot file
        
        Args:
            depotPath (str): Path to depot file
            changelist (int): Changelist ID

        Returns:
            (dict): Dictionary containing: action, clientFile, type, depotFile, workRev
        
        Raises:
            ValueError: P4Exception on invalid changelist or path

        """
        with self._p4.connect():
            if not changelist:
                changelist = "default"
            try:
                # TODO unix path?
                result = self._p4.run_edit("-c", changelist, os.path.normpath(depotPath))
            except P4Exception as e:
                raise ValueError(e.value)
            return result[0]

    def isOpened(self, localPath):
        """Determines if a local file is opened in a changelist alread
        aka: another user is working on it.

        Args:
            localPath (str): Path to asset under local client root

        Returns:
            (bool)
        """

    def sync(self, depotPath):
        """Sync an existing server file to the local root
        
        Args:
            depotPath (str): Path to the file in the Perforce depot

        Returns:
            (bool): Success or fail

        Raises:
            ValueError: If the file is not under the clien'ts root
        """
        with self._p4.connect():
            try:
                self._p4.run_sync(path.toLinuxPath(os.path.normpath(depotPath)))
            except P4Exception as e:
                if "files(s) up-to-date" in e.value:
                    return True
                elif "not under client's root" in e.value:
                    raise ValueError(e.value)
                return False
            return True

    # TODO set client function when needed
