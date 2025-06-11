from __future__ import annotations # allows passing class objects to class member functions
from controlprocedures import ControlProcedure, ControlProcedureState
from readconfig import GetIntInRange, GetNonEmptyString, GetDict, GetBool
import json

ControlProcedureId = 4

class SystemMaintenanceState(ControlProcedureState):
    def __init__(self, recentlyPatched: bool = True, leastPrivilege: bool = True):
        ControlProcedureState.__init__(
            self,
            cpId=ControlProcedureId,
            state={"RecentlyPatched": recentlyPatched, "LeastPrivilege": leastPrivilege})

    def Compare(self, actual: SystemMaintenanceState) -> bool:
        return \
            (not self.state["RecentlyPatched"] or actual.state["RecentlyPatched"]) and \
            (not self.state["LeastPrivilege"] or actual.state["LeastPrivilege"])

class SystemMaintenance(ControlProcedure):
    def __init__(self, stream: str, owner: str, expectedState: SystemMaintenanceState):
        ControlProcedure.__init__(self, ControlProcedureId, stream, owner, expectedState)

    def __init__(self, stream: str, encoding: dict):
        cpId = GetIntInRange(encoding, "cpId", ControlProcedureId, ControlProcedureId)
        owner = GetNonEmptyString(encoding, "owner")
        expected = GetDict(encoding, "expected")
        GetBool(expected, "RecentlyPatched")
        GetBool(expected, "LeastPrivilege")
        ControlProcedure.__init__(
            self,
            cpId,
            stream,
            owner,
            expected)