# Helpers for reading configuration from file

def ReportWrongValueForKey(key: str, v) -> str:
    print("Wrong value for key \"" + key + "\": \"" + str(v) + "\"")

def GetNonEmptyString(d: dict, key: str) -> str:
    s = str(d[key])
    if len(str(s)) == 0:
        raise ValueError(ReportWrongValueForKey(key, s))
    return s

def GetPositiveInt(d: dict, key: str) -> int:
    i = int(d[key])
    if (i <= 0):
        raise ValueError(ReportWrongValueForKey(key, i))
    return i

def GetIntInRange(d: dict, key: str, min: int, max: int) -> int:
    i = int(d[key])
    if i < min or i > max:
        raise ValueError(ReportWrongValueForKey(key, i))
    return i

def GetBool(d: dict, key: str) -> bool:
    s = d[key].upper()
    if (s == "0" or s == "FALSE"):
        b = False
    elif (s == "1" or s == "TRUE"):
        b = True
    else:
        assert(False)
    return b

def GetDict(d: dict, key: str) -> dict:
    r = d[key]
    if not isinstance(r, dict):
        raise ValueError(ReportWrongValueForKey(key, r))
    return r
