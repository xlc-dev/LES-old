from sqlmodel import Session, select

from app.core.crud.base import CRUDBase
from app.core.models.appliance_model import (
    Appliance,
    ApplianceTimeWindow,
    ApplianceCreate,
    ApplianceTimeWindowCreate,
    ApplianceUpdate,
    ApplianceTimeWindowUpdate,
)


class CRUDAppliance(CRUDBase[Appliance, ApplianceCreate, ApplianceUpdate]):
    pass


class CRUDApplianceTimeWindow(
    CRUDBase[
        ApplianceTimeWindow,
        ApplianceTimeWindowCreate,
        ApplianceTimeWindowUpdate,
    ]
):
    def get_by_appliance_id(self, *, session: Session, appliance_id: int):
        return session.exec(
            select(ApplianceTimeWindow).where(
                ApplianceTimeWindow.appliance_id == appliance_id
            )
        ).all()


appliance_crud = CRUDAppliance(Appliance)
appliance_time_window_crud = CRUDApplianceTimeWindow(ApplianceTimeWindow)
