# Payroll application for demo

from controlprocedurepolicy import ReadPolicy
from utils import DemoStream
import sys
from applications import App
from environments import Env
from VerifierTrustworthinessPredicate import VerifierTrustworthiness as vt
from predicates import Mode, Predicate
from controlobjectives import ControlObjective
from controlobjectiveenums import ControlObjectiveDomain
import threading
from appdeployment import AppControls

def main(args):
    print(len(sys.argv))
    print(sys.argv[0])
    input("foo")
    if (len(sys.argv) != 2):
        print("Usage: payrollapp DeploymentId e.g. payrollapp 1234")
        return
    stream=DemoStream(App.Payroll, sys.argv[1], Env.DEV)

    # Create the control estate: CPs, Predicates, COs...
    cpdict = ReadPolicy(stream, "payroll.config")
    vtp = vt(stream, Mode.Firmwide)
    preds: list[Predicate] = []
    preds.append(vtp)
    co1 = ControlObjective(
        coDomain=ControlObjectiveDomain.ConfidentialComputingVerifier,
        coId=1,
        stream=stream,
        predIds=[vtp.PredId()])
    cos: list[ControlObjective] = []
    cos.append(co1)

    input("Press any key to start event processing loop:")

    stop_event = threading.Event()
    appControls = AppControls(
        cps=cpdict,
        preds=preds,
        cos=cos,
        stop=stop_event) 
    deployment=threading.Thread()
    deployment.start()

    input("Press any key to stop event processing loop and exit:")
    stop_event.set()
    deployment.join()

    return

if __name__ == "__main__":
    main(sys.argv[1:])
