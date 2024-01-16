from sqlmodel import Session, select
from sqlalchemy import desc

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

    def get_by_twinworld_sorted_solar_panels(
        self, *, session: Session, id: int
    ):
        return session.exec(
            select(Household)
            .where(Household.twinworld_id == id)
            .order_by(desc(Household.solar_panels))  # type: ignore
        ).all()

    def count_households(self, *, session: Session):
        return session.query(Household).count()

    def get_by_name(self, *, session: Session, name: str):
        return session.exec(
            select(Household).where(Household.name == name)
        ).first()


household_crud = CRUDHousehold(Household)
