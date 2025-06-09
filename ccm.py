# Continuous Control Monitoring Main Loop

from utils import GlobalClient
from eventtypes import ControlObjectiveFailed, ControlObjectiveAchieved, PredicateAssessed, ControlProcedureCompleted

def HandleControlObjectiveFailedEvent(data: str):
    print(data)
    return

def HandleControlObjectiveAchievedEvent(data: str):
    print(data)
    return

def HandlePredicateAssessedEvent(data: str):
    print(data)
    return

with GlobalClient.subscribe_to_all() as subscription:
    for event in subscription:
        print("Encountered event: " + event.type + " " + event.data.decode())
        if event.type == ControlObjectiveFailed:
            HandleControlObjectiveFailedEvent(event.data.decode())
        elif event.type == ControlObjectiveAchieved:
            HandleControlObjectiveAchievedEvent(event.data.decode())
        elif event.type == PredicateAssessed:
            HandlePredicateAssessedEvent(event.data.decode())


