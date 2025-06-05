# Continuous Control Monitoring Main Loop

from utils import CcmClient
from eventtypes import ControlObjectiveFailed, ControlObjectiveAchieved, PredicateSucceeded, PredicateFailed

client = CcmClient()

def HandleControlObjectiveFailedEvent(data: str):
    print(data)
    return

def HandleControlObjectiveAchievedEvent(data: str):
    print(data)
    return

def HandlePredicateSucceededEvent(data: str):
    print(data)
    return

def HandlePredicateFailedEvent(data: str):
    print(data)
    return

with client.subscribe_to_all() as subscription:
    for event in subscription:
        print("Encountered event: " + event.type + " " + event.data.decode())
        if event.type == ControlObjectiveFailed:
            HandleControlObjectiveFailedEvent(event.data.decode())
        elif event.type == ControlObjectiveAchieved:
            HandleControlObjectiveAchievedEvent(event.data.decode())
        elif event.type == PredicateSucceeded:
            HandlePredicateSucceededEvent(event.data.decode())
        elif event.type == PredicateFailed:
            HandlePredicateFailedEvent(event.data.decode())


