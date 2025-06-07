from __future__ import annotations # allows passing class objects to class member functions
from controlprocedures import ControlProcedure, ControlProcedureState, ControlProcedureAssessmentResult, EvidenceFromState

import json
from json import JSONEncoder

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

    def toJson(self):
        dictionary = {
            "SecureBootEnabled": self.SecureBootEnabled(),
            "AntiMalwareCheckResult": self.AntiMalwareCheckResult()}
        return json.dumps(self, default=lambda o: dictionary)

    def Validate(self, state: IPSState) -> ControlProcedureAssessmentResult:
        if self.CpId() != state.CpId():
            raise ValueError("cpId mismatch: " + self.CpId() + " vs " + state.CpId())
        success = \
            (not self.SecureBootEnabled() or state.SecureBootEnabled()) and \
            (self.AntiMalwareCheckResult() == "" or self.AntiMalwareCheckResult() == state.AntiMalwareCheckResult())
        evidence = EvidenceFromState(self, state)

        return ControlProcedureAssessmentResult(success, evidence)

class EndpointIntegrity(ControlProcedure):
    def __init__(self, stream: str, owner: str, state: EndpointIntegrityState):
        ControlProcedure.__init__(self, ControlProcedureId, stream, owner, state)
