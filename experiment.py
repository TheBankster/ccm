from __future__ import annotations # allows passing class objects to class member functions

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
    
    # Returns 'True' if hypotheticalState is valid when compared with the expected state
    # Implement in each derived class
    def Validate(self, hypotheticalState: ControlProcedureState) -> ControlProcedureAssessmentResult:
        raise NotImplementedError("Implement a subclasee of ControlProcedureState for your Control Procedure", self.__cpId)

# Placeholder CP state class until the rest are implemented
class SampleControlProcedureState(ControlProcedureState):
    expectedState: bool
    def __init__(self, cpId: int, expectedState: bool):
        ControlProcedureState.__init__(self, cpId)
        self.expectedState = expectedState

    def Validate(self, hypotheticalState: SampleControlProcedureState) -> ControlProcedureAssessmentResult:
        if self.CpId() != hypotheticalState.CpId():
            raise ValueError("cpId mismatch")
        return ControlProcedureAssessmentResult(
            success = (self.expectedState == hypotheticalState.expectedState),
            evidence = "Expected " + str(self.expectedState) + " Received " + str(hypotheticalState.expectedState))
    
test1 = SampleControlProcedureState(1, False)
test2 = SampleControlProcedureState(1, True)

result = test1.Validate(test2)
print(result.success)
print(result.evidence)
