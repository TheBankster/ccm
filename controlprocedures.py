#
# Control Procedure Helpers
#

from __future__ import annotations # allows passing class objects to class member functions
from eventtypes import ControlProcedureCompleted
from esdbclient import NewEvent, StreamState
from utils import GlobalClient
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
    success: bool
    evidence: str
    def __init__(self, success: bool, evidence: str):
        self.success = success
        self.evidence = evidence

# Abstract base class for all derived CP states
class ControlProcedureState:
    __cpId: int # for sanity checking
    def __init__(self, cpId: int):
        self.__cpId = cpId
    
    def CpId(self) -> int:
        return self.__cpId
    
    # Returns 'True' if 'actual' state is valid when compared with the 'expected' state
    # Implement in each derived class
    def Validate(self, actual: ControlProcedureState) -> ControlProcedureAssessmentResult:
        raise NotImplementedError("Implement Validate() method")
    
    def toJson(self) -> str:
        raise NotImplementedError("Implement toJson() method")

def EvidenceFromState(current: ControlProcedureState, actual: ControlProcedureState) -> str:
    return "{\"expected\": " + current.toJson() + ", \"actual\": " + actual.toJson() + "}"

# Placeholder CP state class until the rest are implemented
class SampleControlProcedureState(ControlProcedureState):
    expectedState: bool
    def __init__(self, cpId: int, expectedState: bool):
        ControlProcedureState.__init__(self, cpId)
        self.expectedState = expectedState

    def Validate(self, state: SampleControlProcedureState) -> ControlProcedureAssessmentResult:
        if self.CpId() != state.CpId():
            raise ValueError("cpId mismatch: " + self.CpId() + " vs " + state.CpId())
        return ControlProcedureAssessmentResult(
            success = (self.expectedState == state.expectedState),
            evidence = "Expected " + str(self.expectedState) + " Received " + str(state.expectedState))

class ControlProcedure:
    __cpId: int
    __stream: str
    __owner: str
    __expectedState: ControlProcedureState

    def __init__(self, cpId: int, stream: str, owner: str, expectedState: ControlProcedureState):
        self.__cpId = cpId
        self.__stream = stream
        try:
            if not re.match(r'^[A-Z]\d{6}$', owner):
                raise ValueError("Owner must be one capital letter followed by six digits")
            self.__owner = owner
        except ValueError as e:
            raise ValueError(f"Invalid owner format: {e}")
        self.__expectedState = expectedState

    def UpdateExpectedState(self, newState: ControlProcedureState):
        if self.CpId() != newState.CpId():
            raise ValueError("cpId mismatch: " + self.CpId() + " vs " + newState.CpId())
        self.__expectedState = newState
        
    def __AppendControlProcedureCompletionEvent(self, assessmentResult: ControlProcedureAssessmentResult):
        dataString = \
            "{\"ControlProcedureID\": " + str(self.__cpId) + "," + \
            "\"Owner\": \"" + self.__owner + "\"," + \
            "\"Success\": \"" + str(assessmentResult.success) + "\"," + \
            "\"Evidence\":" + assessmentResult.evidence + "}"
        GlobalClient.append_to_stream(
            stream_name=self.__stream,
            events=NewEvent(
                ControlProcedureCompleted,
                data = dataString.encode('utf-8')),
            current_version=StreamState.ANY)
    
    def AssessControlProcedureState(self, assessedState: ControlProcedureState) -> ControlProcedureAssessmentResult:
        return self.__expectedState.Validate(assessedState)
    
    def ReportControlProcedureState(self, reportedState: ControlProcedureState):
        self.__AppendControlProcedureCompletionEvent(self.AssessControlProcedureState(reportedState))

class ContractualAgreementWithCSP(ControlProcedure):
    def __init__(self, stream: str, owner: str):
        ControlProcedure.__init__(self, 1, stream, owner, SampleControlProcedureState(1))

class EndpointIntrusionDetectionAndPrevention(ControlProcedure):
    def __init__(self, stream: str, owner: str):
        ControlProcedure.__init__(self, 2, stream, owner, SampleControlProcedureState(2))

class TeeAssistedIsolation(ControlProcedure):
    def __init__(self, stream: str, owner: str):
        ControlProcedure.__init__(self, 3, stream, owner, SampleControlProcedureState(3))

class MachineSystemMaintenance(ControlProcedure):
    def __init__(self, stream: str, owner: str):
        ControlProcedure.__init__(self, 4, stream, owner, SampleControlProcedureState(4))

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
