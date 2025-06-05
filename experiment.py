from predicates import CreatePredicateFailedEvent, CreatePredicateSucceededEvent
from utils import DeploymentStream
from utils import CcmClient
from esdbclient import StreamState
from applications import App
from environments import Env
from controlobjectives import ControlObjectiveDomain

#evidence = "some data"
#print(CreateCOAssessedEvent(False, "CCV", 2, evidence))
#print(CreatePredicateAssessedEvent(True, "CCV", 1, 1))

#print(DeploymentStream(Application.Payroll, Environment.DEV))

predicateFailedEvent = CreatePredicateFailedEvent(ControlObjectiveDomain.ConfidentialComputingVerifier, 1, 1, 12, "Expired Certificate")
predicateSucceededEvent = CreatePredicateSucceededEvent("RP", 2, 2)

PayrollDeploymentStream = DeploymentStream(App.Payroll, Env.DEV)
client = CcmClient()
client.append_to_stream(
    PayrollDeploymentStream,
    events=[predicateFailedEvent, predicateSucceededEvent],
    current_version=StreamState.ANY
)
