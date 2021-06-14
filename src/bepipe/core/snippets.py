import os
from pprint import pprint
import bepeefour as BP4

asset = "//firinne_assets/test.blend"

assets = ["//firinne_assets/test.blend", "//firinne_assets/space_topbar.py"]


print(BP4.getConnectionInfo())

"""
[{'clientFile': '//bevans-pc/test.blend',
  'depotFile': '//firinne_assets/test.blend',
  'haveRev': '2',
  'path': 'e:\\firinne\\assets\\test.blend',
  'syncTime': '1623448442'}]
"""

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
