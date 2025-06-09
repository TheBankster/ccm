import uuid
from esdbclient import EventStoreDBClient
from enum import Enum
from applications import App
from environments import Env
from datetime import date
import time

# Connection

DefaultHost = "localhost"
DefaultPort = "2113"

def KurrentUri(host = DefaultHost, port = DefaultPort):
    return "esdb://" + host + ":" + port + "?tls=false"

def CcmClient(host = DefaultHost, port = DefaultPort):
    return EventStoreDBClient(KurrentUri(host, port))

def DeploymentStream(app: App, env: Env, unittest: bool = False) -> str:
    if unittest:
        # ensure unique id for unit tests
        result = "Unit-Test-Stream-" + str(time.monotonic_ns())
    else:
        result = app.name + "-" + str(app.value) + "-" + env.name
        # for hackathon each day means different stream names
        result += "-" + date.today().isoformat()
    return result

GlobalClient = CcmClient()

PayrollDevStream = DeploymentStream(App.Payroll, Env.DEV)
TimecardProdStream = DeploymentStream(App.Timecard, Env.PROD)
