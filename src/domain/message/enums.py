from enum import Enum


class MessageType(str, Enum):
    BUTTONS = "buttons"
    LIST = "list"
    TEXT = "text"
