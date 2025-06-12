import uuid
from esdbclient import EventStoreDBClient
from enum import Enum
from applications import App
from environments import Env
from datetime import date
import time
import configparser

# Connection

DefaultHost = "localhost"
DefaultPort = "2113"

KurrentHost: str = DefaultHost
KurrentPort: int = DefaultPort

Tracing: bool = True

def trace(str):
    if Tracing:
        print(str)

def KurrentUri(host: str = DefaultHost, port: int = DefaultPort):
    return "esdb://" + host + ":" + str(port) + "?tls=false"

def CcmClient(host = KurrentHost, port = KurrentPort):
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

def DemoStream(app: App, depId: int, env: Env) -> str:
    return(app.name + "-" + str(depId) + "-" + env.name)

def LoadConfig(configFile: str):
    config = configparser.ConfigParser()
    config.read(configFile)

    KurrentHost = config['settings'].get('host', DefaultHost)
    KurrentPort = config['settings'].getint('port', DefaultPort)
    Tracing = config['settings'].getboolean('tracing', False)
    print("Tracing is: " + str(Tracing))
    trace("Tracing turned on")
    GlobalClient = CcmClient(KurrentHost, KurrentPort)

GlobalClient = CcmClient(KurrentHost, KurrentPort)

PayrollDevStream = DeploymentStream(App.Payroll, Env.DEV)
TimecardProdStream = DeploymentStream(App.Timecard, Env.PROD)
UnitTestStream = DeploymentStream(App.UnitTest, Env.UAT, unittest=True)
