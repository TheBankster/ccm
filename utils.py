import uuid
from esdbclient import EventStoreDBClient, NewEvent
from enum import Enum

# Connection

DefaultHost = "localhost"
DefaultPort = "2113"

def KurrentUri(host = DefaultHost, port = DefaultPort):
    return "esdb://" + host + ":" + port + "?tls=false"

def Client(host = DefaultHost, port = DefaultPort):
    return EventStoreDBClient(KurrentUri(host, port))

def DeploymentStream(suffix):
    return "Deployment-" + suffix

#
# Deployment names (same as stream names)
#

class Application(Enum):
    Payroll = 1234
    Timecard = 5678

class Environment(Enum):
    DEV = 1
    UAT = 2
    PROD = 3

def DeploymentStream(app: Application, env: Environment) -> str:
    return app.name + "-" + str(app.value) + "-" + env.name

#
# Event Types
#

# Control Objective Event Types
COPrefix = "CO-"
COAchieved = "ControlObjectiveAchieved"
COFailed = "ControlObjectiveFailed"

# Control Objective Event Creation
def COIdentifier(CODomain: str, COID: int) -> str:
    return COPrefix + CODomain + "-" + str(COID)

def CreateCOAssessedEvent(success: bool, CODomain: str, COID: int, evidence: str) -> NewEvent:
    dataString = \
        "{\"id\":\"" + COIdentifier(CODomain, COID) + "\"," + \
        "\"evidence\":\"" + evidence + "\"" + \
        "}"
    return NewEvent(
        type = COAchieved if success else COFailed,
        data = dataString.encode('utf-8')
    )

# Predicate Event Types
PredicateSucceeded = "PredicateSucceeded"
PredicateFailed = "PredicateFailed"

def PredicateIdentifier(CODomain: str, COID: int, PredicateID: int) -> str:
    return CODomain + "-" + str(COID) + "-" + str(PredicateID)

# Predict Event Creation
def CreatePredicateAssessedEvent(success: bool, CODomain: str, COID: str, PredicateID: int) -> NewEvent:
    dataString = \
        "{\"id\":\"" + PredicateIdentifier(CODomain, COID, PredicateID) + "\"" + \
        "}"
    return NewEvent(
        type = PredicateSucceeded if success else PredicateFailed,
        data = dataString.encode('utf-8')
    )