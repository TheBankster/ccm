# experimentations go here
from enum import Enum
class AssessmentIndicator(Enum):
    Unknown = -1
    Failed = 0
    Succeeded = 1

def Assessment(items: dict) -> AssessmentIndicator:
        indicator = AssessmentIndicator.Succeeded
        for key in items.keys():
            value = items[key]
            assert value == None or isinstance(value, bool)
            if value == None:
                indicator = AssessmentIndicator.Unknown
                # Continue iterating, maybe something Failed
            elif value == False:
                indicator = AssessmentIndicator.Failed
                # One Failed -- everything Failed
                break
            # otherwise completion is successful; continue iterating
        return indicator

items = {1: True, 3: True, 5: True}
print(str(Assessment(items)))
