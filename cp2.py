from __future__ import annotations # allows passing class objects to class member functions
from controlprocedures import ControlProcedure, ControlProcedureState, ControlProcedureAssessmentResult, EvidenceFromState

import json
from json import JSONEncoder

ControlProcedureId = 2

class IPSState(ControlProcedureState):
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
            (self.SecureBootEnabled() == state.SecureBootEnabled()) and \
            (self.AntiMalwareCheckResult() == state.AntiMalwareCheckResult())
        evidence = EvidenceFromState(self, state)

        return ControlProcedureAssessmentResult(success, evidence)

class ContractualAgreementWithCSP(ControlProcedure):
    def __init__(self, stream: str, owner: str, state: IPSState):
        ControlProcedure.__init__(self, ControlProcedureId, stream, owner, state)

#test1 = IPSState(secureBoot=True, antimalwareCheckResult="Passed")
#test2 = IPSState(secureBoot=False, antimalwareCheckResult="Passed")
#test3 = IPSState(secureBoot=True,antimalwareCheckResult="Infected with StuxNet")
#result2 = test1.Validate(test2)
#result3 = test1.Validate(test3)
#print(result2.success, result2.evidence)
#print(result3.success, result3.evidence)
