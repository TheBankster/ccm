from __future__ import annotations # allows passing class objects to class member functions
from controlprocedures import ControlProcedure, ControlProcedureState
from readconfig import GetIntInRange, GetNonEmptyString, GetBool, GetDict
import json
import trace

ControlProcedureId = 2

class EndpointIntegrityState(ControlProcedureState):
    def __init__(self, secureBoot: bool, antimalwareCheck: str):
        ControlProcedureState.__init__(
            self,
            cpId=ControlProcedureId,
            state={"SecureBoot": secureBoot, "AntiMalwareCheck": antimalwareCheck})

    def Compare(self, actual: EndpointIntegrityState) -> bool:
        result = \
            (not self.state["SecureBoot"] or actual.state["SecureBoot"]) and \
            (self.state["AntiMalwareCheck"] == actual.state["AntiMalwareCheck"])
        return result

class EndpointIntegrity(ControlProcedure):
    def __init__(self, stream: str, owner: str, expectedState: EndpointIntegrityState):
        ControlProcedure.__init__(self, ControlProcedureId, stream, owner, expectedState)
