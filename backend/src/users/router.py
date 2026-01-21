import logging
from starlette import status
from fastapi import APIRouter, HTTPException
from src.auth.dependencies import CurrentUser
from src.auth.service import verify_password, get_password_hash
from src.database.core import DB_Session
from src.users.schemas import UserUpdateRequest, CurrentUserResponse, ChangePasswordRequest

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/users", tags=['user'])

@router.get("/me", response_model=CurrentUserResponse)
def get_user(user: CurrentUser):
    return CurrentUserResponse.model_validate(user)


@router.patch("/me", response_model=CurrentUserResponse)
def update_user(update_info: UserUpdateRequest, user: CurrentUser, db: DB_Session):
    """
    Basically, if a field exists, then update it. In SQLAlchemy, you can just modify the ORM object and commit
    the changes and it will reflect itself within the database
    """
    try:
        for field, value in update_info.model_dump(exclude_unset=True).items():
            setattr(user, field, value)
        
        db.commit()
        db.refresh(user)

        logger.info(f"User {user.email} has been successfully updated")
        return CurrentUserResponse.model_validate(user)
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to update user {user.email} | Error: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to Update User")


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user: CurrentUser, db: DB_Session):
    db.delete(user)
    db.commit()

    logger.info(f"User {user.email} has been successfully deleted")


@router.patch("/me/change-password", status_code=status.HTTP_204_NO_CONTENT)
def change_password(pwd_info: ChangePasswordRequest, user: CurrentUser, db: DB_Session):
    """ 
    Verify the old password, then update with the new password. 
    """

    try:
        if not verify_password(plain_password=pwd_info.current_password, hashed_password=user.password_hash): # type: ignore
            logger.info(f"Failed to change password for user {user.email}. Incorrect Password")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Current Password is Incorrect")
        
        # Create a new password hash using the new password
        new_pwd_hash = get_password_hash(password=pwd_info.new_password)
        user.password_hash = new_pwd_hash # type: ignore
        user.token_version += 1 # type: ignore

        db.commit()
        logger.info(f"Password for user {user.email} successfully changed")

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error changing password for user {user.email}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unable to change password at this time")


