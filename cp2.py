from __future__ import annotations # allows passing class objects to class member functions
from controlprocedures import ControlProcedure, ControlProcedureState

import json

ControlProcedureId = 2

class EndpointIntegrityState(ControlProcedureState):
    __secureBoot: bool
    __antimalwareCheckResult: str

    def SecureBootEnabled(self) -> bool:
        return self.__secureBoot
    
    def AntiMalwareCheckResult(self) -> str:
        return self.__antimalwareCheckResult
    
    def __init__(self, secureBoot: bool, antimalwareCheckResult: str):
        ControlProcedureState.__init__(self, ControlProcedureId)
        self.__secureBoot = secureBoot
        self.__antimalwareCheckResult = antimalwareCheckResult

    def toDict(self):
        return { \
            "SecureBootEnabled": self.SecureBootEnabled(),
            "AntiMalwareCheckResult": self.AntiMalwareCheckResult()}

    def Compare(self, state: EndpointIntegrityState) -> bool:
        return \
            (not self.SecureBootEnabled() or state.SecureBootEnabled()) and \
            (self.AntiMalwareCheckResult() == "" or self.AntiMalwareCheckResult() == state.AntiMalwareCheckResult())

class EndpointIntegrity(ControlProcedure):
    def __init__(self, stream: str, owner: str, state: EndpointIntegrityState):
        ControlProcedure.__init__(self, ControlProcedureId, stream, owner, state)
