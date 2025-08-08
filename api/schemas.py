from pydantic import BaseModel, ValidationError
from typing import Literal

class UserEvent(BaseModel):
    """
    Pydantic model for validating incoming user event data.
    """
    type: Literal["deposit", "withdraw"]
    amount: str
    user_id: int
    time: int

def validate_event(api_body):
    try:
        return UserEvent(**api_body)

    except ValidationError as e:
        raise e