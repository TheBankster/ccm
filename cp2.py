from __future__ import annotations # allows passing class objects to class member functions
from controlprocedures import ControlProcedure, ControlProcedureState
from readconfig import GetIntInRange, GetNonEmptyString, GetBool, GetDict
import json

ControlProcedureId = 2

class EndpointIntegrityState(ControlProcedureState):
    def __init__(self, secureBoot: bool, antimalwareCheck: str):
        ControlProcedureState.__init__(
            self,
            cpId=ControlProcedureId,
            state={"SecureBoot": secureBoot, "AntiMalwareCheck": antimalwareCheck})

    def Compare(self, actual: EndpointIntegrityState) -> bool:
        return \
            (not self.state["SecureBoot"] or actual.state["SecureBoot"]) and \
            (self.state["AntiMalwareCheck"] == actual.state["AntiMalwareCheck"])

class EndpointIntegrity(ControlProcedure):
    def __init__(self, stream: str, owner: str, expectedState: EndpointIntegrityState):
        ControlProcedure.__init__(self, ControlProcedureId, stream, owner, expectedState)

    def __init__(self, stream: str, encoding: dict):
        cpId = GetIntInRange(encoding, "cpId", ControlProcedureId, ControlProcedureId)
        owner = GetNonEmptyString(encoding, "owner")
        expected = GetDict(encoding, "expected")
        GetBool(expected, "SecureBoot")
        GetNonEmptyString(expected, "AntiMalwareCheck")
        ControlProcedure.__init__(
            self,
            cpId,
            stream,
            owner,
            expected)
