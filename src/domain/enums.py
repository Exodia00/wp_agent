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

