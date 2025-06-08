from __future__ import annotations # allows passing class objects to class member functions
from controlprocedures import ControlProcedure, ControlProcedureState

import json

ControlProcedureId = 1

class CSPState(ControlProcedureState):
    __csp: str
    __soc3passed: bool

    def Csp(self) -> str:
        return self.__csp
    
    def Soc3Passed(self) -> bool:
        return self.__soc3passed
    
    def __init__(self, csp: str, soc3passed: bool):
        ControlProcedureState.__init__(self, ControlProcedureId)
        self.__csp = csp
        self.__soc3passed = soc3passed

    def toDict(self):
        return {"csp": self.Csp(), "soc3": self.Soc3Passed()}

    def Compare(self, state: CSPState) -> bool:
        return \
            (self.Csp() == state.Csp()) and \
            (not self.Soc3Passed() or state.Soc3Passed())

class ContractualAgreementWithCSP(ControlProcedure):
    def __init__(self, stream: str, owner: str, state: CSPState):
        ControlProcedure.__init__(self, ControlProcedureId, stream, owner, state)

