from __future__ import annotations # allows passing class objects to class member functions
from controlprocedures import ControlProcedure, ControlProcedureState, ControlProcedureAssessmentResult, EvidenceFromState

import json

ControlProcedureId = 3

class TEEIsolationState(ControlProcedureState):
    __correctCode: bool
    __correctConfiguration: bool

    def CorrectCode(self) -> bool:
        return self.__correctCode
    
    def CorrectConfiguration(self) -> bool:
        return self.__correctConfiguration
    
    def __init__(self, correctCode: bool = True, correctConfiguration: bool = True):
        ControlProcedureState.__init__(self, ControlProcedureId)
        self.__correctCode = correctCode
        self.__correctConfiguration = correctConfiguration

    def toJson(self):
        dictionary = {"CorrectCode": self.CorrectCode(), "CorrectConfiguration": self.CorrectConfiguration()}
        return json.dumps(self, default=lambda o: dictionary)

    def Validate(self, state: TEEIsolationState) -> ControlProcedureAssessmentResult:
        if self.CpId() != state.CpId():
            raise ValueError("cpId mismatch: " + self.CpId() + " vs " + state.CpId())
        success = \
            (not self.CorrectCode() or state.CorrectCode()) and \
            (not self.CorrectConfiguration() or state.CorrectConfiguration())
        return ControlProcedureAssessmentResult(success, EvidenceFromState(self, state))

class TEEIsolation(ControlProcedure):
    def __init__(self, stream: str, owner: str, state: TEEIsolationState):
        ControlProcedure.__init__(self, ControlProcedureId, stream, owner, state)
