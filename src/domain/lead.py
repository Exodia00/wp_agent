from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

# todo: Change the Lead usage to use the new property names

@dataclass(slots=True)
class Lead:
    id: Optional[int] = None
    num: str = field(default="")
    phone_id: str = field(default="")
    state: Optional[str] = None
    started_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None
    in_casa: Optional[bool] = None
    service: Optional[str] = None
    activity: Optional[str] = None
    is_organic: Optional[bool] = None
    lang: Optional[str] = None

