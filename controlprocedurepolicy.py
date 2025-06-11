from controlprocedures import ControlProcedure
from cp1 import ContractualAgreementWithCSP
from cp2 import EndpointIntegrity
from cp3 import TEEIsolation
from cp4 import SystemMaintenance
import json
from readconfig import GetPositiveInt

def ReadPolicy(stream: str, filename: str) -> list[ControlProcedure]:
    result: list[ControlProcedure] = []
    with open(filename, 'r') as file:
        lines = file.readlines()
        for l in lines:
            entry = json.loads(l)
            cpId = GetPositiveInt(entry, "cpId")
            match cpId:
                case 1:
                    result.append(ContractualAgreementWithCSP(stream, entry))
                case 2:
                    result.append(EndpointIntegrity(stream, entry))
                case 3:
                    result.append(TEEIsolation(stream, entry))
                case 4:
                    result.append(SystemMaintenance(stream, entry))
                case _:
                    raise ValueError("Unexpected CpId")
    return result
