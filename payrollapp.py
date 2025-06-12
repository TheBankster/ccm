# Payroll application for demo

from controlprocedurepolicy import ReadPolicy, ReadActual
from utils import DemoStream, LoadConfig
import sys
from applications import App
from environments import Env
from VerifierTrustworthinessPredicate import VerifierTrustworthiness as vt
from predicates import Mode, Predicate
from controlprocedures import ControlProcedure, ControlProcedureState
from controlobjectives import ControlObjective
from controlobjectiveenums import ControlObjectiveDomain
import threading
from appdeployment import AppControls

def main(args):
    LoadConfig('payroll.config')

    cpDict: dict[int, ControlProcedure]
    if (len(sys.argv) != 2):
        print("Usage: payrollapp DeploymentId e.g. payrollapp 1234")
        return
    appStream=DemoStream(App.Payroll, sys.argv[1], Env.DEV)

    # Create the control estate: CPs, Predicates, COs...
    cpDict = ReadPolicy(appStream, "payroll.expected")
    vtp = vt(appStream, Mode.Firmwide)
    preds: list[Predicate] = []
    preds.append(vtp)
    co1 = ControlObjective(
        coDomain=ControlObjectiveDomain.ConfidentialComputingVerifier.value,
        coId=1,
        stream=appStream,
        predIds=[vtp.PredId()])
    cos: list[ControlObjective] = []
    cos.append(co1)

    print("--- Starting event processing loop ---")

    stop_event = threading.Event()
    deployment = AppControls(
        stream=appStream,
        cps=cpDict,
        preds=preds,
        cos=cos,
        stop=stop_event)
    thread=threading.Thread(target=deployment.loop)
    thread.start()

    input("--- Press any key to assess existing control estate ---")

    actualDict = ReadActual(filename="payroll.actual")
    for key in actualDict.keys():
        cp: ControlProcedure = cpDict[key]
        actualState: ControlProcedureState = actualDict[key]
        cp.ReportControlProcedureState(actualState)

    print("--- Existing control estate assessed ---")
    input("--- Press any key to update control estate with fixes and re-assess ---")

    fixedDict = ReadActual(filenae="payroll.fixed")
    for key in fixedDict.keys():
        cp: ControlProcedure = cpDict[key]
        fixedState: ControlProcedureState = fixedDict[key]
        cp.ReportControlProcedureState(fixedState)

    # input("Press any key to roll out a new policy and see the impact:")

    input("Press any key to stop event processing loop and exit:")
    stop_event.set()
    thread.join()

    return

if __name__ == "__main__":
    main(sys.argv[1:])
