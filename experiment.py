from utils import PayrollDevStream

from cp1 import CSPState, ContractualAgreementWithCSP

# Payroll application in Dev environment will be deployed in Azure
PayrollDevCSPState = CSPState(csp="Azure")
CP1 = ContractualAgreementWithCSP(
    stream=PayrollDevStream,
    owner="N702766",
    state=PayrollDevCSPState)

PayrollDevCSPCompliantState = CSPState(csp="Azure", soc3passed=True)
PayrollDevCSPNonCompliantState = CSPState(csp="Azure", soc3passed=False)

compliantResult = CP1.AssessControlProcedureState(assessedState=PayrollDevCSPCompliantState)
nonCompliantResult = CP1.AssessControlProcedureState(assessedState=PayrollDevCSPNonCompliantState)

#print(compliantResult.success, compliantResult.evidence)
#print(nonCompliantResult.success, nonCompliantResult.evidence)

CP1.ReportControlProcedureState(reportedState=PayrollDevCSPCompliantState)
CP1.ReportControlProcedureState(reportedState=PayrollDevCSPNonCompliantState)
