import array as arr
from esdbclient import NewEvent
from enum import Enum
from controlprocedures import ControlProcedureIdentifier
from controlobjectives import ControlObjectiveDomain

#
# Predicate Helpers
#

# Predicate Event Types
PredicateSucceeded = "PredicateSucceeded"
PredicateFailed = "PredicateFailed"

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

FailedCP = "FailedControlProcedure"

def CreatePredicateSucceededEvent(domain: ControlObjectiveDomain, coId: int, predicateId: int, reason: str = "") -> NewEvent:
    return CreatePredicateAssessedEvent(True, domain, coId, predicateId)

def ReasonForControlProcedureFailure(cpId: int, reason: str) -> str:
    return \
        "{\"" + FailedCP + "\":\"" + ControlProcedureIdentifier(cpId) + "\"," + \
        "\"Reason\":\"" + reason + "\"}"

def CreatePredicateFailedEvent(domain: ControlObjectiveDomain, coId: int, predicateId: int, cpId: int, reason: str) -> NewEvent:
    return CreatePredicateAssessedEvent(False, domain, coId, predicateId, ReasonForControlProcedureFailure(cpId, reason))

class Mode(Enum):
    SaaS = 0
    Firmwide = 1
    RollYourOwn = 2

class Predicate:
    ControlObjectiveId: str
    ControlProcedures = []
    def __init__(self, mode: Mode, cpsArray):
        self.ControlProcedures = cpsArray

    def HandlePredicateFailure(self):
        raise NotImplementedError("Predicate is an abstract class")

class VerifierPredicate_1_1_1(Predicate):
    
    def __init__(self, mode: Mode):
        ModeToCPMapping = [\
            ["CP-1"], # SaaS
            ["CP-2", "CP-3"], # Firmwide
            ["CP-2", "CP-3"]] # Roll Your Own
        Predicate.__init__(mode, ModeToCPMapping[mode])
