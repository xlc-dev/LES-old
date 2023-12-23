from sqlmodel import Session, select

from app.core.crud.base import CRUDBase
from app.core.models.appliance_model import (
    Appliance,
    ApplianceTimeWindow,
    ApplianceCreate,
    ApplianceTimeWindowCreate,
    ApplianceUpdate,
    ApplianceTimeWindowUpdate,
    ApplianceTimeDaily,
    ApplianceTimeDailyCreate,
    ApplianceTimeDailyUpdate,
    ApplianceTimeNoEnergyDaily,
    ApplianceTimeNoEnergyDailyCreate,
    ApplianceTimeNoEnergyDailyUpdate,
)


class CRUDAppliance(CRUDBase[Appliance, ApplianceCreate, ApplianceUpdate]):
    pass


class CRUDApplianceTimeDaily(
    CRUDBase[
        ApplianceTimeDaily, ApplianceTimeDailyCreate, ApplianceTimeDailyUpdate
    ]
):
    def get_appliance_time_daily(
        self, *, session: Session, appliance_id: int, day: int
    ):
        return session.exec(
            select(ApplianceTimeDaily)
            .where(ApplianceTimeDaily.day == day)
            .where(ApplianceTimeDaily.appliance_id == appliance_id)
        ).first()

    def get_non_empty_timewindow(self, *, session: Session):
        return session.exec(
            select(ApplianceTimeDaily).where(
                ApplianceTimeDaily.bitmap_plan != 0
            )
        ).first()

    def get_filled_appliance_time_daily(self, *, session: Session):
        return session.exec(
            select(ApplianceTimeDaily).where(
                ApplianceTimeDaily.bitmap_plan != 0
            )
        ).all()


class CRUDAppliancTimeNoEnergyDaily(
    CRUDBase[
        ApplianceTimeNoEnergyDaily,
        ApplianceTimeNoEnergyDailyCreate,
        ApplianceTimeNoEnergyDailyUpdate,
    ]
):
    def get_appliance_time_no_energy_daily(
        self, *, session: Session, appliance_id: int, day: int
    ):
        return session.exec(
            select(ApplianceTimeNoEnergyDaily)
            .where(ApplianceTimeNoEnergyDaily.day == day)
            .where(ApplianceTimeNoEnergyDaily.appliance_id == appliance_id)
        ).first()


class CRUDApplianceTimeWindow(
    CRUDBase[
        ApplianceTimeWindow,
        ApplianceTimeWindowCreate,
        ApplianceTimeWindowUpdate,
    ]
):
    pass


appliance_crud = CRUDAppliance(Appliance)
appliance_time_daily_crud = CRUDApplianceTimeDaily(ApplianceTimeDaily)
appliance_time_no_energy_daily_crud = CRUDAppliancTimeNoEnergyDaily(
    ApplianceTimeNoEnergyDaily
)
appliance_time_window_crud = CRUDApplianceTimeWindow(ApplianceTimeWindow)
