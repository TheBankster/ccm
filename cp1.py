from __future__ import annotations # allows passing class objects to class member functions
from controlprocedures import ControlProcedure, ControlProcedureState, ControlProcedureAssessmentResult, EvidenceFromState

import json
from json import JSONEncoder

ControlProcedureId = 1

class CSPState(ControlProcedureState):
    __csp: str
    __soc3passed: bool

    def Csp(self) -> str:
        return self.__csp
    
    def Soc3Passed(self) -> bool:
        return self.__soc3passed
    
    def __init__(self, csp: str, soc3passed: bool = True):
        ControlProcedureState.__init__(self, ControlProcedureId)
        self.__csp = csp
        self.__soc3passed = soc3passed

    def toJson(self):
        dictionary = {"csp": self.Csp(), "soc3": self.Soc3Passed()}
        return json.dumps(self, default=lambda o: dictionary)

    def Validate(self, state: CSPState) -> ControlProcedureAssessmentResult:
        if self.CpId() != state.CpId():
            raise ValueError("cpId mismatch: " + self.CpId() + " vs " + state.CpId())
        success = \
            (self.Csp() == state.Csp()) and \
            state.Soc3Passed()
        evidence = EvidenceFromState(self, state)

        return ControlProcedureAssessmentResult(success, evidence)

class ContractualAgreementWithCSP(ControlProcedure):
    def __init__(self, stream: str, owner: str, state: CSPState):
        ControlProcedure.__init__(self, ControlProcedureId, stream, owner, state)

#test1 = CSPState("Azure")
#test2 = CSPState("Azure", False)
#result = test1.Validate(test2)
#print(result.success)
#print(result.evidence)
