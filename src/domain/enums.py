from enum import Enum


class State(str, Enum):
    START = "START"
    GET_LANG = "LANG"
    GET_SERVICE = "SERVICE"
    GET_SERVICE_BV = "SERVICE_BV"
    GET_CITY = "CITY"
    UNEXPECTED = "UNEXPECTED"
    GET_DIM = "DIM"
    GET_DETAILS = "DETAILS"
    GET_ACTIVITY = "ACTIVITY"
    COMPLETE = "COMPLETE"

class Service(str, Enum):
    BV = "srv_bache_vinyl"
    BEACH_FLAG = "srv_beachflag"
    ROLLUP = "srv_rollup"
    X_BANNER = "srv_xbanner"


class MessageOrigin(str, Enum):
    ORGANIC = 1
    AD = 2

# todo: Use wherever language is needed
class Language(str, Enum):
    AR = "ar",
    FR = "fr"
