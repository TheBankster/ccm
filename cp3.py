from __future__ import annotations # allows passing class objects to class member functions
from controlprocedures import ControlProcedure, ControlProcedureState

import json

ControlProcedureId = 3

class TEEIsolationState(ControlProcedureState):
    __correctCode: bool
    __correctConfiguration: bool

    def CorrectCode(self) -> bool:
        return self.__correctCode
    
    def CorrectConfiguration(self) -> bool:
        return self.__correctConfiguration
    
    def __init__(self, correctCode: bool, correctConfiguration: bool):
        ControlProcedureState.__init__(self, ControlProcedureId)
        self.__correctCode = correctCode
        self.__correctConfiguration = correctConfiguration

    def toDict(self):
        return {"CorrectCode": self.CorrectCode(), "CorrectConfiguration": self.CorrectConfiguration()}

    def Compare(self, state: TEEIsolationState) -> bool:
        return \
            (not self.CorrectCode() or state.CorrectCode()) and \
            (not self.CorrectConfiguration() or state.CorrectConfiguration())

class TEEIsolation(ControlProcedure):
    def __init__(self, stream: str, owner: str, state: TEEIsolationState):
        ControlProcedure.__init__(self, ControlProcedureId, stream, owner, state)
