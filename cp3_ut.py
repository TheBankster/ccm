# CP3 Unit Tests

from cp3 import TEEIsolationState, TEEIsolation
from utils import UnitTestStream

test1 = TEEIsolationState(codeVersion=3, configurationHash=12345)
test2 = TEEIsolationState(codeVersion=4, configurationHash=12345)
test3 = TEEIsolationState(codeVersion=2, configurationHash=23456)
result2 = test1.Validate(test2)
result3 = test1.Validate(test3)
print(result2.isSuccessful(), result2.toJson())
print(result3.isSuccessful(), result3.toJson())

# Payroll application in Dev environment will have anti-malware but not secure boot
UnitTestTEEIsolationState = TEEIsolationState(codeVersion=2, configurationHash=34567)
CP3 = TEEIsolation(
    stream=UnitTestStream,
    owner="E983729",
    expectedState=UnitTestTEEIsolationState)

EndpointTEECompliantState = TEEIsolationState(codeVersion=3, configurationHash=34567)
EndpointTEENonCompliantState = TEEIsolationState(codeVersion=2, configurationHash=45678)

compliantResult = CP3.AssessControlProcedureState(assessedState=EndpointTEECompliantState)
nonCompliantResult = CP3.AssessControlProcedureState(assessedState=EndpointTEENonCompliantState)

CP3.ReportControlProcedureState(reportedState=EndpointTEECompliantState)
CP3.ReportControlProcedureState(reportedState=EndpointTEENonCompliantState)
