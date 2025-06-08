#CP1 Unit Tests

from cp1 import CSPState, ContractualAgreementWithCSP
from utils import PayrollDevStream

test1 = CSPState("Azure", True)
test2 = CSPState("Azure", False)
result = test1.Validate(test2)
print(result.isSuccessful())
print(result.toJson())

# Payroll application in Dev environment will be deployed in Azure
PayrollDevCSPState = CSPState(csp="Azure", soc3passed=True)
CP1 = ContractualAgreementWithCSP(
    stream=PayrollDevStream,
    owner="N702766",
    state=PayrollDevCSPState)

PayrollDevCSPCompliantState = CSPState(csp="Azure", soc3passed=True)
PayrollDevCSPNonCompliantState = CSPState(csp="Azure", soc3passed=False)

compliantResult = CP1.AssessControlProcedureState(assessedState=PayrollDevCSPCompliantState)
nonCompliantResult = CP1.AssessControlProcedureState(assessedState=PayrollDevCSPNonCompliantState)

CP1.ReportControlProcedureState(reportedState=PayrollDevCSPCompliantState)
CP1.ReportControlProcedureState(reportedState=PayrollDevCSPNonCompliantState)
