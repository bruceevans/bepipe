import os
from pprint import pprint
import bepeefour as BP4

asset = "//firinne_assets/test.blend"

assets = ["//firinne_assets/test.blend", "//firinne_assets/space_topbar.py"]

perforceFile = BP4.isFileLocal(asset) # gives both paths

"""
[{'clientFile': '//bevans-pc/test.blend',
  'depotFile': '//firinne_assets/test.blend',
  'haveRev': '2',
  'path': 'e:\\firinne\\assets\\test.blend',
  'syncTime': '1623448442'}]
"""

# get status
if perforceFile:
    # pprint(BP4.getFileStatus(perforceFile[0].get('depotFile')))
    # print(perforceFile[0].get('depotFile'))
    depotFile = perforceFile[0].get('depotFile')
else:
    print("FILE IS NOT LOCAL")


"""
for f in result:
    # f is a file

    # versions of each file
    for thing in f.revisions:
        # print(thing)
        print(thing.rev)
        print(thing.desc)
        print(thing.time)
        print(thing.action)
        print(thing.user)

        #.time
        #.user
        #.action
        #.desc
        #.rev
"""

def isLatestVersion(f, ver):
    """ Quick test to determine if local version is up to date

    Args:
        f (str): Depot path of the file
        ver (int) : Current local version

    Returns:
        bool
    """
    pass

## State Cases ##

# Local Up to Date
    # isFileLocal and isLatestVersion
# Local Out of Date
    # isFileLocal and not isLatestVersion
# Offline
    # not isFileLocal
# Checked out
    # latest version status == 'edit'

# print(isFileLocal(asset))
