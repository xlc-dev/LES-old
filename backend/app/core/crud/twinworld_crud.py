from sqlmodel import Session, select

from app.core.crud.base import CRUDBase
from app.core.models.twinworld_model import (
    TwinWorld,
    TwinWorldCreate,
    TwinWorldUpdate,
)


class CRUDTwinWorld(CRUDBase[TwinWorld, TwinWorldCreate, TwinWorldUpdate]):
    def get_by_name(self, *, session: Session, name: str):
        "Get a single TwinWorld by name"

        return session.exec(
            select(TwinWorld).where(TwinWorld.name == name)
        ).first()


twinworld_crud = CRUDTwinWorld(TwinWorld)
