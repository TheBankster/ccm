# CP4 Unit Tests

from cp4 import SystemMaintenanceState, SystemMaintenance
from utils import PayrollDevStream

test1 = SystemMaintenanceState(recentlyPatched=True, leastPrivilege=True)
test2 = SystemMaintenanceState(recentlyPatched=False, leastPrivilege=True)
test3 = SystemMaintenanceState(recentlyPatched=True, leastPrivilege=False)
result2 = test1.Validate(test2)
result3 = test1.Validate(test3)
print(result2.success, result2.evidence)
print(result3.success, result3.evidence)

# Payroll application in Dev environment will have recentlyPatched = True and leastPrivilege = False
PayrollDevSystemMaintenanceState = SystemMaintenanceState(recentlyPatched=True, leastPrivilege=False)
CP4 = SystemMaintenance(
    stream=PayrollDevStream,
    owner="F938291",
    state=PayrollDevSystemMaintenanceState)

SystemMaintenanceCompliantState = SystemMaintenanceState(recentlyPatched=True, leastPrivilege=False)
SystemMaintenanceNonCompliantState = SystemMaintenanceState(recentlyPatched=False, leastPrivilege=True)

compliantResult = CP4.AssessControlProcedureState(assessedState=SystemMaintenanceCompliantState)
nonCompliantResult = CP4.AssessControlProcedureState(assessedState=SystemMaintenanceNonCompliantState)

CP4.ReportControlProcedureState(reportedState=SystemMaintenanceCompliantState)
CP4.ReportControlProcedureState(reportedState=SystemMaintenanceNonCompliantState)
