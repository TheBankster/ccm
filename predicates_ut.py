# Predicates unit tests

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