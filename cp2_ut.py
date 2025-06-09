# CP2 Unit Tests

from cp2 import EndpointIntegrityState, EndpointIntegrity
from utils import UnitTestStream

test1 = EndpointIntegrityState(secureBoot=True, antimalwareCheck="Passed")
test2 = EndpointIntegrityState(secureBoot=False, antimalwareCheck="Passed")
test3 = EndpointIntegrityState(secureBoot=True, antimalwareCheck="Infected with StuxNet")
result2 = test1.Validate(test2)
result3 = test1.Validate(test3)
print(result2.isSuccessful(), result2.toJson())
print(result3.isSuccessful(), result3.toJson())

# Payroll application in Dev environment will have anti-malware but not secure boot
UnitTestIntegrityState = EndpointIntegrityState(secureBoot=False, antimalwareCheck="Passed")
CP2 = EndpointIntegrity(
    stream=UnitTestStream,
    owner="F123234",
    expectedState=UnitTestIntegrityState)

EndpointIntegrityCompliantState = EndpointIntegrityState(secureBoot=True, antimalwareCheck="Passed")
EndpointIntegrityNonCompliantState = EndpointIntegrityState(secureBoot=False, antimalwareCheck="StuxNet")

compliantResult = CP2.AssessControlProcedureState(assessedState=EndpointIntegrityCompliantState)
nonCompliantResult = CP2.AssessControlProcedureState(assessedState=EndpointIntegrityNonCompliantState)

CP2.ReportControlProcedureState(reportedState=EndpointIntegrityCompliantState)
CP2.ReportControlProcedureState(reportedState=EndpointIntegrityNonCompliantState)
