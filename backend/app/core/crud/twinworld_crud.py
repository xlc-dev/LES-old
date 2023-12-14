from sqlmodel import Session, select

from app.core.crud.base import CRUDBase
from app.core.models.twinworld_model import TwinWorld
from app.core.schemas.twinworld_schema import TwinWorldCreate, TwinWorldUpdate


class CRUDTwinWorld(CRUDBase[TwinWorld, TwinWorldCreate, TwinWorldUpdate]):
    def get_by_name(self, *, session: Session, name: str):
        return session.exec(
            select(TwinWorld).where(TwinWorld.name == name)
        ).first()


twinworld_crud = CRUDTwinWorld(TwinWorld)
