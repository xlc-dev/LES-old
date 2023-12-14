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
    pass


appliance_crud = CRUDAppliance(Appliance)
appliance_time_window_crud = CRUDApplianceTimeWindow(ApplianceTimeWindow)
