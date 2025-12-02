# Payroll application for demo

from controlprocedurepolicy import ReportControlState, UpdatePolicy
from utils import ControlStream, PolicyStream, LoadConfig
import sys
from applications import App
from environments import Env
from VerifierTrustworthinessPredicate import VerifierTrustworthiness as vt
from predicates import Mode, Predicate
from controlprocedures import ControlProcedure
from controlobjectives import ControlObjective
from controlobjectiveenums import ControlObjectiveDomain, VerifierControlObjectives
import threading
from appdeployment import AppControls, AppPolicies
import time

def main(args):
    LoadConfig('payroll.config')

    if (len(sys.argv) != 2):
        print("Usage: payrollapp DeploymentId e.g. payrollapp 1234")
        return

    # Application-global control estate
    # Control procedures
    cpDict: dict[int, ControlProcedure] = {}
    # Predicates
    predList: list[Predicate] = []
    # Control objectives
    coList: list[ControlObjective] = []

    controlStream=ControlStream(app=App.Payroll, env=Env.DEV, depId=sys.argv[1])
    policyStream=PolicyStream(env=Env.DEV, unittest=True)

    # Set up the control estate

    vtp = vt(controlStream, Mode.Firmwide)
    predList.append(vtp)
    CO_CCV_1 = ControlObjective(
        coDomain=ControlObjectiveDomain.ConfidentialComputingVerifier.value,
        coId=VerifierControlObjectives.VerifierTrustworthiness.value,
        stream=controlStream,
        predIds=[vtp.PredId()])
    coList.append(CO_CCV_1)

    print("--- Starting policy event handling ---")

    stop_event = threading.Event()

    appPolicies = AppPolicies(
        policyStream=policyStream,
        controlStream=controlStream,
        cpDict=cpDict,
        stop=stop_event)
    policiesThread=threading.Thread(target=appPolicies.loop)
    policiesThread.start()

    print("--- Starting control event handling ---")

    appControls = AppControls(
        controlStream=controlStream,
        preds=predList,
        cos=coList,
        stop=stop_event)
    controlsThread=threading.Thread(target=appControls.loop)
    controlsThread.start()

    time.sleep(2)
    input(">>> Press Enter to roll out a control assessment policy >>>")
    UpdatePolicy(policyStream, "payroll.expected")

    time.sleep(2)
    print("--- Policy loaded and ready ---")
    input(">>> Press Enter to assess existing control estate >>>")
    ReportControlState("payroll.actual", cpDict)

    time.sleep(2)
    print("--- Existing control estate assessed ---")
    input(">>> Press Enter to update control estate with fixes and re-assess >>>")
    ReportControlState("payroll.fixed", cpDict)

    time.sleep(2)
    print("--- Fixed control estate assessed ---")
    input(">>> Press Enter to roll out a new policy and see the impact >>>")
    UpdatePolicy(policyStream, "payroll.newexpected")

    time.sleep(2)
    ReportControlState("payroll.fixed", cpDict)

    time.sleep(2)
    input(">>> Press Enter to fix remaining issues and re-assess >>>")
    ReportControlState("payroll.newfixed", cpDict)

    time.sleep(2)
    input(">>> Hit ^C to stop event handling and exit >>>")

    stop_event.set()
    controlsThread.join()
    policiesThread.join()

    return

if __name__ == "__main__":
    main(sys.argv[1:])
