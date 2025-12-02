#
# Control Objective Helpers
#

from __future__ import annotations # allows passing class objects to class member functions
from typing import final
import json
from assessmentindicator import AssessmentIndicator
from kurrentdbclient import NewEvent, StreamState
from eventtypes import ControlObjectiveAssessed
from controlobjectiveenums import ControlObjectveDomainNames
from predicates import PredicateAssessmentReport
from utils import GlobalClient

# Control Objective Event Creation

# e.g. CO-CCV-1
def ControlObjectiveIdentifier(domain: int, id: int) -> str:
    ControlObjectivePrefix = "CO-"
    return ControlObjectivePrefix + ControlObjectveDomainNames[domain-1] + "-" + str(id)

class ControlObjectiveAssessmentReport:
    coDomain: int
    coId: int
    incomplete: list[int]
    complete: dict[int, PredicateAssessmentReport]
    success: bool

    def __init__(self, coDomain: int, coId: int, incomplete: list[int], complete: dict[int, PredicateAssessmentReport], success: bool):
        self.coDomain = coDomain
        self.coId = coId
        self.incomplete = incomplete
        self.complete = complete
        self.success = success

    @final
    def toJson(self) -> str:
        return json.dumps(self.__dict__, default=lambda o: o.__dict__)
    """
    @staticmethod
    def fromJson(encoding: str) -> ControlObjectiveAssessmentReport:
        decoding = json.loads(encoding)
        return ControlObjectiveAssessmentReport(
            coDomain=decoding["coDomain"],
            coId=decoding["coId"],
            incomplete=decoding["incomplete"],
            complete=decoding["complete"],
            success=decoding["success"])
    """
class ControlObjective:
    __coDomain: int
    __coId: int
    __stream: str
    __complete: dict[int, PredicateAssessmentReport]
    __incomplete: list[int]
    
    def __init__(self, coDomain: int, coId:int, stream: str, predIds: list[int]):
        self.__coDomain = coDomain
        self.__coId = coId
        self.__stream = stream
        self.__complete = {}
        self.__incomplete = []
        for predId in predIds:
            # Check for duplicates
            assert not (predId in self.__incomplete)
            self.__incomplete.append(predId)
        
    # A Control Objective is assessed as:
    #  - Succeeded iff all individual precdicates are Succeeded
    #  - Failed if at least one individual predicate is Failed
    #  - Unknown otherwise
    # Derived Control Objectives can change the behavior
    def ControlObjectiveAssessment(self) -> AssessmentIndicator:
        for key in self.__complete.keys():
            value = self.__complete[key]
            assert isinstance(value, PredicateAssessmentReport)
            if not value.success:
                # One Failed -- everything Failed
                return AssessmentIndicator.Failed
            else:
                # Continue iterating; maybe something else Failed
                continue
        if len(self.__incomplete) > 0:
            return AssessmentIndicator.Unknown
        else:
            return AssessmentIndicator.Succeeded

    # When a Predicate completes, checks to see if Predicate can be assessed (meaning
    # that either at least one Predicate failed, or all have succeeded) and report that if so
    def HandlePredicateCompletion(self, completion: PredicateAssessmentReport):
        if (self.__coDomain != completion.coDomain) or \
            (self.__coId != completion.coId):
            # Predicate does not correspond to this Control Objective
            return
        predId = completion.predId
        if not (predId in self.__incomplete) and \
            not (predId in self.__complete.keys()):
            # This is not one of the Predicates this Control Objective is interested in
            return
        if predId in self.__incomplete:
            self.__incomplete.remove(predId)
        self.__complete[predId] = completion
        assessment = self.ControlObjectiveAssessment()
        if assessment != AssessmentIndicator.Unknown:
            # The assessment state is no longer unknown: can report Control Objective state now
            assessmentReport = ControlObjectiveAssessmentReport(
                coDomain=self.__coDomain,
                coId=self.__coId,
                incomplete=self.__incomplete,
                complete=self.__complete,
                success=(assessment == AssessmentIndicator.Succeeded))
            GlobalClient.append_to_stream(
                stream_name=self.__stream,
                events=NewEvent(
                    type=ControlObjectiveAssessed,
                    data=assessmentReport.toJson().encode('utf-8')),
                    current_version=StreamState.ANY)
            
    def Identifier(self) -> str:
        return ControlObjectiveIdentifier(self.__coDomain, self.__coId)
