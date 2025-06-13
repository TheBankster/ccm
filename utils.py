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

Tracing: bool = False

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
    trace("DeploymentStream will be " + result)
    return result

# ControlStream carries control assessment events for an application deployment
def ControlStream(app: App, env: Env, depId: int) -> str:
    result =app.name + "-" + env.name + "-" + str(depId)
    trace("ControlStream will be " + result)
    return result

# PolicyStream carries policy change events for a given environment
def PolicyStream(env: Env, unittest: bool = False) -> str:
    result: str = "ControlStream-"+env.name
    if (unittest):
        result += str(time.monotonic_ns())
    trace("PolicyStream will be " + result)
    return result

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

UnitTestStream = DeploymentStream(App.UnitTest, Env.UAT, unittest=True)
