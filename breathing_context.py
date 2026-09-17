from typing import Optional, List
from pydantic import BaseModel


class BreathingContext(BaseModel):
    state: Optional[str] = None
    goal: Optional[str] = None
    duration: Optional[int] = None
    avoidBreathHolding: bool = False
    breathingPreference: Optional[str] = None
    explicitFields: List[str] = []


def get_missing_breathing_fields(context: BreathingContext):
    missing_fields = []

    if context.state is None:
        missing_fields.append("state")

    if context.goal is None:
        missing_fields.append("goal")

    if context.duration is None:
        missing_fields.append("duration")

    return missing_fields