from predicates import Predicate, Mode
from controlobjectiveenums import ControlObjectiveDomain, VerifierControlObjectives

VerifierTrustworthinessModeToControlProcedureIdMapping = [\
    [1],    # SaaS
    [2, 4], # Firmwide
    [2, 3]] # Roll Your Own

class VerifierTrustworthiness(Predicate):
    def __init__(self, stream: str, mode: Mode):
        Predicate.__init__(
            self,
            coDomain=ControlObjectiveDomain.ConfidentialComputingVerifier.value,
            coId=VerifierControlObjectives.VerifierTrustworthiness.value,
            predId=1,
            stream=stream,
            cpIds=VerifierTrustworthinessModeToControlProcedureIdMapping[mode.value])

