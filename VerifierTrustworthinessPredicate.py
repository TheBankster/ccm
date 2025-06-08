from predicates import Predicate, Mode
from controlobjectives import ControlObjectiveDomain, VerifierControlObjectives

VerifierTrustworthinessModeToCPMapping = [\
    [1],    # SaaS
    [2, 4], # Firmwide
    [2, 3]] # Roll Your Own

class VerifierTrustworthiness(Predicate):
    def __init__(self, mode: Mode):
        Predicate.__init__(self, ControlObjectiveDomain.ConfidentialComputingVerifier, VerifierControlObjectives.VerifierTrustworthiness, VerifierTrustworthinessModeToCPMapping[mode])
