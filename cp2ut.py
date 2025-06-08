# CP2 Unit Tests

from cp2 import EndpointIntegrityState, EndpointIntegrity
from utils import PayrollDevStream

test1 = EndpointIntegrityState(secureBoot=True, antimalwareCheckResult="Passed")
test2 = EndpointIntegrityState(secureBoot=False, antimalwareCheckResult="Passed")
test3 = EndpointIntegrityState(secureBoot=True, antimalwareCheckResult="Infected with StuxNet")
result2 = test1.Validate(test2)
result3 = test1.Validate(test3)
print(result2.isSuccessful(), result2.toJson())
print(result3.isSuccessful(), result3.toJson())

# Payroll application in Dev environment will have anti-malware but not secure boot
PayrollDevIntegrityState = EndpointIntegrityState(secureBoot=False, antimalwareCheckResult="Passed")
CP2 = EndpointIntegrity(
    stream=PayrollDevStream,
    owner="F123234",
    state=PayrollDevIntegrityState)

EndpointIntegrityCompliantState = EndpointIntegrityState(secureBoot=True, antimalwareCheckResult="Passed")
EndpointIntegrityNonCompliantState = EndpointIntegrityState(secureBoot=False, antimalwareCheckResult="StuxNet")

compliantResult = CP2.AssessControlProcedureState(assessedState=EndpointIntegrityCompliantState)
nonCompliantResult = CP2.AssessControlProcedureState(assessedState=EndpointIntegrityNonCompliantState)

CP2.ReportControlProcedureState(reportedState=EndpointIntegrityCompliantState)
CP2.ReportControlProcedureState(reportedState=EndpointIntegrityNonCompliantState)
