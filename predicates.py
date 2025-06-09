from __future__ import annotations # allows passing class objects to class member functions
from esdbclient import NewEvent, StreamState
from enum import Enum
from controlprocedures import ControlProcedureCompletionReport
from controlobjectives import ControlObjectiveDomain
from eventtypes import PredicateAssessed
from typing import List
from utils import GlobalClient
import json

#
# Predicate Helpers
#

class AssessmentIndicator(Enum):
    Unknown = -1
    Failed = 0
    Succeeded = 1

class Mode(Enum):
    SaaS = 0
    Firmwide = 1
    RollYourOwn = 2

def PredicateIdentifier(coDomain: str, coId: int, predId: int) -> str:
    return coDomain + "-" + str(coId) + "-" + str(predId)

class PredicateAssessmentReport:
    __coDomain: int
    __coId: int
    __predId: int
    __incomplete: List[int]
    __complete: dict[int, ControlProcedureCompletionReport]

    def __init__(self, coDomain: int, coId: int, predId: int, incomplete: List[int], complete: dict[int, ControlProcedureCompletionReport]):
        self.__coDomain = coDomain
        self.__coId = coId
        self.__predId = predId
        self.__incomplete = incomplete
        self.__complete = complete

    def toDict(self) -> dict:
        return {
            "coDomain": self.__coDomain,
            "coId": self.__coId,
            "predId": self.__predId,
            "incomplete": self.__incomplete,
            "complete": self.__complete}
    
    def toJson(self) -> str:
        return json.dumps(self.toDict())
        # return json.dumps(self, default=lambda o: o.__dict__)
    
    @staticmethod
    def fromJson(encoding: str) -> PredicateAssessmentReport:
        decoding = json.loads(encoding)
        return PredicateAssessmentReport(
            coDomain=decoding["coDomain"],
            coId=decoding["coId"],
            predId=decoding["predId"],
            incomplete=decoding["incomplete"],
            complete=decoding["complete"])

class Predicate:
    __coDomain: ControlObjectiveDomain
    __coId: int
    __predId: int
    __stream: str
    __incomplete: List[int]
    __complete: dict[int, ControlProcedureCompletionReport]

    def __init__(self, coDomain: int, coId: int, predId: int, stream: int, cpIds: List[int]):
        self.__coDomain = coDomain
        self.__coId = coId
        self.__predId = predId
        self.__stream = stream
        self.__complete = {}
        self.__incomplete = []
        for cpId in cpIds:
            # Check for duplicates
            assert not (cpId in self.__incomplete)
            self.__incomplete.append(cpId)

    # A Predicate is assessed as:
    #  - Succeeded iff all individual results are Succeeded
    #  - Failed if at least one individual result is Failed
    #  - Unknown otherwise
    def PredicateAssessment(self) -> AssessmentIndicator:
        for key in self.__complete.keys():
            value = self.__complete[key]
            assert isinstance(value, ControlProcedureCompletionReport)
            if not value.result.isSuccessful():
                # One Failed -- everything Failed
                return AssessmentIndicator.Failed
            else:
                # Continue iterating; maybe something else Failed
                continue
        if self.__incomplete.count > 0:
            return AssessmentIndicator.Unknown
        else:
            return AssessmentIndicator.Succeeded

    # When a Control Procedure completes, checks to see if Predicate can be assessed (meaning
    # that either at least CP failed, or all have succeeded) and report that if so
    def HandleControlProcedureCompletion(self, completion: ControlProcedureCompletionReport):
        cpId = completion.cpId
        if not (cpId in self.__incomplete) and \
            not (cpId in self.__complete.keys()):
            # This is not one of the Control Procedures this Predicate is interested in
            return
        if cpId in self.__incomplete:
            self.__incomplete.remove(cpId)
        self.__complete[cpId] = completion
        if self.PredicateAssessment() != AssessmentIndicator.Unknown:
            # The assessment state is no longer unknown: can inform the Control Objective now
            assessmentReport = PredicateAssessmentReport(
                coDomain=self.__coDomain,
                coId=self.__coId,
                predId=self.__predId,
                incomplete=self.__incomplete,
                complete=self.__complete)
            GlobalClient.append_to_stream(
                stream_name=self.__stream,
                events=NewEvent(
                    type=PredicateAssessed,
                    data=assessmentReport.toJson().encode('utf-8')),
                    current_version=StreamState.ANY)

