import uuid
from esdbclient import EventStoreDBClient, NewEvent
from enum import Enum
from applications import App
from environments import Env

# Connection

DefaultHost = "localhost"
DefaultPort = "2113"

def KurrentUri(host = DefaultHost, port = DefaultPort):
    return "esdb://" + host + ":" + port + "?tls=false"

def CcmClient(host = DefaultHost, port = DefaultPort):
    return EventStoreDBClient(KurrentUri(host, port))

def DeploymentStream(app: App, env: Env) -> str:
    return app.name + "-" + str(app.value) + "-" + env.name

GlobalClient = CcmClient()

PayrollDevStream = DeploymentStream(App.Payroll, Env.DEV)
TimecardProdStream = DeploymentStream(App.Timecard, Env.PROD)