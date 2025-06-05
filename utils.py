import uuid
from esdbclient import EventStoreDBClient, NewEvent
from enum import Enum

# Connection

DefaultHost = "localhost"
DefaultPort = "2113"

def KurrentUri(host = DefaultHost, port = DefaultPort):
    return "esdb://" + host + ":" + port + "?tls=false"

def CcmClient(host = DefaultHost, port = DefaultPort):
    return EventStoreDBClient(KurrentUri(host, port))

def DeploymentStream(suffix):
    return "Deployment-" + suffix

#
# Deployment names (same as stream names)
#

class Application(Enum):
    Payroll = 1236
    Timecard = 5678

class Environment(Enum):
    DEV = 1
    UAT = 2
    PROD = 3

def DeploymentStream(app: Application, env: Environment) -> str:
    return app.name + "-" + str(app.value) + "-" + env.name

#
# Control Procedure Helpers
#

CPPrefix = "CP-"
def CPIdentifier(CPID: int) -> str:
    return CPPrefix + str(CPID)

#
# Control Objective Helpers
#

# Control Objective Event Creation
COPrefix = "CO-"
def COIdentifier(CODomain: str, COID: int) -> str:
    return COPrefix + CODomain + "-" + str(COID)

# Control Objective Event Types
COAchieved = "ControlObjectiveAchieved"
COFailed = "ControlObjectiveFailed"

def CreateCOAssessedEvent(success: bool, CODomain: str, COID: int, evidence: str) -> NewEvent:
    dataString = \
        "{\"ControlObjectiveID\":\"" + COIdentifier(CODomain, COID) + "\"," + \
        "\"Evidence\":\"" + evidence + "\"}"
    return NewEvent(
        type = COAchieved if success else COFailed,
        data = dataString.encode('utf-8'))

#
# Predicate Helpers
#

# Predicate Event Types
PredicateSucceeded = "PredicateSucceeded"
PredicateFailed = "PredicateFailed"

def PredicateIdentifier(CODomain: str, COID: int, PredicateID: int) -> str:
    return CODomain + "-" + str(COID) + "-" + str(PredicateID)

# Predicate Event Creation
def CreatePredicateAssessedEvent(success: bool, CODomain: str, COID: str, PredicateID: int, evidence: str = "\"\"") -> NewEvent:
    dataString = \
        "{\"PredicateID\":\"" + PredicateIdentifier(CODomain, COID, PredicateID) + "\"," + \
        "\"Evidence\":" + evidence + "}"
    return NewEvent(
        type = PredicateSucceeded if success else PredicateFailed,
        data = dataString.encode('utf-8'))

FailedCP = "FailedControlProcedure"

def CreatePredicateSucceededEvent(CODomain: str, COID: int, PredicateID: int) -> NewEvent:
    return CreatePredicateAssessedEvent(True, CODomain, COID, PredicateID)

def ReasonForCPFailure(CPID: int, reason: str) -> str:
    return \
        "{\"" + FailedCP + "\":\"" + CPIdentifier(CPID) + "\"," + \
        "\"Reason\":\"" + reason + "\"}"

def CreatePredicateFailedEvent(CODomain: str, COID: int, PredicateID: int, CPID: int, reason: str) -> NewEvent:
    return CreatePredicateAssessedEvent(False, CODomain, COID, PredicateID, ReasonForCPFailure(CPID, reason))