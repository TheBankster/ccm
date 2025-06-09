# experimentations go here
from __future__ import annotations # allows passing class objects to class member functions
import json
from typing import final

class ControlProcedureAssessmentResult:
    success: bool
    expected: dict
    actual: dict

    def __init__(self, success: bool, expected: dict, actual: dict):
        self.success = success
        self.expected = expected
        self.actual = actual

#    @final
#    def toDict(self) -> dict:
#        return {"success": self.__success, "expected": self.__expected, "actual": self.__actual}
    
    @final
    def isSuccessful(self) -> bool:
        return self.success
    
    @final
    def toJson(self) -> str:
        return json.dumps(self.__dict__, default=lambda o: o.__dict__)
    
    @staticmethod
    def fromJson(encoding: str) -> ControlProcedureAssessmentResult:
        decoding = json.loads(encoding)
        return ControlProcedureAssessmentResult(
            success=decoding["success"],
            expected=decoding["expected"],
            actual=decoding["actual"])

cpar = ControlProcedureAssessmentResult(
    success=True,
    expected={"key1": 1, "key2": "value2"},
    actual={"key1": 3, "key2": "value4"})

jsonStr = cpar.toJson()
print(jsonStr)
cpar2 = ControlProcedureAssessmentResult.fromJson(jsonStr)
jsonStr2 = cpar2.toJson()
print(jsonStr2)
assert(jsonStr == jsonStr2)
