from applications import App
from environments import Env
import eventtypes
from utils import GlobalClient as client, trace
from controlprocedures import ControlProcedure
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
import json

def AnnounceEventHandling(stream: str, eventname: str) -> None:
    trace(stream + " stream is handling " + eventname + " event")

def GetFailingCpsAndOwnersWithEvidence(report: COAR) -> dict[int, tuple[str, dict, dict]]:
    d: dict[int, tuple[str, str, str]] = {}
    #print("========================================")
    #print("Length of report.complete: " + str(len(report.complete)))
    #print("Type of report.complete: " + str(type(report.complete)))
    #print("Report.complete: " + json.dumps(report.complete))
    #print("Report.complete[\"1\"]: " + json.dumps(report.complete["1"]))
    #print("========================================")
    for predkey in report.complete.keys():
        prar = report.complete[predkey]
        #print(json.dumps(prar))
        if not prar["success"]:
            for cpkey in prar["complete"].keys():
                cpar = prar["complete"][cpkey]
                if not cpar["success"]:
                    d[cpar["cpId"]] = (cpar["owner"], cpar["expected"], cpar["actual"])
    assert(len(d) > 0)
    return d    

def DisplayReasonForCoFailure(report: COAR) -> None:
    assert(not report.success)
    print("Control Objective " + CoId(report.coDomain, report.coId) + " Failed:")
    print("Reason(s):")
    reasons = GetFailingCpsAndOwnersWithEvidence(report)
    for cpid in reasons.keys():
        reason = reasons[cpid]
        print("    " + CpId(cpid) + " owned by " + reason[0] + " expected: " + json.dumps(reason[1]) + " actual: " + json.dumps(reason[2]))
    return

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
        for p in self.__preds:
            p.HandleControlProcedureCompletion(completion=report)
        return

    def HandlePredicateAssessedEvent(self, report: PRAR) -> None:
        for c in self.__cos:
            c.HandlePredicateCompletion(completion=report)
        return

    def HandleControlObjectiveAssessedEvent(self, report: COAR) -> None:
        coId = CoId(report.coDomain, report.coId)
        if report.success:
            print("Control Objective " + coId + " Succeeded")
        else:
            DisplayReasonForCoFailure(report)
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
                        self.HandleControlProcedureAssessedEvent(report=CPAR(**json.loads(event.data)))
                    elif event.type == eventtypes.PredicateAssessed:
                        self.HandlePredicateAssessedEvent(report=PRAR(**json.loads(event.data)))
                    elif event.type == eventtypes.ControlObjectiveAssessed:
                        self.HandleControlObjectiveAssessedEvent(report=COAR(**json.loads(event.data)))
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
                        report = ControlProcedureUpdateReport(**json.loads(event.data))
                        self.HandleControlProcedureUpdatedEvent(report)
        print("--- Stopped policy event handling ---")
        return
