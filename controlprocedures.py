#
# Control Procedure Helpers
#

from controlprocedures import ControlProcedureCompletionEvent
from esdbclient import NewEvent

def ControlProcedureIdentifier(cpid: int) -> str:
    ControlProcedurePrefix = "CP-"
    return ControlProcedurePrefix + str(cpid)

class ControlProcedure:
    cpId: int
    def __init__(self, cpId: int):
        self.cpId = cpId
    # Control Procedure Completion Event Creation
    def CreateControlProcedureCompletionEvent(success: bool, cpId: int, evidence) -> NewEvent:
        dataString = \
            "{\"ControlProcedureID\":" + str(cpId) + "," + \
            "\"Evidence\":" + evidence + "}"
        return NewEvent(
            ControlProcedureCompletionEvent,
            data = dataString.encode('utf-8'))

class ContractualAgreementWithCSP(ControlProcedure):
    def __init__(self):
        ControlProcedure.__init__(self, 1)

class EndpointIntrusionDetectionAndPrevention(ControlProcedure):
    def __init__(self):
        ControlProcedure.__init__(self, 2)

class TeeAssistedIsolation(ControlProcedure):
    def __init__(self):
        ControlProcedure.__init__(self, 3)
        