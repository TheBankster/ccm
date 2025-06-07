# CP3 Unit Tests

from cp3 import TEEState, TEEIsolation
from utils import PayrollDevStream

test1 = TEEState(correctCode=True, correctConfiguration=True)
test2 = TEEState(correctCode=False, correctConfiguration=True)
test3 = TEEState(correctCode=True,correctConfiguration=False)
result2 = test1.Validate(test2)
result3 = test1.Validate(test3)
print(result2.success, result2.evidence)
print(result3.success, result3.evidence)

# Payroll application in Dev environment will have anti-malware but not secure boot
PayrollDevTEEState = TEEState(correctCode=True,correctConfiguration=False)
CP3 = TEEIsolation(
    stream=PayrollDevStream,
    owner="E983729",
    state=PayrollDevTEEState)

EndpointTEECompliantState = TEEState(correctCode=True, correctConfiguration=True)
EndpointTEENonCompliantState = TEEState(correctCode=False, correctConfiguration=True)

compliantResult = CP3.AssessControlProcedureState(assessedState=EndpointTEECompliantState)
nonCompliantResult = CP3.AssessControlProcedureState(assessedState=EndpointTEENonCompliantState)

CP3.ReportControlProcedureState(reportedState=EndpointTEECompliantState)
CP3.ReportControlProcedureState(reportedState=EndpointTEENonCompliantState)
