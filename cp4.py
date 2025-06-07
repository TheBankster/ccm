from __future__ import annotations # allows passing class objects to class member functions
from controlprocedures import ControlProcedure, ControlProcedureState, ControlProcedureAssessmentResult, EvidenceFromState

import json
from json import JSONEncoder

ControlProcedureId = 4

class MachineMaintenanceState(ControlProcedureState):
    __recentlyPatched: bool
    __leastPrivilege: bool

    def RecentlyPatched(self) -> bool:
        return self.__recentlyPatched
    
    def LeastPrivilege(self) -> bool:
        return self.__leastPrivilege
    
    def __init__(self, recentlyPatched: bool = True, leastPrivilege: bool = True):
        ControlProcedureState.__init__(self, ControlProcedureId)
        self.__recentlyPatched = recentlyPatched
        self.__leastPrivilege = leastPrivilege

    def toJson(self):
        dictionary = {"RecentlyPatched": self.RecentlyPatched(), "LeastPrivilege": self.LeastPrivilege()}
        return json.dumps(self, default=lambda o: dictionary)

    def Validate(self, state: MachineMaintenanceState) -> ControlProcedureAssessmentResult:
        if self.CpId() != state.CpId():
            raise ValueError("cpId mismatch: " + self.CpId() + " vs " + state.CpId())
        success = \
            (self.RecentlyPatched() == state.RecentlyPatched()) and \
            (self.LeastPrivilege() == state.LeastPrivilege())
        evidence = EvidenceFromState(self, state)

        return ControlProcedureAssessmentResult(success, evidence)

class MachineMaintenance(ControlProcedure):
    def __init__(self, stream: str, owner: str, state: TEEState):
        ControlProcedure.__init__(self, ControlProcedureId, stream, owner, state)

test1 = MachineMaintenanceState(recentlyPatched=True, leastPrivilege=True)
test2 = MachineMaintenanceState(recentlyPatched=False, leastPrivilege=True)
test3 = MachineMaintenanceState(recentlyPatched=True,leastPrivilege=False)
result2 = test1.Validate(test2)
result3 = test1.Validate(test3)
print(result2.success, result2.evidence)
print(result3.success, result3.evidence)
