from __future__ import annotations # allows passing class objects to class member functions
from controlprocedures import ControlProcedure, ControlProcedureState
from readconfig import GetIntInRange, GetNonEmptyString, GetDict, GetBool
import json

ControlProcedureId = 1

class CSPState(ControlProcedureState):
    def __init__(self, csp: str, soc3: bool):
        ControlProcedureState.__init__(
            self,
            cpId=ControlProcedureId,
            state={"CSP": csp, "SOC3": soc3})
    
    def Compare(self, actual: CSPState) -> bool:
        return \
            (self.state["CSP"] == actual.state["CSP"]) and \
            (not self.state["SOC3"] or actual.state["SOC3"])

class ContractualAgreementWithCSP(ControlProcedure):
    def __init__(self, stream: str, owner: str, expectedState: CSPState):
        ControlProcedure.__init__(self, ControlProcedureId, stream, owner, expectedState)

    def __init__(self, stream: str, encoding: dict):
        cpId = GetIntInRange(encoding, "cpId", ControlProcedureId, ControlProcedureId)
        owner = GetNonEmptyString(encoding, "owner")
        expected = GetDict(encoding, "expected")
        GetNonEmptyString(expected, "CSP")
        GetBool(expected, "SOC3")
        ControlProcedure.__init__(
            self,
            cpId,
            stream,
            owner,
            expected)