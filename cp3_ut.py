# CP3 Unit Tests

from cp3 import TEEIsolationState, TEEIsolation
from utils import PayrollDevStream

test1 = TEEIsolationState(correctCode=True, correctConfiguration=True)
test2 = TEEIsolationState(correctCode=False, correctConfiguration=True)
test3 = TEEIsolationState(correctCode=True, correctConfiguration=False)
result2 = test1.Validate(test2)
result3 = test1.Validate(test3)
print(result2.isSuccessful(), result2.toJson())
print(result3.isSuccessful(), result3.toJson())

# Payroll application in Dev environment will have anti-malware but not secure boot
PayrollDevTEEIsolationState = TEEIsolationState(correctCode=True, correctConfiguration=False)
CP3 = TEEIsolation(
    stream=PayrollDevStream,
    owner="E983729",
    expectedState=PayrollDevTEEIsolationState)

EndpointTEECompliantState = TEEIsolationState(correctCode=True, correctConfiguration=True)
EndpointTEENonCompliantState = TEEIsolationState(correctCode=False, correctConfiguration=True)

compliantResult = CP3.AssessControlProcedureState(assessedState=EndpointTEECompliantState)
nonCompliantResult = CP3.AssessControlProcedureState(assessedState=EndpointTEENonCompliantState)

CP3.ReportControlProcedureState(reportedState=EndpointTEECompliantState)
CP3.ReportControlProcedureState(reportedState=EndpointTEENonCompliantState)
