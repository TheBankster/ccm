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

class AppControls:
    __appName: str
    __envName: str
    __stream: str

    def __init__(
            self,
            app: App,
            env: Env,
            cps: list[ControlProcedure],
            preds: list[Predicate],
            cos: list[ControlObjective]):
        self.__appName = app.name
        self.__envName = env.name
        self.__stream = DeploymentStream(self.__appName, self.__envName, True)
        self.__cps = cps
        self.__preds = preds
        self.__cos = cos

    def AnnounceEventHandling(self, eventname: str):
         print(self.__appName + " is handling " + str(eventname))

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

    def HandleControlProcedureAssessedEvent(self, report: COAR):
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
        with client.subscribe_to_stream(self.__stream) as sub:
            for event in sub:
                self.AnnounceEventHandling(event.type)
                if event.type == eventtypes.ControlProcedureAssessed:
                    self.HandleControlProcedureAssessedEvent(CPAR.fromJson(event.data))
                elif event.type == eventtypes.PredicateAssessed:
                    self.HandlePredicateAssessedEvent(PAR.fromJson(event.data))
                elif event.type == eventtypes.ControlObjectiveAssessed:
                    self.HandleControlProcedureAssessedEvent(COAR.fromJson(event.data))
                else:
                    assert(False)
                    print("Unrecognized event type: " + event.type)