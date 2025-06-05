from enum import Enum

#
# Deployment names (same as stream names)
#

class Env(Enum):
    DEV = 1
    UAT = 2
    PROD = 3
