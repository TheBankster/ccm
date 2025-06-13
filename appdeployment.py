from applications import App
from environments import Env
import eventtypes
from utils import GlobalClient as client, trace
from controlprocedures import ControlProcedure, ControlProcedureState
from controlprocedures import ControlProcedureIdentifier as CpId
from controlprocedures import ControlProcedureAssessmentReport as CPAR
from predicates import Predicate
from predicates import PredicateIdentifier as PrId
from predicates import PredicateAssessmentReport as PRAR
from controlobjectives import ControlObjective
from controlobjectives import ControlObjectiveIdentifier as CoId
from controlobjectives import ControlObjectiveAssessmentReport as COAR
from controlprocedurepolicy import ControlProcedureUpdateReport, ControlProcedureFromUpdateReport
import threading

def AnnounceEventHandling(stream: str, eventname: str) -> None:
    trace(stream + " stream is handling " + eventname + " event")

class AppControls():
    __controlStream: str
    __preds: list[Predicate] = []
    __cos: list[ControlObjective] = []
    __stop: threading.Event

    def __init__(
            self,
            controlStream: str,
            preds: list[Predicate],
            cos: list[ControlObjective],
            stop: threading.Event):
        self.__controlStream = controlStream
        self.__preds = preds
        self.__cos = cos
        self.__stop = stop

    def AnnounceEventHandling(self, eventname: str) -> None:
        AnnounceEventHandling(self.__controlStream, eventname)

    def HandleControlProcedureAssessedEvent(self, report: CPAR) -> None:
        trace("Handilng Control Procedure Assessment Report for " + CpId(report.cpId))
        trace("Control Procedure " + CpId(report.cpId) + (" Succeeded" if report.success else " Failed"))
        for p in self.__preds:
            trace("Handing off handling of " + CpId(report.cpId) + " assessment report to Predicate " + p.Identifier())
            p.HandleControlProcedureCompletion(completion=report)
        return

    def HandlePredicateAssessedEvent(self, report: PRAR) -> None:
        trace("Handling Predicate Assessment Report for " + report.PredicateIdentifier())
        for c in self.__cos:
            c.HandlePredicateCompletion(completion=report)
        return

    def HandleControlObjectiveAssessedEvent(self, report: COAR) -> None:
        coId = CoId(report.coDomain, report.coId)
        trace("Handling Control Objectve Assessment Report for " + coId)
        print("Control Objective " + coId + (" Succeeded" if report.success else " Failed"))
        if (not report.success):
            # TODO: print out reasons for failure
            # TODO: send an event alerting failed CP owners
            # TODO: track time to getting offending CPs fixed
            pass
        return

    def loop(self):
        print("--- Started control event handling ---")
        while not self.__stop.is_set():
            with client.subscribe_to_stream(stream_name=self.__controlStream) as sub:
                for event in sub:
                    self.AnnounceEventHandling(event.type)
                    if event.type == eventtypes.ControlProcedureAssessed:
                        self.HandleControlProcedureAssessedEvent(report=CPAR.fromJson(event.data))
                    elif event.type == eventtypes.PredicateAssessed:
                        self.HandlePredicateAssessedEvent(report=PRAR.fromJson(event.data))
                    elif event.type == eventtypes.ControlObjectiveAssessed:
                        self.HandleControlObjectiveAssessedEvent(report=COAR.fromJson(event.data))
                    else:
                        trace("Unrecognized event type: " + event.type)
                        assert(False)
        print("--- Stopped control event handling ---")
        return

class AppPolicies():
    __policyStream: str
    __controlStream: str
    __cpDict: dict[int, ControlProcedure] = {}
    __stop: threading.Event

    def __init__(
            self,
            policyStream: str,
            controlStream: str,
            cpDict: dict[int, ControlProcedure],
            stop: threading.Event):
        self.__policyStream = policyStream
        self.__controlStream = controlStream
        self.__cpDict = cpDict
        self.__stop = stop

    def AnnounceEventHandling(self, eventname: str) -> None:
        AnnounceEventHandling(self.__policyStream, eventname)

    def HandleControlProcedureUpdatedEvent(self, report: ControlProcedureUpdateReport) -> None:
        trace("Handling Control Procedure Updated event")
        cpId = report.cpId
        if cpId in self.__cpDict.keys():
            # TODO: see what can be salvaged from previous state
            # TODO: maybe update owner?
            # TODO: maybe update assessment based on last assessed state?
            pass
        self.__cpDict[cpId] = ControlProcedureFromUpdateReport(self.__controlStream, report)

    def loop(self):
        print("--- Started policy event handling ---")
        while not self.__stop.is_set():
            with client.subscribe_to_stream(stream_name=self.__policyStream) as sub:
                for event in sub:
                    self.AnnounceEventHandling(event.type)
                    if event.type == eventtypes.ControlProcedureUpdated:
                        report = ControlProcedureUpdateReport.fromJson(event.data)
                        self.HandleControlProcedureUpdatedEvent(report)
        print("--- Stopped policy event handling ---")
        return
