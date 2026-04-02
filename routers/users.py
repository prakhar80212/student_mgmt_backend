from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from schemas import UserOut
from auth_utils import require_admin
import models

router = APIRouter()


@router.get("/", response_model=List[UserOut])
def list_users(
    db: Session = Depends(get_db),
    _: models.User = Depends(require_admin),
):
    """Admin only – list all registered users."""
    return db.query(models.User).order_by(models.User.id).all()
