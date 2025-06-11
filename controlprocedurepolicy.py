from controlprocedures import ControlProcedure, ControlProcedureState
from cp1 import ContractualAgreementWithCSP, CSPState
from cp2 import EndpointIntegrity, EndpointIntegrityState
from cp3 import TEEIsolation, TEEIsolationState
from cp4 import SystemMaintenance, SystemMaintenanceState
import json
from readconfig import GetPositiveInt, GetDict, GetNonEmptyString, GetBool, GetIntInRange

def ReadPolicy(stream: str, filename: str) -> dict[int, ControlProcedure]:
    result: dict[int, ControlProcedure] = {}
    with open(filename, 'r') as file:
        lines = file.readlines()
        for l in lines:
            entry = json.loads(l)
            cpId = GetPositiveInt(entry, "cpId")
            match cpId:
                case 1:
                    result[1] = ContractualAgreementWithCSP(stream, entry)
                case 2:
                    result[2] = EndpointIntegrity(stream, entry)
                case 3:
                    result[3] = TEEIsolation(stream, entry)
                case 4:
                    result[4] = SystemMaintenance(stream, entry)
                case _:
                    raise ValueError("Unexpected CpId")
    return result

def ReadActual(filename: str) -> dict[int, ControlProcedureState]:
    result: dict[int, ControlProcedureState] = {}
    with open(filename, 'r') as file:
        lines = file.readlines()
        for l in lines:
            entry = json.loads(l)
            cpId = GetPositiveInt(entry, "cpId")
            actual = GetDict(entry, "actual")
            match cpId:
                case 1:
                    result[cpId] = CSPState(
                        csp=GetNonEmptyString(actual, "CSP"),
                        soc3=GetBool(actual, "SOC3"))
                case 2:
                    result[cpId] = EndpointIntegrityState(
                        secureBoot=GetBool(actual, "SecureBoot"),
                        antimalwareCheck=GetNonEmptyString(actual, "AntiMalwareCheck"))
                case 3:
                    result[cpId] = TEEIsolationState(
                        codeVersion=GetIntInRange(actual, "CodeVersion", 1, 65536),
                        configurationHash=GetPositiveInt(actual, "ConfigurationHash"))
                case 4:
                    result[cpId] = SystemMaintenanceState(
                        recentlyPatched=GetBool(actual, "RecentlyPatched"),
                        leastPrivilege=GetBool(actual, "LeastPrivilege"))
                case _:
                    raise ValueError("Unexpected CpId")
    return result
