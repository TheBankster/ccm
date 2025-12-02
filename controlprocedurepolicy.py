# Utilities for policy handling

from __future__ import annotations # allows passing class objects to class member functions
from controlprocedures import ControlProcedure, ControlProcedureState, ValidateOwner
from cp1 import ContractualAgreementWithCSP, CSPState
from cp2 import EndpointIntegrity, EndpointIntegrityState
from cp3 import TEEIsolation, TEEIsolationState
from cp4 import SystemMaintenance, SystemMaintenanceState
import json
from readconfig import GetPositiveInt, GetDict, GetNonEmptyString, GetBool, GetIntInRange
from typing import Tuple, final
from utils import trace, GlobalClient
from kurrentdbclient import NewEvent, StreamState
from eventtypes import ControlProcedureUpdated

class ControlProcedureUpdateReport:
    cpId: int
    owner: str
    expectedState: dict

    def __init__(self, cpId: int, owner: str, expectedState: dict):
        self.cpId = cpId
        ValidateOwner(owner)
        self.owner = owner
        self.expectedState = expectedState

    @final
    def toJson(self) -> str:
        return json.dumps(self.__dict__, default=lambda o: o.__dict__)
    
    @staticmethod
    def fromJson(encoding: str) -> ControlProcedureUpdateReport:
        decoding = json.loads(encoding)
        return ControlProcedureUpdateReport(
            cpId=decoding["cpId"],
            owner=decoding["owner"],
            expectedState=decoding["expectedState"])

def ControlProcedureStateFromDict(cpId: int, d: dict) -> ControlProcedureState:
    match cpId:
        case 1:
            state = CSPState(
                csp=GetNonEmptyString(d, "CSP"),
                soc3=GetBool(d, "SOC3"))
        case 2:
            state = EndpointIntegrityState(
                secureBoot=GetBool(d, "SecureBoot"),
                antimalwareCheck=GetNonEmptyString(d, "AntiMalwareCheck"))
        case 3:
            state = TEEIsolationState(
                codeVersion=GetIntInRange(d, "CodeVersion", 1, 65536),
                configurationHash=GetPositiveInt(d, "ConfigurationHash"))
        case 4:
            state = SystemMaintenanceState(
                recentlyPatched=GetBool(d, "RecentlyPatched"),
                leastPrivilege=GetBool(d, "LeastPrivilege"))
        case _:
            raise ValueError("Unexpected CpId")
    return state

def ControlProcedureFromUpdateReport(controlStream: str, report=ControlProcedureUpdateReport) -> ControlProcedure:
    cpId = report.cpId
    owner = report.owner
    expectedState = ControlProcedureStateFromDict(cpId, report.expectedState)
    match cpId:
        case 1:
            result = ContractualAgreementWithCSP(controlStream, owner, expectedState)
        case 2:
            result = EndpointIntegrity(controlStream, owner, expectedState)
        case 3:
            result = TEEIsolation(controlStream, owner, expectedState)
        case 4:
            result = SystemMaintenance(controlStream, owner, expectedState)
        case _:
            raise ValueError("Unexpected CpId")
    return result

def ReadPolicy(filename: str) -> list[Tuple[int, str, dict]]:
    result: list[Tuple[int, str, dict]] = []
    with open(filename, 'r') as file:
        lines = file.readlines()
        for l in lines:
            entry = json.loads(l)
            cpId = GetPositiveInt(entry, "cpId")
            owner = GetNonEmptyString(entry, "owner")
            ValidateOwner(owner)
            expectedState = GetDict(entry, "expected")
            result.append((cpId, owner, expectedState))
    return result

def UpdatePolicy(policyStream: str, filename: str) -> None:
    policy = ReadPolicy(filename)
    events = []
    for entry in policy:
        cpId = entry[0]
        owner = entry[1]
        expectedState = entry[2]
        updateReport = ControlProcedureUpdateReport(
            cpId=cpId,
            owner=owner,
            expectedState=expectedState)
        events.append(NewEvent(
            type=ControlProcedureUpdated,
            data=updateReport.toJson().encode('utf-8')))
    GlobalClient.append_to_stream(
        stream_name=policyStream,
        events=events,
        current_version=StreamState.ANY)
    return

def ReadControlState(filename: str) -> dict[int, ControlProcedureState]:
    result: dict[int, ControlProcedureState] = {}
    with open(filename, 'r') as file:
        lines = file.readlines()
        for l in lines:
            entry = json.loads(l)
            cpId = GetPositiveInt(entry, "cpId")
            actual = GetDict(entry, "actual")
            result[cpId] = ControlProcedureStateFromDict(cpId, actual)
    return result

def ReportControlState(filename: str, cpDict: dict[int, ControlProcedure]) -> None:
    controlState = ReadControlState(filename)
    for cpId in controlState.keys():
        cp = cpDict[cpId]
        assert(isinstance(cp, ControlProcedure))
        cpState = controlState[cpId]
        assert(isinstance(cpState, ControlProcedureState))
        cp.ReportControlProcedureState(cpState)
