'''Offline new dropBox's configuration.
'''

__author__ = 'Miguel Ojeda'
__copyright__ = 'Copyright 2012, CERN CMS'
__credits__ = ['Giacomo Govi', 'Salvatore Di Guida', 'Miguel Ojeda', 'Andreas Pfeiffer']
__license__ = 'Unknown'
__maintainer__ = 'Miguel Ojeda'
__email__ = 'mojedasa@cern.ch'


import os


group = 'cms-cond-dropbox'

# Note: At the moment, all the paths should be in the same filesystem.
# FIXME: Put the paths in /data/files/service/... (and create the paths
#        automatically in deploy.py, if we do not use AFS or Oracle for
#        the production version.

# Base path for stored files
filesPath = 'files'

# Files just uploaded to the dropbox that are being checked
uploadedFilesPath = os.path.join(filesPath, 'uploaded')

# Files just extracted that are being checked
extractedFilesPath = os.path.join(filesPath, 'extracted')

# Files pending to be pulled from online
pendingFilesPath = os.path.join(filesPath, 'pending')

# Files that were acknowledged by online, kept for reference for some time
acknowledgedFilesPath = os.path.join(filesPath, 'acknowledged')

# Files that were malformed, kept for reference for some time
badFilesPath = os.path.join(filesPath, 'bad')


# Base path for test files
testFilesPath = 'testFiles'

# Files for offline testing, used by test.py
offlineTestFilesPath = os.path.join(testFilesPath, 'offline')

# Files for online testing, used by copyOnlineTestFiles()
onlineTestFilesPath = os.path.join(testFilesPath, 'online')

