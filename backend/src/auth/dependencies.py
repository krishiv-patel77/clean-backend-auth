import logging
from uuid import UUID
from fastapi import Depends, HTTPException
from starlette import status
from fastapi.security import OAuth2PasswordBearer
from src.database.core import DB_Session
from src.auth.service import verify_token
from src.core.config import settings
from src.core.entities import User
from typing import Annotated

logger = logging.getLogger(__name__)

"""
The only job of the OAuth2PasswordBearer is given the Authorization = "Bearer dwiffjlkfmeqf...", it's job is to read that, strip the Bearer away and extract
the access_token. The only reason we use the tokenUrl specified is for documentation purposes, but it is never used
"""
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')
Bearer_Token = Annotated[str, Depends(oauth2_bearer)]       # Basically, Bearer_Token is of type str but it also depends on oauth2_bearer to extract the token from the authorization header

# Dependency function which also depends on the 
def get_current_user(token: Bearer_Token, db: DB_Session) -> User:
    """
    Docstring for get_current_user
    
    :param token: this is another dependency which extracts the bearer token from the authorization header
    :type token: Bearer_Token
    :param db: this is used for querying via the extracted token data to get the full user object
    :type db: DB_Session
    :return: this returns a full reflection of the actual user object stored in the database omitted sensitive details ofcourse like password hash
    :rtype: CurrentUserResponse

    This function should verify the token, extract the user relevant metadata from the token, query the database for all the information about this user,
    populate the CurrentUserResponse object with the data it recieves and return that object
    """
    
    # First verify the access token
    token_data = verify_token(token=token,
                              SECRET_KEY=settings.SECRET_KEY,
                              ALGORITHM=settings.ALGORITHM,
                              refresh=False)
    
    if not token_data:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Failed to fetch current user. Invalid Access Token",
                            headers={"WWW-Authenticate": "Bearer"})
    
    token_id = UUID(token_data['sub'])
    user = db.query(User).filter(User.id == token_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"})
    
    if token_data['token_version'] != user.token_version: 
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token revoked"
        )
    
    # Return the ORM object for internal manipulations
    return user


# This is the object that will be imported and used which depends on get_current_user which essentially extracts the bearer token from the header, verifies it, and return the user data
CurrentUser = Annotated[User, Depends(get_current_user)]



