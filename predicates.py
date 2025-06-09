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
    __completions: dict[int, ControlProcedureCompletionReport]

    def __init__(self, coDomain: int, coId: int, predId: int, completions: dict[int, ControlProcedureCompletionReport]):
        self.__coDomain = coDomain
        self.__coId = coId
        self.__predId = predId
        self.__completions = completions

    def toDict(self) -> dict:
        return {
            "coDomain": self.__coDomain,
            "coId": self.__coId,
            "predId": self.__predId,
            "completions": self.__completions}
    
    def toJson(self) -> str:
        return json.dumps(self.toDict())
    
    @staticmethod
    def fromJson(encoding: str) -> PredicateAssessmentReport:
        decoding = json.loads(encoding)
        return PredicateAssessmentReport(
            coDomain=decoding["coDomain"],
            coId=decoding["coId"],
            predId=decoding["predId"],
            completions=decoding["completions"])

class Predicate:
    __coDomain: ControlObjectiveDomain
    __coId: int
    __predId: int
    __stream: str
    __completions: dict

    def __init__(self, coDomain: int, coId: int, predId: int, stream: int, cpIds: List[int]):
        self.__coDomain = coDomain
        self.__coId = coId
        self.__predId = predId
        self.__stream = stream
        self._cpIds = cpIds
        self.__completions = {}
        for cpId in cpIds:
            # Check for duplicates
            assert not (cpId in self.__completions.keys())
            self.__completions[cpId] = None # Insert a placeholder without a value

    # A Predicate is assessed as:
    #  - Succeeded iff all individual results are Succeeded
    #  - Failed if at least one individual result is Failed
    #  - Unknown otherwise
    def PredicateAssessment(self) -> AssessmentIndicator:
        indicator = AssessmentIndicator.Succeeded
        for key in self.__completions.keys():
            value = self.__completions[key]
            assert value == None or isinstance(value, ControlProcedureCompletionReport)
            if value == None:
                indicator = AssessmentIndicator.Unknown
                # Continue iterating, maybe something Failed
            elif not value.result.isSuccessful():
                indicator = AssessmentIndicator.Failed
                # One Failed -- everything Failed
                break
            # otherwise completion is successful; continue iterating
        return indicator

    # When a Control Procedure completes, checks to see if Predicate can be assessed (meaning
    # that either at least CP failed, or all have succeeded) and report that if so
    def HandleControlProcedureCompletion(self, completion: ControlProcedureCompletionReport):
#        if self.__completions[completion.cpId] == None:
#            # This is not one of the Control Procedures this Predicate is interested in
#            return
        self.__completions[completion.cpId] = completion
        if self.PredicateAssessment() != AssessmentIndicator.Unknown:
            # The assessment state is no longer unknown: can inform the Control Objective now
            assessmentReport = PredicateAssessmentReport(
                coDomain=self.__coDomain,
                coId=self.__coId,
                predId=self.__predId,
                completions=self.__completions)
            GlobalClient.append_to_stream(
                stream_name=self.__stream,
                events=NewEvent(
                    type=PredicateAssessed,
                    data=assessmentReport.toJson().encode('utf-8')),
                    current_version=StreamState.ANY)

