from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Self

from domain.enums import State

# todo: Change the Lead usage to use the new property names

# todo: This can be made to contain something like :
"""
lead.isComplete() which should set all the necesssary information for a lead when complete, instead of having upstream do it
"""

# todo: For safety, state and lang should be enums, and validated

# todo: lang can be literal

# todo: __POST_INIT__ validation

@dataclass(slots=True)
class Lead:
    id: Optional[int] = None
    num: str = field(default="")
    phone_id: str = field(default="")
    state: Optional[State] = None       # todo: since it was changed to type State, it might cause isues when saving, the saving method should use the State.value
    started_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None
    in_casa: Optional[bool] = None
    service: Optional[str] = None
    activity: Optional[str] = None
    is_organic: Optional[bool] = None
    lang: Optional[str] = None
    is_complete: bool = False


    def new_from(self, lead: Self) -> Self:
        self.num = lead.num
        self.phone_id = lead.phone_id
        self.lang = lead.lang
        return self

    def start(self):
        self.started_at = datetime.now()
        self.state = State.START

    def complete(self, is_expected: bool):
        self.ended_at = datetime.now()
        self.is_complete = True
        self.state = State.COMPLETE if is_expected else State.UNEXPECTED