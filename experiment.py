from utils import CreateCOAssessedEvent
from utils import CreatePredicateAssessedEvent
from utils import DeploymentStream, Application, Environment

#evidence = "some data"
#print(CreateCOAssessedEvent(False, "CCV", 2, evidence))
#print(CreatePredicateAssessedEvent(True, "CCV", 1, 1))

print(DeploymentStream(Application.Payroll, Environment.DEV))
