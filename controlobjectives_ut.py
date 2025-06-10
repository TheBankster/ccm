# ControlObjectives unit tests

from controlprocedures import ControlProcedureAssessmentResult, ControlProcedureAssessmentReport
from predicates import PredicateAssessmentReport as PAR, Mode
from controlobjectives import ControlObjective, ControlObjectiveAssessmentReport as COAR
from controlobjectiveenums import ControlObjectiveDomain as COD
from eventtypes import PredicateAssessed, ControlObjectiveAssessed
from utils import UnitTestStream
from utils import GlobalClient

#
print("ControlObjectiveAssessmentReport unit tests")
#

cpar2 = ControlProcedureAssessmentResult(
    success=False,
    expected={"key1": 1, "key2": "value2"},
    actual={"key1": 1, "key2": "value2"})
cpcr2 = ControlProcedureAssessmentReport(
    cpId = 2,
    owner="N702722",
    expected=cpar2.expected,
    actual=cpar2.actual,
    success=cpar2.success)
par3=PAR(
    coDomain=COD.ConfidentialComputingVerifier.value,
    coId=7,
    predId=3,
    incomplete=[],
    complete={2: cpcr2},
    success=False)
par3JsonStr=par3.toJson()
coar7=COAR(
    coDomain=COD.ConfidentialComputingVerifier.value,
    coId=7,
    incomplete=[4],
    complete={3: par3},
    success=False)
coarJsonStr=coar7.toJson()
print(coarJsonStr)
coar7C=COAR.fromJson(coarJsonStr)
coarJsonStrC=coar7C.toJson()
assert(coarJsonStr == coarJsonStrC)

#
print("ControlObjectve Unit Tests")
#

class UnitTestControlObjective(ControlObjective):
    def __init__(self):
        ControlObjective.__init__(
            self,
            coDomain=COD.ConfidentialComputingVerifier.value,
            coId=7,
            stream=UnitTestStream,
            predIds=[3])
        
utco = UnitTestControlObjective()
utco.HandlePredicateCompletion(completion=par3)

subscription = GlobalClient.subscribe_to_stream(stream_name=UnitTestStream)
for event in subscription:
    if event.type == ControlObjectiveAssessed:
        report = COAR.fromJson(event.data)
    else:
        print("Unrecognized event type: " + event.type)
input("Press any key to delete the unit test stream")

GlobalClient.delete_stream(
    stream_name=UnitTestStream,
    current_version=GlobalClient.get_current_version(stream_name=UnitTestStream))
