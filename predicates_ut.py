# Predicates unit tests

import json
from predicates import PredicateAssessmentReport as PAR
from controlobjectives import ControlObjectiveDomain as COD
from controlprocedures import ControlProcedureAssessmentResult as CPAR
from controlprocedures import ControlProcedureCompletionReport as CPCR

#
print("PredicateAssessmentReport unit tests")
#

cpar1 = CPAR(
    success=True,
    expected={"key1": 1, "key2": "value2"},
    actual={"key1": 1, "key2": "value2"})
cpar3 = CPAR(
    success=False,
    expected={"key3": 3, "key4": "value4"},
    actual={"key3": 4, "key4": "value5"})
cpcr1 = CPCR(
    cpId = 1,
    owner="N702722",
    result=cpar1)
cpcr3 = CPCR(
    cpId = 3,
    owner="E093722",
    result=cpar3)
par = PAR(
    coDomain=COD.ConfidentialComputingVerifier.value,
    coId=1,
    predId=1,
    incomplete=[2,4],
    complete={1: cpcr1, 3: cpcr3})
parJsonStr=par.toJson()
print(parJsonStr)
par2 = PAR.fromJson(parJsonStr)
parJsonStr2 = par2.toJson()
print(parJsonStr2)
assert(parJsonStr == parJsonStr2)

"""
from predicates import Mode, PredicateAssessmentReport
from VerifierTrustworthinessPredicate import VerifierTrustworthiness as VT
from utils import GlobalClient, UnitTestStream
from eventtypes import ControlProcedureCompleted, PredicateAssessed
from applications import App
from environments import Env
from controlprocedures import ControlProcedureCompletionReport
from cp2 import EndpointIntegrity, EndpointIntegrityState
from cp4 import SystemMaintenance, SystemMaintenanceState

vt = VT(stream=UnitTestStream, mode=Mode.Firmwide)

cp2state = EndpointIntegrityState(secureBoot=True, antimalwareCheckResult="Healthy")
cp2 = EndpointIntegrity(
    stream=UnitTestStream,
    owner="N702766",
    expectedState=cp2state)

cp4state = SystemMaintenanceState(recentlyPatched=True, leastPrivilege=True)
cp4 = SystemMaintenance(
    stream=UnitTestStream,
    owner="E235035",
    expectedState=cp4state)

EndpointIntegrityCompliantState = EndpointIntegrityState(secureBoot=True, antimalwareCheckResult="Healthy")
EndpointIntegrityNonCompliantState = EndpointIntegrityState(secureBoot=False, antimalwareCheckResult="StuxNet")

SystemMaintenanceCompliantState = SystemMaintenanceState(recentlyPatched=True, leastPrivilege=False)
SystemMaintenanceNonCompliantState = SystemMaintenanceState(recentlyPatched=False, leastPrivilege=True)

cp2.ReportControlProcedureState(reportedState=EndpointIntegrityNonCompliantState)
cp4.ReportControlProcedureState(reportedState=SystemMaintenanceNonCompliantState)

cp2.ReportControlProcedureState(reportedState=EndpointIntegrityCompliantState)
cp4.ReportControlProcedureState(reportedState=SystemMaintenanceCompliantState)

subscription = GlobalClient.subscribe_to_stream(stream_name=UnitTestStream)
for event in subscription:
    if event.type == ControlProcedureCompleted:
        report = ControlProcedureCompletionReport.fromJson(event.data)
        print("Control Procedure Completion Report: " + report.toJson())
        vt.HandleControlProcedureCompletion(report)
    elif event.type == PredicateAssessed:
        report = PredicateAssessmentReport.fromJson(event.data)
        print("Predicate Assessment Report: " + report.toJson())
    else:
        print("Unrecognized event type: " + event.type)

input("Press any key to delete the unit test stream")

GlobalClient.delete_stream(
    stream_name=UnitTestStream,
    current_version=GlobalClient.get_current_version(stream_name=UnitTestStream))
"""