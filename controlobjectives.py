#
# Control Objective Helpers
#

from enum import Enum
from esdbclient import NewEvent

ControlObjectveDomainNames = ["CCV", "RP"]

class ControlObjectiveDomain(Enum):
    ConfidentialComputingVerifier = 1
    ReverseProxy = 2

def ControlObjectiveDomainName(domain: ControlObjectiveDomain) -> str:
    return ControlObjectveDomainNames[domain.value - 1]

# Control Objective Event Creation

# e.g. CO-CCV-1
def ControlObjectiveIdentifier(domain: ControlObjectiveDomain, id: int) -> str:
    ControlObjectivePrefix = "CO-"
    return ControlObjectivePrefix + ControlObjectiveDomainName(domain) + "-" + str(id)

# Control Objective Event Types
ControlObjectiveAchieved = "ControlObjectiveAchieved"
ControlObjectiveFailed = "ControlObjectiveFailed"

def CreateObjectiveAssessedEvent(success: bool, domain: ControlObjectiveDomain, id: int, evidence: str) -> NewEvent:
    dataString = \
        "{\"ControlObjectiveID\":\"" + ControlObjectiveIdentifier(domain, id) + "\"," + \
        "\"Evidence\":\"" + evidence + "\"}"
    return NewEvent(
        type = ControlObjectiveAchieved if success else ControlObjectiveFailed,
        data = dataString.encode('utf-8'))
        