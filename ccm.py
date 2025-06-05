# Continuous Control Monitoring Main Loop

from utils import CcmClient
from controlobjectives import ControlObjectiveFailed

client = CcmClient()

def HandleControlObjectiveFailedEvent(data: str):
    print(data)
    return

with client.subscribe_to_all() as subscription:
    for event in subscription:
        print("Encountered event: " + event.type + " " + event.data.decode())
        if event.type == ControlObjectiveFailed:
            HandleControlObjectiveFailedEvent(event.data.decode())

