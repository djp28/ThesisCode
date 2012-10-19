'''dropBox backend's test suite.
'''

__author__ = 'Miguel Ojeda'
__copyright__ = 'Copyright 2012, CERN CMS'
__credits__ = ['Giacomo Govi', 'Salvatore Di Guida', 'Miguel Ojeda', 'Andreas Pfeiffer']
__license__ = 'Unknown'
__maintainer__ = 'Miguel Ojeda'
__email__ = 'mojedasa@cern.ch'


import sys
import os
import subprocess
import logging
import glob
import socket
import netrc
import time
import cStringIO
import uu
import gzip

import http
import tier0
import service

import config
import Dropbox
import Constants
import databaseLog


frontendHost = socket.gethostname()
frontendBaseUrl = 'https://%s/dropBox/' % frontendHost


class DropBoxBETest(service.TestCase):

    def upload(self, folder, loggingPrefix = ''):

        tests = [ x.partition( '.txt' )[ 0 ] for x in glob.glob( os.path.join( 'testFiles', folder, '*.txt' ) ) ]

        logging.info( '%s Uploading %s files...', loggingPrefix, len( tests ) )

        i = 0
        for test in tests :
            i += 1
            logging.info( '%s   [%s/%s] %s: Uploading...', loggingPrefix, i, len( tests ), os.path.basename( test ) )
            # Use upload.py
            process = subprocess.Popen( '../dropBox/upload.py -H %s %s' % (frontendHost, test),
                                        shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE )
            result = process.communicate( )
            error = result[ 1 ].rsplit( '\n', 1 )[ -2 ].partition( 'ERROR: ' )[ 2 ]

            if len( error ) > 0 :
                raise Exception('%s Upload failed: %s (full msg: %s)' % (loggingPrefix, error, result))


    def testRun(self):
        tstConfig = config.test()

        # override baseUrl to use private VM
        tstConfig.baseUrl = frontendBaseUrl

        (username, account, password) = netrc.netrc().authenticators('newOffDb')
        frontendHttp = http.HTTP()
        frontendHttp.setBaseUrl(frontendBaseUrl)

        folders = os.listdir( 'testFiles' )

        logging.info('Testing %s bunches...', len(folders))

        i = 0
        for folder in folders:
            i += 1

            loggingPrefix = '  [%s/%s] %s:' % (i, len(folders), folder)
            logging.info('%s Testing bunch...', loggingPrefix)

            logging.info( '%s Signing in the frontend...', loggingPrefix)
            frontendHttp.query('signIn', {
                'username': username,
                'password': password,
            })

            # First ask also to hold the files until we have uploaded all
            # the folder to prevent the backend from taking them in-between.
            logging.info( '%s Asking the frontend to hold files...', loggingPrefix)
            frontendHttp.query('holdFiles')

            # Wait until the dropBox has nothing to do
            logging.info( '%s Waiting for backend to be idle...', loggingPrefix)
            while databaseLog.getLatestRunLogStatusCode() != Constants.NOTHING_TO_DO:
                time.sleep(2)

            # When we reach this point, the server will always report an empty
            # list of files, so even if it starts a new run right now, we can
            # safely manipulate the list of files. Therefore, ask the frontend
            # to do a clean up to delete previous files and database entries
            logging.info( '%s Asking the frontend to clean up files and database...', loggingPrefix)
            frontendHttp.query('cleanUp')

            # Upload all the test files in the folder
            logging.info('%s Uploading files...', loggingPrefix)
            self.upload(folder, loggingPrefix = loggingPrefix)

            # And finally release the files so that the backend can take them
            logging.info( '%s Asking the frontend to release files...', loggingPrefix)
            frontendHttp.query('releaseFiles')

            logging.info( '%s Signing out the frontend...', loggingPrefix)
            frontendHttp.query('signOut')

            # The backend will process the files eventually, so wait for
            # a finished status code
            logging.info('%s Waiting for backend to process files...', loggingPrefix)
            while True:
                statusCode = databaseLog.getLatestRunLogStatusCode()

                if statusCode in frozenset([Constants.DONE_WITH_ERRORS, Constants.DONE_ALL_OK]):
                    break

                time.sleep(2)

            # First compare the runLog's statusCode
            logging.info('%s Comparing runLog results...', loggingPrefix)
            with open(os.path.join('testFiles', folder, 'statusCode'), 'rb') as f:
                self.assertEqual(statusCode, getattr(Constants, f.read().strip()))

            # Then compare the runLog's logs
            (creationTimestamp, downloadLog, globalLog) = databaseLog.getLatestRunLogInfo()

            def unpackLog(log):

                # Decode uu
                uuFile = cStringIO.StringIO()
                uuFile.write(log)
                uuFile.seek(0)
                gzFile = cStringIO.StringIO()
                uu.decode(uuFile, gzFile)

                # Decode gzip
                gzFile.seek(0)
                f = gzip.GzipFile(fileobj = gzFile)
                log = f.read()
                f.close()

                return log

            downloadLog = unpackLog(downloadLog)
            globalLog = unpackLog(globalLog)

            logging.debug('downloadLog = %s', downloadLog)
            logging.debug('globalLog = %s', globalLog)

            #-mos TODO: Think how to take out timestamps, use file paths, etc.
            #           Probably the best solution is to match each line vs a regexp

            with open(os.path.join('testFiles', folder, 'downloadLog'), 'rb') as f:
                pass #self.assertEqual(downloadLog, f.read().strip())
            
            with open(os.path.join('testFiles', folder, 'globalLog'), 'rb') as f:
                pass #self.assertEqual(globalLog, f.read().strip())

            tests = [x.partition('.txt')[0] for x in glob.glob(os.path.join('testFiles', folder, '*.txt'))]

            logging.info('%s Comparing %s fileLogs results...', loggingPrefix, len(tests))

            # Then for each file in the test, compare the fileLog's foreign key, statusCode and log
            j = 0
            for test in tests:
                j += 1

                logging.info('%s   [%s/%s] %s: Comparing file...', loggingPrefix, j, len(tests), os.path.basename(test))

                # Get the expected file hash
                with open('%s.fileHash' % test, 'rb') as f:
                    fileHash = f.read().strip()

                (fileStatusCode, fileLog, runLogCreationTimestamp) = databaseLog.getFileLogInfo(fileHash)

                # Compare the foreign key
                self.assertEqual(creationTimestamp, runLogCreationTimestamp)

                # Compare the statusCode
                with open('%s.statusCode' % test, 'rb') as f:
                    self.assertEqual(fileStatusCode, getattr(Constants, f.read().strip()))

                fileLog = unpackLog(fileLog)

                # Compare the fileLog
                with open('%s.fileLog' % test, 'rb') as f:
                    pass #self.assertEqual(fileLog, f.read().strip())


def main():
    sys.exit(service.test(DropBoxBETest))


if __name__ == "__main__":
    main()

