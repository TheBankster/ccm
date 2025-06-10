#
# Control Procedure Helpers
#

from __future__ import annotations # allows passing class objects to class member functions
import re
import json
from typing import final
from eventtypes import ControlProcedureAssessed
from esdbclient import NewEvent, StreamState
from utils import GlobalClient

def ControlProcedureIdentifier(cpid: int) -> str:
    ControlProcedurePrefix = "CP-"
    return ControlProcedurePrefix + str(cpid)

ControlProcedureNames = [
    "Contractual Agreement with the CSP",                   # 1
    "Endpoint Intrusion Prevention and Detection",          # 2
    "Trusted Execution Environment-Assisted Isolation",     # 3
    "Virtual/Physical Machine System Maintenance",          # 4
    "Ensure Correct Configuration of a Deployed Service",   # 5
    "Ensure Correct Network Area of a Service",             # 6
    "Service Health and Latency Checks",                    # 7
    "Service Redundancy and Auto-Scaling Checks",           # 8
    "Service Configuration Protection",                     # 9
    "Service Key Lifecycle Management",                     # 10
    "Service Log Redaction and Protection",                 # 11
    "Service Data-in-Transit Protection",                   # 12
    "Service Policies Stored in a System of Record",        # 13
    "Secure Service Policy and Key History Storage"         # 14
    ]

class ControlProcedureAssessmentResult:
    success: bool
    expected: dict
    actual: dict

    def __init__(self, success: bool, expected: dict, actual: dict):
        self.success = success
        self.expected = expected
        self.actual = actual

# Abstract base class for all derived CP states
class ControlProcedureState:
    cpId: int # for sanity checking
    state: dict

    def __init__(self, cpId: int, state: dict):
        self.cpId = cpId
        self.state = state
    
    def Compare(self, actual: ControlProcedureState) -> bool:
        raise NotImplementedError("Implement Validate() method")
    
    # Returns 'True' if 'actual' state is valid when compared with the 'expected' state
    # Implement in each derived class
    @final
    def Validate(self, actual: ControlProcedureState) -> ControlProcedureAssessmentResult:
        if self.cpId != actual.cpId:
            raise ValueError("cpId mismatch: " + self.CpId() + " vs " + actual.CpId())
        return ControlProcedureAssessmentResult(
            success=self.Compare(actual),
            expected=self.state,
            actual=actual.state)
    
def ValidateOwner(owner: str):
    assert re.match(r'^[A-Z]\d{6}$', owner)

class ControlProcedureAssessmentReport:
    cpId: int
    owner: str
    expected: dict
    actual: dict
    success: bool

    def __init__(self, cpId: int, owner: str, expected: dict, actual: dict, success: bool):
        self.cpId = cpId
        ValidateOwner(owner)
        self.owner = owner
        self.expected = expected
        self.actual = actual
        self.success = success
    
    @final
    def toJson(self) -> str:
        return json.dumps(self.__dict__, default=lambda o: o.__dict__)
    
    @staticmethod
    def fromJson(encoding: str) -> ControlProcedureAssessmentReport:
        decoding = json.loads(encoding)
        return ControlProcedureAssessmentReport(
            cpId=decoding["cpId"],
            owner=decoding["owner"],
            expected=decoding["expected"],
            actual=decoding["actual"],
            success=decoding["success"])

class ControlProcedure:
    __cpId: int
    __stream: str
    __owner: str
    __expectedState: ControlProcedureState

    def __init__(self, cpId: int, stream: str, owner: str, expectedState: ControlProcedureState):
        self.__cpId = cpId
        self.__stream = stream
        ValidateOwner(owner)
        self.__owner = owner
        self.__expectedState = expectedState

    def UpdateExpectedState(self, newState: ControlProcedureState):
        if self.CpId() != newState.CpId():
            raise ValueError("cpId mismatch: " + self.CpId() + " vs " + newState.CpId())
        self.__expectedState = newState
        
    def __AppendControlProcedureCompletionEvent(self, assessmentResult: ControlProcedureAssessmentResult):
        completionReport = ControlProcedureAssessmentReport(
            cpId=self.__cpId,
            owner=self.__owner,
            expected=assessmentResult.expected,
            actual=assessmentResult.actual,
            success=assessmentResult.success)
        GlobalClient.append_to_stream(
            stream_name=self.__stream,
            events=NewEvent(
                type=ControlProcedureAssessed,
                data=completionReport.toJson().encode('utf-8')),
            current_version=StreamState.ANY)
    
    def AssessControlProcedureState(self, assessedState: ControlProcedureState) -> ControlProcedureAssessmentResult:
        return self.__expectedState.Validate(assessedState)
    
    def ReportControlProcedureState(self, reportedState: ControlProcedureState):
        self.__AppendControlProcedureCompletionEvent(self.AssessControlProcedureState(reportedState))
