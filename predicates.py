import array as arr
from esdbclient import NewEvent
from enum import Enum
from controlprocedures import ControlProcedureIdentifier
from controlobjectives import ControlObjectiveDomain
from eventtypes import PredicateSucceeded, PredicateFailed
from controlobjectives import VerifierControlObjectives, ReverseProxyControlObjectives

#
# Predicate Helpers
#

def PredicateIdentifier(CODomain: str, COID: int, PredicateID: int) -> str:
    return CODomain + "-" + str(COID) + "-" + str(PredicateID)

# Predicate Event Creation
def CreatePredicateAssessedEvent(success: bool, domain: ControlObjectiveDomain, coId: str, predicateId: int, evidence) -> NewEvent:
    dataString = \
        "{\"PredicateID\":\"" + PredicateIdentifier(domain, coId, predicateId) + "\"," + \
        "\"Evidence\":" + evidence + "}"
    return NewEvent(
        type = PredicateSucceeded if success else PredicateFailed,
        data = dataString.encode('utf-8'))

FailedControlProcedure = "FailedControlProcedure"

def CreatePredicateSucceededEvent(domain: ControlObjectiveDomain, coId: int, predicateId: int, reason: str = "") -> NewEvent:
    return CreatePredicateAssessedEvent(True, domain, coId, predicateId)

def ReasonForControlProcedureFailure(cpId: int, reason: str) -> str:
    return \
        "{\"" + FailedControlProcedure + "\":\"" + ControlProcedureIdentifier(cpId) + "\"," + \
        "\"Reason\":\"" + reason + "\"}"

def CreatePredicateFailedEvent(coDomain: ControlObjectiveDomain, coId: int, predicateId: int, cpId: int, reason: str) -> NewEvent:
    return CreatePredicateAssessedEvent(False, coDomain, coId, predicateId, ReasonForControlProcedureFailure(cpId, reason))

class Mode(Enum):
    SaaS = 0
    Firmwide = 1
    RollYourOwn = 2

class Predicate:
    coDomain: ControlObjectiveDomain
    coId: int
    ControlProcedures = []
    def __init__(self, coDomain: ControlObjectiveDomain, coId: int, cpArray):
        self.coDomain = coDomain
        self.coId = coId
        self.ControlProcedures = cpArray

    def HandlePredicateFailure(self, cpId: int, reason: str):
        CreatePredicateFailedEvent(self.coDomain, self.coId, cpId, reason)


VerifierTrustworthinessModeToCPMapping = [\
    [1],    # SaaS
    [2, 3], # Firmwide
    [2, 3]] # Roll Your Own

class VerifierPredicate_1_1_1(Predicate):
    def __init__(self, mode: Mode):
        Predicate.__init__(self, ControlObjectiveDomain.ConfidentialComputingVerifier, VerifierControlObjectives.VerifierTrustworthiness, VerifierTrustworthinessModeToCPMapping[mode])
