import logging
from uuid import uuid4, UUID
from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status
from src.auth.schemas import RegisterUserRequest, Token, RefreshTokenRequest
from src.auth.service import get_password_hash, authenticate_user, create_token, verify_token
from src.database.core import DB_Session
from src.core.entities import User
from src.core.config import settings

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=['auth'])       # tags are just for documentation purposes for grouping together all auth edpts in docs together

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(db: DB_Session, register_user_data: RegisterUserRequest) -> None:
    """
    Docstring for register
    
    :param db: used for saving the new user
    :type db: DB_Session -> Dependency which automatically starts and yields the DB session for usage and then handles closing it
    :param register_user_data: provides the data to register for the user as per the defined model
    :type register_user_data: RegisterUserRequest

    This function is called by the frontend upon a new user being registered into the system. Note, this function simply acknoledges that a new 
    user has been registered, it does not issues tokens. This is done via explicit login. 
    """
    try:
        # Check if user already exists
        existing_user = db.query(User).filter(User.email == register_user_data.email).first()
        if existing_user:
            logger.error("Failed to Register User. User already exists.")
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User with this email already exists")     # 409 conflict indicates a valid request but it conflicts with the existing state of the application

        # Create a new user entity
        user = User(
            id = uuid4(),
            email=register_user_data.email,
            first_name=register_user_data.first_name,
            last_name=register_user_data.last_name,
            password_hash=get_password_hash(register_user_data.password)
        )

        db.add(user)
        db.commit()
        logger.info(f"Successfully registered user: {register_user_data.email}")
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to register user: {register_user_data.email}. Error: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to register user")


@router.post("/token", response_model=Token)
def login(db: DB_Session, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    """
    Docstring for login
    
    :param db: used for retrieving the saved user for password validation
    :type db: DB_Session
    :param form_data: used to securely recieve username and password via OAuth standard format
    :type form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
    :return: returns a Token model which contains the access token, the refresh token, and the type (bearer)
    :rtype: Token

    Now, when calling requests from the frontend, there needs to be authorization in the request headers of all requests made to the backend. 
    """
    try:
        user = authenticate_user(form_data.username, form_data.password, db)

        # If no user is returned, there was either a wrong password or user wasn't found
        if not user:
            logger.warning(f"Failed authentication attempt for email: {form_data.username}")     
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                detail="Incorrect username or password",
                                headers={"WWW-Authenticate": "Bearer"})     # Headers are required for 401 Unauthorized
        
        access_token = create_token(
            email=user.email,  # type: ignore
            user_id=user.id,   # type: ignore
            expiry=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES), # type: ignore
            SECRET_KEY=settings.SECRET_KEY, 
            ALGORITHM=settings.ALGORITHM, 
            refresh=False)
        
        refresh_token = create_token(
            email=user.email,  # type: ignore
            user_id=user.id,   # type: ignore
            expiry=timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES), 
            SECRET_KEY=settings.SECRET_KEY, 
            ALGORITHM=settings.ALGORITHM, 
            refresh=True)

        logger.info(f"Successful login for user: {form_data.username}")
        return Token(access_token=access_token, refresh_token=refresh_token, token_type="bearer")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error during login for {form_data.username}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occurred during login")


@router.post("/refresh", response_model=Token)
def refresh(payload: RefreshTokenRequest) -> Token:
    """
    Docstring for refresh
    
    :param payload: for recieving the data needed to refresh the access token 
    :type payload: RefreshTokenRequest
    :return: a Token object containing the refresh token the user already has along with a new refresh_token
    :rtype: Token

    Note: here, the payload which is of type RefreshTokenRequest only contains the refresh_token but it must be in the body of the request because it is a
    long-lived secret meaning it should not be given out in the headers. It is merely used for refreshing access tokens.
    """

    token_data = verify_token(token=payload.refresh_token, 
                              SECRET_KEY=settings.SECRET_KEY,
                              ALGORITHM=settings.ALGORITHM,
                              refresh=True)
    
    if not token_data:
        logger.warning("Failed to refresh access token. Invalid refresh token.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
            headers={"WWW-Authenticate": "Bearer"})
    
    # If we have a valid refresh_token, then using the token_data, create a new access token
    new_access_token = create_token(email=token_data['sub'],
                                    user_id=UUID(token_data['id']),
                                    expiry=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
                                    SECRET_KEY=settings.SECRET_KEY,
                                    ALGORITHM=settings.ALGORITHM,
                                    refresh=False)
    
    logger.info(f"Successfully refreshed access token for user: {token_data['sub']}")

    return Token(access_token=new_access_token, refresh_token=payload.refresh_token, token_type="bearer")



