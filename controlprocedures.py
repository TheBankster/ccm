#
# Control Procedure Helpers
#

from __future__ import annotations # allows passing class objects to class member functions
from eventtypes import ControlProcedureCompleted
from esdbclient import NewEvent, StreamState
from utils import GlobalClient
from typing import final
import re
import json

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
    __success: bool
    __expected: dict
    __actual: dict

    def __init__(self, success: bool, expected: dict, actual: dict):
        self.__success = success
        self.__expected = expected
        self.__actual = actual

    @final
    def toDict(self) -> dict:
        return {"success": self.__success, "expected": self.__expected, "actual": self.__actual}
    
    @final
    def isSuccessful(self) -> bool:
        return self.__success
    
    @final
    def toJson(self) -> str:
        return json.dumps(self.toDict())
    
    @staticmethod
    def fromJson(encoding: str) -> ControlProcedureAssessmentResult:
        decoding = json.loads(encoding)
        return ControlProcedureAssessmentResult(
            success=decoding["success"],
            expected=decoding["expected"],
            actual=decoding["actual"])

# Abstract base class for all derived CP states
class ControlProcedureState:
    __cpId: int # for sanity checking

    def __init__(self, cpId: int):
        self.__cpId = cpId
    
    @final
    def CpId(self) -> int:
        return self.__cpId
    
    def Compare(self, actual: ControlProcedureState) -> bool:
        raise NotImplementedError("Implement Validate() method")
    
    # Returns 'True' if 'actual' state is valid when compared with the 'expected' state
    # Implement in each derived class
    @final
    def Validate(self, state: ControlProcedureState) -> ControlProcedureAssessmentResult:
        if self.CpId() != state.CpId():
            raise ValueError("cpId mismatch: " + self.CpId() + " vs " + state.CpId())
        return ControlProcedureAssessmentResult(
            success=self.Compare(state),
            expected=self.toDict(),
            actual=state.toDict())
    
    def toDict(self) -> dict:
        raise NotImplementedError("Implement toDict() method")

def ValidateOwner(owner: str):
    assert re.match(r'^[A-Z]\d{6}$', owner)

class ControlProcedureCompletionReport:
    cpId: int
    owner: str
    result: ControlProcedureAssessmentResult

    def __init__(self, cpId: int, owner: str, result: ControlProcedureAssessmentResult):
        self.cpId = cpId
        ValidateOwner(owner)
        self.owner = owner
        self.result = result
    
    def toDict(self) -> dict:
        return {
            "cpId": self.cpId,
            "owner": self.owner,
            "result": self.result.toDict() }

    def toJson(self) -> str:
        return json.dumps(self.toDict())
    
    @staticmethod
    def fromJson(encoding: str) -> ControlProcedureCompletionReport:
        decoding = json.loads(encoding)
        return ControlProcedureCompletionReport(
            cpId=decoding["cpId"],
            owner=decoding["owner"],
            result=ControlProcedureAssessmentResult.fromJson(json.dumps(decoding["result"])))

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
        completionReport = ControlProcedureCompletionReport(
            cpId=self.__cpId,
            owner=self.__owner,
            result=assessmentResult)
        GlobalClient.append_to_stream(
            stream_name=self.__stream,
            events=NewEvent(
                type=ControlProcedureCompleted,
                data=completionReport.toJson().encode('utf-8')),
            current_version=StreamState.ANY)
    
    def AssessControlProcedureState(self, assessedState: ControlProcedureState) -> ControlProcedureAssessmentResult:
        return self.__expectedState.Validate(assessedState)
    
    def ReportControlProcedureState(self, reportedState: ControlProcedureState):
        self.__AppendControlProcedureCompletionEvent(self.AssessControlProcedureState(reportedState))

#
# Placeholder code below this line.
#

# Temporary CP state class until the rest are implemented
class SampleControlProcedureState(ControlProcedureState):
    expectedBool: bool
    expectedStr: str

    def __init__(self, expectedBool: bool, expectedStr: str):
        ControlProcedureState.__init__(self, 0)
        self.expectedBool = bool
        self.expectedStr = str

    def toDict(self) -> dict:
        return {"expectedBool": self.expectedBool, "expectedStr": self.expectedStr}

    def Compare(self, state: SampleControlProcedureState) -> bool:
            return \
              (self.expectedBool == state.expectedBool) and \
              (self.expectedStr == state.expectedStr)

class CorrectServiceConfiguration(ControlProcedure):
    def __init__(self, stream: str, owner: str):
        ControlProcedure.__init__(self, 5, stream, owner, SampleControlProcedureState(5))

class CorrectServiceNetworkSurface(ControlProcedure):
    def __init__(self, stream: str, owner: str):
        ControlProcedure.__init__(self, 6, stream, owner, SampleControlProcedureState(6))

class HealthAndLatencyChecks(ControlProcedure):
    def __init__(self, stream: str, owner: str):
        ControlProcedure.__init__(self, 7, stream, owner, SampleControlProcedureState(7))

class RedundancyAndAutoScalingChecks(ControlProcedure):
    def __init__(self, stream: str, owner: str):
        ControlProcedure.__init__(self, 8, stream, owner, SampleControlProcedureState(8))

class ServiceConfigurationProtection(ControlProcedure):
    def __init__(self, stream: str, owner: str):
        ControlProcedure.__init__(self, 9, stream, owner, SampleControlProcedureState(9))

class ServiceKeyLifecycleManagement(ControlProcedure):
    def __init__(self, stream: str, owner: str):
        ControlProcedure.__init__(self, 10, stream, owner, SampleControlProcedureState(10))

class ServiceLogRedactionAndProtection(ControlProcedure):
    def __init__(self, stream: str, owner: str):
        ControlProcedure.__init__(self, 11, stream, owner, SampleControlProcedureState(11))

class ServiceDataInTransitProtection(ControlProcedure):
    def __init__(self, stream: str, owner: str):
        ControlProcedure.__init__(self, 12, stream, owner, SampleControlProcedureState(12))

class ServicePoliciesStoredInSOR(ControlProcedure):
    def __init__(self, stream: str, owner: str):
        ControlProcedure.__init__(self, 13, stream, owner, SampleControlProcedureState(13))

class ServicePolicyAndKeyHistoryStorage(ControlProcedure):
    def __init__(self, stream: str, owner: str):
        ControlProcedure.__init__(self, 14, stream, owner, SampleControlProcedureState(14))
