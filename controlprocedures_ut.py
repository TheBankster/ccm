# ControlProcedures unit tests

from __future__ import annotations # allows passing class objects to class member functions
import json
from typing import final
from controlprocedures import ControlProcedureState
from controlprocedures import ControlProcedureAssessmentReport as CPCR

#
print("ControlProcedureState unit tests")
#

class SampleControlProcedureState(ControlProcedureState):
    def __init__(self, expectedValue1: bool, expectedValue2: str):
        ControlProcedureState.__init__(
            self,
            cpId=0,
            state={"Key1": expectedValue1, "Key2": expectedValue2})

    def Compare(self, actual: SampleControlProcedureState) -> bool:
        return \
            (self.state["Key1"] == actual.state["Key1"]) and \
            (self.state["Key2"] == actual.state["Key2"])
    
scps = SampleControlProcedureState(True, "Healthy")
scpsGood = SampleControlProcedureState(True, "Healthy")
scpsBad1 = SampleControlProcedureState(False, "Healthy")
scpsBad2 = SampleControlProcedureState(True, "Unhealthy")

cpar3 = scps.Validate(actual=scpsGood)
cpar4 = scps.Validate(actual=scpsBad1)
cpar5 = scps.Validate(actual=scpsBad2)
assert(cpar3.success == True)
assert(cpar4.success == False)
assert(cpar5.success == False)

#
print("ControlProcedureCompletionReport unit tests")
#

cpcr = CPCR(
    cpId = 0,
    owner="N702722",
    expected=cpar3.expected,
    actual=cpar3.actual,
    success=cpar3.success)

cpcrJsonStr = cpcr.toJson()
print(cpcrJsonStr)
cpcr2 = CPCR.fromJson(cpcrJsonStr)
cpcrJsonStr2 = cpcr2.toJson()
print(cpcrJsonStr2)
assert(cpcrJsonStr == cpcrJsonStr2)


