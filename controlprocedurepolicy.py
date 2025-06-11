from controlprocedures import ControlProcedure
from cp1 import ContractualAgreementWithCSP, ContractualAgreementWithCSP_CPID
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
                case ContractualAgreementWithCSP_CPID:
                    result.append(ContractualAgreementWithCSP(stream, entry))
    return result
