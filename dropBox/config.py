'''Offline new dropBox's configuration.
'''

__author__ = 'Miguel Ojeda'
__copyright__ = 'Copyright 2012, CERN CMS'
__credits__ = ['Giacomo Govi', 'Salvatore Di Guida', 'Miguel Ojeda', 'Andreas Pfeiffer']
__license__ = 'Unknown'
__maintainer__ = 'Miguel Ojeda'
__email__ = 'mojedasa@cern.ch'


import os

import service


group = 'cms-cond-dropbox'


# For alarms
fromAddress = 'mojedasa@cern.ch'
toAddresses = ['cms-cond-dev@cern.ch']
ccAddresses = []


# For integration and production, we use the production dropBox database
if service.settings['productionLevel'] in set(['int', 'pro']):
    connectionDictionary = service.secrets['connections']['pro']

# For development, we use the prep dropBox database
elif service.settings['productionLevel'] in set(['dev']):
    connectionDictionary = service.secrets['connections']['dev']

# In private instances, we take it from netrc
elif service.settings['productionLevel'] in set(['private']):
    connectionDictionary = service.getConnectionDictionaryFromNetrc('dropBoxDatabase')

else:
    raise Exception('Unknown production level.')


# Allowed backends per production level
allowedBackends = {
    'private': set(['private']),
    'dev': set(['dev']),
    'int': set(['offline', 'online', 'tier0']),
    'pro': set(['offline', 'online', 'tier0']),
}


# Allowed services (i.e. databases) per backend
#
# None means 'same as the dropBox connectionString above', i.e. the user's
# destinationDatabase is ignored, and everything goes into the same database
# as the one used for storing the dropBox-related information (i.e. files,
# fileLog and runLog).
allowedServices = {
    'private': None,
    'dev': None,
    'offline': set(['int', 'prep']),
    'online': set(['int', 'prep', 'prod']),
    'tier0': set(['int', 'prep', 'prod']),
}


# Default dictionary for production Global Tags
productionGlobalTags = {
    'hlt': 'GR_H_V29',
    'express': 'GR_E_V31',
    'prompt': 'GR_P_V42',
}

# Base path for test files
testFilesPath = 'testFiles'

# Files for security testing, crafted by createSecurityTestFiles.py, treated
# specially by test.py and used by copyOnlineTestFiles()
securityTestFilesPath = os.path.join(testFilesPath, 'security')

