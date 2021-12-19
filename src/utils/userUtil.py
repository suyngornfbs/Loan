from ..config.auth import get_current_active_user
from fastapi import Depends
from ..models.schemasOut import UserOut


def getCurrentUser(current_user: UserOut = Depends(get_current_active_user)):
    return current_user