#--- Constants for online and offline dropbox ---

TIMETYPE_MAP = {'runnumber' : 0,
                'timestamp' : 1,
                'lumiid' : 2,
                'hash' : 3,
                'userid' : 4}

DEFAULT_GT_VALUES = {'hlt' : 'GR_H_V29',
                     'express' : 'GR_E_V25',
                     'prompt' : 'GR_P_V32'}

# --- File processing status ---------------------

# convention: offset + step*100 + { base: 01, fail: 10, warning: 11, OK; 00 }

# overall:
WAITING_FOR_START = 100
STARTING      = 1000
NOTHING_TO_DO = 1999
DOWNLOADING   = 2000
EXTRACTING    = 3000
PROCESSING    = 4000
DONE_WITH_ERRORS  = 9910
DONE_ALL_OK       = 9999

# file-related:
# downloading : offset = 2000
DOWNLOADING_FAILURE = 2010
CHECKSUM_FAILURE    = 2110
UNTARING_ILLCONT    = 2210
UNTARING_FAILURE    = 2220
DOWNLOADING_OK      = 2999

# extracting metadata and sorting :  offset = 3000
EXTRACT_FAILED = 3010
EXTRACT_OK     = 3999

# processing : offset = 4000
FILECHECK_FAILED   = 4110
EXPORTING          = 4201
EXPORTING_FAILURE  = 4210
EXPORTING_OK       = 4299
DUPLICATING        = 4301
EXPORTING_OK_BUT_DUPLICATION_FAILURE = 4310
PCL_EXPORTING_OK_BUT_DUPLICATION_TO_HLTEXPRESS_FAILURE = 4311
DUPLICATING_OK     = 4399
INVALID_FCSR_FROM_TIER0 = 4410
UNREACHABLE_FCSR_FROM_TIER0 = 4510
PROCESSING_FAILURE = 4910
PROCESSING_OK      = 4999

# For scripts that need to show a human-string of the value
inverseMapping = {}
for name in dict(vars()):
    if not name.startswith('_') and isinstance(vars()[name], int):
        inverseMapping[vars()[name]] = name

# ------------------------------------------------
