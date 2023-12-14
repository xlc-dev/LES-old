from sqlmodel import Session, select

from app.core.crud.base import CRUDBase
from app.core.models.household_model import (
    Household,
    HouseholdCreate,
    HouseholdUpdate,
)


class CRUDHousehold(CRUDBase[Household, HouseholdCreate, HouseholdUpdate]):
    def get_by_twinworld(self, *, session: Session, id: int):
        return session.exec(
            select(Household).where(Household.twinworld_id == id)
        ).all()


household_crud = CRUDHousehold(Household)
