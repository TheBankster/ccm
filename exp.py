# experimentations go here

from cp1 import ContractualAgreementWithCSP
from utils import UnitTestStream
from controlprocedurepolicy import ReadPolicy

cplist = ReadPolicy(UnitTestStream, "payroll.config")

print(len(cplist))
