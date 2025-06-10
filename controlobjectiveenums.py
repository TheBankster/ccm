from enum import Enum

ControlObjectveDomainNames = ["CCV", "RP"]

class ControlObjectiveDomain(Enum):
    ConfidentialComputingVerifier = 1
    ReverseProxy = 2

class VerifierControlObjectives(Enum):
    VerifierTrustworthiness = 1
    VerifierAvailabilityAndPerformance = 2
    VerifierAssetProtection = 3
    VerifierSORConsiderations = 4

class ReverseProxyControlObjectives(Enum):
    ReverseProxyTrustworthiness = 1
    ReverseProxyAvailabilityAndPerformance = 2
    ReverseProxyRegulatoryCompliance = 3
    ReverseProxySORConsiderations = 4

def ControlObjectiveDomainName(domain: ControlObjectiveDomain) -> str:
    return ControlObjectveDomainNames[domain.value - 1]
