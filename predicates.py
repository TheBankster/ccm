from esdbclient import NewEvent
from enum import Enum
from controlprocedures import ControlProcedureIdentifier
from controlobjectives import ControlObjectiveDomain
from eventtypes import ControlProcedureCompleted
from controlobjectives import VerifierControlObjectives, ReverseProxyControlObjectives

#
# Predicate Helpers
#

def PredicateIdentifier(CODomain: str, COID: int, PredicateID: int) -> str:
    return CODomain + "-" + str(COID) + "-" + str(PredicateID)

class Mode(Enum):
    SaaS = 0
    Firmwide = 1
    RollYourOwn = 2

class Predicate:
    __coDomain: ControlObjectiveDomain
    __coId: int
    __predId: int

    ControlProcedures = {}

    def __init__(self, coDomain: ControlObjectiveDomain, coId: int, cpDict = {}):
        self.coDomain = coDomain
        self.coId = coId
        self.ControlProcedures = cpDict

    def HandleControlProcedureCompletion(self, event: NewEvent):
        if (event.type != ControlProcedureCompleted):
            raise ValueError("Wrong CP completion event type: " + event.type)
        return
        
