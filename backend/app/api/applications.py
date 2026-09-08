from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.database.connection import get_db
from app.models.application import Application
from app.models.user import User
from app.schemas.application import (
    ApplicationCreate,
    ApplicationResponse,
)


router = APIRouter(
    prefix="/api/applications",
    tags=["Applications"],
)


@router.get(
    "",
    response_model=list[ApplicationResponse],
)
def list_applications(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    return (
        db.query(Application)
        .order_by(Application.id.desc())
        .all()
    )


@router.post(
    "",
    response_model=ApplicationResponse,
)
def create_application(
    application_data: ApplicationCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    application = Application(
        **application_data.model_dump()
    )

    db.add(application)
    db.commit()
    db.refresh(application)

    return application