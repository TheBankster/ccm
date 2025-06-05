from utils import CreateCOAssessedEvent
from utils import CreatePredicateAssessedEvent
from utils import CreatePredicateFailedEvent, CreatePredicateSucceededEvent
from utils import DeploymentStream, Application, Environment
from utils import CcmClient
from esdbclient import StreamState

#evidence = "some data"
#print(CreateCOAssessedEvent(False, "CCV", 2, evidence))
#print(CreatePredicateAssessedEvent(True, "CCV", 1, 1))

#print(DeploymentStream(Application.Payroll, Environment.DEV))

predicateFailedEvent = CreatePredicateFailedEvent("CCV", 1, 1, 12, "Expired Certificate")
predicateSucceededEvent = CreatePredicateSucceededEvent("RP", 2, 2)

PayrollDeploymentStream = DeploymentStream(Application.Payroll, Environment.DEV)
client = CcmClient()
client.append_to_stream(
    PayrollDeploymentStream,
    events=[predicateFailedEvent, predicateSucceededEvent],
    current_version=StreamState.ANY
)
