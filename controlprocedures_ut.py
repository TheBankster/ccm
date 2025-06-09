from __future__ import annotations # allows passing class objects to class member functions
import json
from typing import final
from controlprocedures import ControlProcedureAssessmentResult as CPAR
from controlprocedures import ControlProcedureState
from controlprocedures import ControlProcedureCompletionReport as CPCR

#
print("ControlProcedureAssessmentResult unit tests")
#

cpar = CPAR(
    success=True,
    expected={"key1": 1, "key2": "value2"},
    actual={"key1": 3, "key2": "value4"})

# Validate ControlProcedureAssessment Result JSON (de)serialization
cparJsonStr = cpar.toJson()
print(cparJsonStr)
cpar2 = CPAR.fromJson(cparJsonStr)
cparJsonStr2 = cpar2.toJson()
print(cparJsonStr2)
assert(cparJsonStr == cparJsonStr2)

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
print(cpar3.toJson())
print(cpar4.toJson())
print(cpar5.toJson())

#
print("ControlProcedureCompletionReport unit tests")
#

cpcr = CPCR(
    cpId = 0,
    owner="N702722",
    result=cpar3)

cpcrJsonStr = cpcr.toJson()
print(cpcrJsonStr)
cpcr2 = CPCR.fromJson(cpcrJsonStr)
cpcrJsonStr2 = cpcr2.toJson()
print(cpcrJsonStr2)
assert(cpcrJsonStr == cpcrJsonStr2)


