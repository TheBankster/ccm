# experimentations go here

from utils import UnitTestStream
from controlprocedurepolicy import ReadPolicy

cplist = ReadPolicy(UnitTestStream, "payroll.config")

print(len(cplist))
