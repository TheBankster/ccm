from __future__ import annotations # allows passing class objects to class member functions
from controlprocedures import ControlProcedure, ControlProcedureState
from readconfig import GetIntInRange, GetNonEmptyString, GetDict, GetBool
import json
import trace

ControlProcedureId = 4

class SystemMaintenanceState(ControlProcedureState):
    def __init__(self, recentlyPatched: bool = True, leastPrivilege: bool = True):
        ControlProcedureState.__init__(
            self,
            cpId=ControlProcedureId,
            state={"RecentlyPatched": recentlyPatched, "LeastPrivilege": leastPrivilege})

    def Compare(self, actual: SystemMaintenanceState) -> bool:
        result = \
            (not self.state["RecentlyPatched"] or actual.state["RecentlyPatched"]) and \
            (not self.state["LeastPrivilege"] or actual.state["LeastPrivilege"])
        return result

class SystemMaintenance(ControlProcedure):
    def __init__(self, stream: str, owner: str, expectedState: SystemMaintenanceState):
        ControlProcedure.__init__(self, ControlProcedureId, stream, owner, expectedState)
