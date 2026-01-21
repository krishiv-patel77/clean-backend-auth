from pydantic import BaseModel
from typing import Optional
from datetime import datetime 

class UserUpdateRequest(BaseModel):
    """ This is the request model for Put requests so it must have all data avaliable """
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[str]
    university: Optional[str]

class CurrentUserResponse(BaseModel):
    first_name: str
    last_name: str
    email: str
    university: Optional[str]      # University is an optional field
    time_created: datetime

class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str