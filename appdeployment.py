from applications import App
from environments import Env
import eventtypes
from utils import GlobalClient as client, DeploymentStream
from controlprocedures import ControlProcedure
from controlprocedures import ControlProcedureIdentifier as CpId
from controlprocedures import ControlProcedureAssessmentReport as CPAR
from predicates import Predicate
from predicates import PredicateIdentifier as PrId
from predicates import PredicateAssessmentReport as PAR
from controlobjectives import ControlObjective
from controlobjectives import ControlObjectiveIdentifier as CoId
from controlobjectives import ControlObjectiveAssessmentReport as COAR
import threading

class AppControls():
    def __init__(
            self,
            stream: str,
            cps: dict[int, ControlProcedure],
            preds: list[Predicate],
            cos: list[ControlObjective],
            stop: threading.Event):
        self.__stream = stream
        self.__cps = cps
        self.__preds = preds
        self.__cos = cos
        self.__stop = stop

    def AnnounceEventHandling(self, eventname: str):
         print(self.__stream + " is handling " + eventname)

    # TODO: add handling for changing CP policy

    def HandleControlProcedureAssessedEvent(self, report: CPAR):
        print("Handilng Control Procedure Assessment Report for " + CpId(report.cpId))
        for p in self.__preds:
            p.HandleControlProcedureCompletion(completion=report)
        return

    def HandlePredicateAssessedEvent(self, report: PAR):
        print("Handling Predicate Assessment Report for " + PrId(report.coDomain, report.coId, report.predId))
        for c in self.__cos:
            c.HandlePredicateCompletion(completion=report)
        return

    def HandleControlObjectiveAssessedEvent(self, report: COAR):
        coId = CoId(report.coDomain, report.coId)
        print("Handling Control Objectve Assessment Report for " + coId)
        print("Control Objective " + coId + ("Succeeded" if report.success else "Failed"))
        if (not report.success):
            # TODO: print out reasons for failure
            # TODO: send an event alerting failed CP owners
            # TODO: track time to getting offending CPs fixed
            pass
        return

    def loop(self):
        print("--- Started event processing loop ---")
        while not self.__stop.is_set():
            with client.subscribe_to_stream(self.__stream) as sub:
                for event in sub:
                    self.AnnounceEventHandling(event.type)
                    if event.type == eventtypes.ControlProcedureAssessed:
                        self.HandleControlProcedureAssessedEvent(CPAR.fromJson(event.data))
                    elif event.type == eventtypes.PredicateAssessed:
                        self.HandlePredicateAssessedEvent(PAR.fromJson(event.data))
                    elif event.type == eventtypes.ControlObjectiveAssessed:
                        self.HandleControlObjectiveAssessedEvent(COAR.fromJson(event.data))
                    else:
                        print("Unrecognized event type: " + event.type)
                        assert(False)