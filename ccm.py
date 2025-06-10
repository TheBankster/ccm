# Continuous Control Monitoring Main Loop

from utils import GlobalClient
from eventtypes import ControlObjectiveAssessed

def HandleControlObjectiveAssessedEvent(data: str):
    print(data)
    return

with GlobalClient.subscribe_to_all() as subscription:
    for event in subscription:
        print("Encountered event: " + event.type + " " + event.data.decode())
        if event.type == ControlObjectiveAssessed:
            HandleControlObjectiveAssessedEvent(event.data.decode())

