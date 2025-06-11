from __future__ import annotations # allows passing class objects to class member functions
from controlprocedures import ControlProcedure, ControlProcedureState
from readconfig import GetIntInRange, GetNonEmptyString, GetDict, GetPositiveInt
import json

ControlProcedureId = 3

class TEEIsolationState(ControlProcedureState):
    def __init__(self, codeVersion: int, configurationHash: int):
        ControlProcedureState.__init__(
            self,
            cpId=ControlProcedureId,
            state={"CodeVersion": codeVersion, "ConfigurationHash": configurationHash})

    def Compare(self, actual: TEEIsolationState) -> bool:
        return \
            (self.state["CodeVersion"] <= actual.state["CodeVersion"]) and \
            (self.state["ConfigurationHash"] == actual.state["ConfigurationHash"])

class TEEIsolation(ControlProcedure):
    def __init__(self, stream: str, owner: str, expectedState: TEEIsolationState):
        ControlProcedure.__init__(self, ControlProcedureId, stream, owner, expectedState)

    def __init__(self, stream: str, encoding: dict):
        cpId = GetIntInRange(encoding, "cpId", ControlProcedureId, ControlProcedureId)
        owner = GetNonEmptyString(encoding, "owner")
        expected = GetDict(encoding, "expected")
        GetIntInRange(expected, "CodeVersion", 1, 65536)
        GetPositiveInt(expected, "ConfigurationHash")
        ControlProcedure.__init__(
            self,
            cpId,
            stream,
            owner,
            expected)
