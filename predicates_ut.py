# Predicates unit tests

from controlprocedures import ControlProcedureAssessmentResult
from controlprocedures import ControlProcedureAssessmentReport
from predicates import PredicateAssessmentReport as PAR
from controlobjectiveenums import ControlObjectiveDomain as COD

#
print("PredicateAssessmentReport unit tests")
#

result1 = ControlProcedureAssessmentResult(
    success=True,
    expected={"key1": 1, "key2": "value2"},
    actual={"key1": 1, "key2": "value2"})
result3 = ControlProcedureAssessmentResult(
    success=False,
    expected={"key3": 3, "key4": "value4"},
    actual={"key3": 4, "key4": "value5"})
report1 = ControlProcedureAssessmentReport(
    cpId = 1,
    owner="N702722",
    expected=result1.expected,
    actual=result1.actual,
    success=result1.success)
report3 = ControlProcedureAssessmentReport(
    cpId = 3,
    owner="E093722",
    expected=result3.expected,
    actual=result3.actual,
    success=result3.success)
par = PAR(
    coDomain=COD.ConfidentialComputingVerifier.value,
    coId=1,
    predId=1,
    incomplete=[2,4],
    complete={1: report1, 3: report3},
    success=report1.success and report3.success)
parJsonStr=par.toJson()
print(parJsonStr)
par2 = PAR.fromJson(parJsonStr)
parJsonStr2 = par2.toJson()
print(parJsonStr2)
assert(parJsonStr == parJsonStr2)

#
print("Predicate unit tests")
#

from predicates import Predicate, Mode
from utils import GlobalClient, UnitTestStream
from eventtypes import ControlProcedureCompleted, PredicateAssessed
from cp2 import EndpointIntegrity, EndpointIntegrityState
from cp4 import SystemMaintenance, SystemMaintenanceState
from controlobjectives import ControlObjectiveDomain
from controlobjectiveenums import VerifierControlObjectives
from controlprocedures import ControlProcedureAssessmentReport as ControlProcedureAssessmentReport

UnitTestModeToControlProcedureIdMapping = [\
    [1],    # SaaS
    [2, 4], # Firmwide
    [2, 3]] # Roll Your Own

class UnitTestPredicate(Predicate):
    def __init__(self, stream: str, mode: Mode):
        Predicate.__init__(
            self,
            coDomain=ControlObjectiveDomain.ConfidentialComputingVerifier.value,
            coId=VerifierControlObjectives.VerifierTrustworthiness.value,
            predId=1,
            stream=stream,
            cpIds=UnitTestModeToControlProcedureIdMapping[mode.value])

utp = UnitTestPredicate(stream=UnitTestStream, mode=Mode.Firmwide)

cp2state = EndpointIntegrityState(secureBoot=True, antimalwareCheck="Healthy")
cp2 = EndpointIntegrity(
    stream=UnitTestStream,
    owner="N702766",
    expectedState=cp2state)

cp4state = SystemMaintenanceState(recentlyPatched=True, leastPrivilege=True)
cp4 = SystemMaintenance(
    stream=UnitTestStream,
    owner="E235035",
    expectedState=cp4state)

EndpointIntegrityCompliantState = EndpointIntegrityState(secureBoot=True, antimalwareCheck="Healthy")
EndpointIntegrityNonCompliantState = EndpointIntegrityState(secureBoot=False, antimalwareCheck="StuxNet")

SystemMaintenanceCompliantState = SystemMaintenanceState(recentlyPatched=True, leastPrivilege=True)
SystemMaintenanceNonCompliantState = SystemMaintenanceState(recentlyPatched=False, leastPrivilege=True)

cp2.ReportControlProcedureState(reportedState=EndpointIntegrityNonCompliantState)
cp4.ReportControlProcedureState(reportedState=SystemMaintenanceNonCompliantState)

cp2.ReportControlProcedureState(reportedState=EndpointIntegrityCompliantState)
cp4.ReportControlProcedureState(reportedState=SystemMaintenanceCompliantState)

subscription = GlobalClient.subscribe_to_stream(stream_name=UnitTestStream)
for event in subscription:
    if event.type == ControlProcedureCompleted:
        report = ControlProcedureAssessmentReport.fromJson(event.data)
        print("Processing ControlProcedureAssessmentReport: " + report.toJson())
        utp.HandleControlProcedureCompletion(report)
    elif event.type == PredicateAssessed:
        report = PAR.fromJson(event.data)
        print("Processing PredicateAssessmentReport: " + report.toJson())
    else:
        print("Unrecognized event type: " + event.type)

input("Press any key to delete the unit test stream")

GlobalClient.delete_stream(
    stream_name=UnitTestStream,
    current_version=GlobalClient.get_current_version(stream_name=UnitTestStream))
