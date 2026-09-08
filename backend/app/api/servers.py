from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.database.connection import get_db
from app.models.server import Server
from app.models.user import User
from app.schemas.server import (
    ServerCreate,
    ServerResponse,
    ServerUpdate,
)


router = APIRouter(
    prefix="/api/servers",
    tags=["Servers"],
)


@router.get(
    "",
    response_model=list[ServerResponse],
)
def list_servers(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    return (
        db.query(Server)
        .order_by(Server.id.desc())
        .all()
    )


@router.post(
    "",
    response_model=ServerResponse,
)
def create_server(
    server_data: ServerCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    existing = (
        db.query(Server)
        .filter(
            Server.hostname == server_data.hostname
        )
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=409,
            detail="Hostname already exists",
        )

    server = Server(**server_data.model_dump())

    db.add(server)
    db.commit()
    db.refresh(server)

    return server


@router.get(
    "/{server_id}",
    response_model=ServerResponse,
)
def get_server(
    server_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    server = (
        db.query(Server)
        .filter(Server.id == server_id)
        .first()
    )

    if not server:
        raise HTTPException(
            status_code=404,
            detail="Server not found",
        )

    return server


@router.put(
    "/{server_id}",
    response_model=ServerResponse,
)
def update_server(
    server_id: int,
    server_data: ServerUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    server = (
        db.query(Server)
        .filter(Server.id == server_id)
        .first()
    )

    if not server:
        raise HTTPException(
            status_code=404,
            detail="Server not found",
        )

    updates = server_data.model_dump(exclude_unset=True)

    if "hostname" in updates and updates["hostname"] != server.hostname:
        duplicate = (
            db.query(Server)
            .filter(
                Server.hostname == updates["hostname"],
                Server.id != server.id,
            )
            .first()
        )
        if duplicate:
            raise HTTPException(
                status_code=409,
                detail="Hostname already exists",
            )

    for field, value in updates.items():
        setattr(server, field, value)

    db.commit()
    db.refresh(server)

    return server


@router.delete("/{server_id}")
def delete_server(
    server_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    server = (
        db.query(Server)
        .filter(Server.id == server_id)
        .first()
    )

    if not server:
        raise HTTPException(
            status_code=404,
            detail="Server not found",
        )

    server.is_active = False

    db.commit()

    return {
        "message": "Server deactivated successfully"
    }