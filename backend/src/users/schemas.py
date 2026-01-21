from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime 

class UserUpdateRequest(BaseModel):
    """ This is the request model for Put requests so it must have all data avaliable """
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    university: Optional[str] = None

class CurrentUserResponse(BaseModel):
    first_name: str
    last_name: str
    email: str
    university: Optional[str]      # University is an optional field
    time_created: datetime

    model_config = ConfigDict(from_attributes=True)

class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str