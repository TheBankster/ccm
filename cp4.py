from __future__ import annotations # allows passing class objects to class member functions
from controlprocedures import ControlProcedure, ControlProcedureState, ControlProcedureAssessmentResult, EvidenceFromState

import json

ControlProcedureId = 4

class SystemMaintenanceState(ControlProcedureState):
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

    def Validate(self, state: SystemMaintenanceState) -> ControlProcedureAssessmentResult:
        if self.CpId() != state.CpId():
            raise ValueError("cpId mismatch: " + self.CpId() + " vs " + state.CpId())
        success = \
            (not self.RecentlyPatched() or state.RecentlyPatched()) and \
            (not self.LeastPrivilege() or state.LeastPrivilege())
        return ControlProcedureAssessmentResult(success, EvidenceFromState(self, state))

class SystemMaintenance(ControlProcedure):
    def __init__(self, stream: str, owner: str, state: SystemMaintenanceState):
        ControlProcedure.__init__(self, ControlProcedureId, stream, owner, state)
