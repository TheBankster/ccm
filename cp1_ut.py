#CP1 Unit Tests

from cp1 import CSPState, ContractualAgreementWithCSP
from utils import UnitTestStream

test1 = CSPState("Azure", True)
test2 = CSPState("Azure", False)
result = test1.Validate(test2)
print(result.isSuccessful(), result.toJson())

# Payroll application in Dev environment will be deployed in Azure
UnitTestCSPState = CSPState(csp="Azure", soc3=True)
CP1 = ContractualAgreementWithCSP(
    stream=UnitTestStream,
    owner="N702766",
    expectedState=UnitTestCSPState)

CSPCompliantState = CSPState(csp="Azure", soc3=True)
CSPNonCompliantState = CSPState(csp="Azure", soc3=False)

compliantResult = CP1.AssessControlProcedureState(assessedState=CSPCompliantState)
nonCompliantResult = CP1.AssessControlProcedureState(assessedState=CSPNonCompliantState)

CP1.ReportControlProcedureState(reportedState=CSPCompliantState)
CP1.ReportControlProcedureState(reportedState=CSPNonCompliantState)
