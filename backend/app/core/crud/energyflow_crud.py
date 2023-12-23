from sqlmodel import Session, select
from sqlalchemy import func, desc

from app.core.crud.base import CRUDBase
from app.core.models.energyflow_model import (
    EnergyFlow,
    EnergyFlowCreate,
    EnergyFlowUpdate,
)


class CRUDEnergyFlow(CRUDBase[EnergyFlow, EnergyFlowCreate, EnergyFlowUpdate]):
    def get_by_timestamp(self, *, session: Session, timestamp: int):
        return session.exec(
            select(EnergyFlow).where(EnergyFlow.timestamp == timestamp)
        ).first()

    def get_by_solar_produced(self, *, session: Session):
        return session.exec(
            select(EnergyFlow)
            .where(EnergyFlow.solar_produced > 0)
            .order_by(desc(EnergyFlow.solar_produced))  # type: ignore
        ).all()

    def get_start_end_date(self, *, session: Session):
        min_timestamp_query = select(EnergyFlow).filter(
            EnergyFlow.timestamp  # type: ignore
            == session.execute(select(func.min(EnergyFlow.timestamp))).scalar()
        )
        max_timestamp_query = select(EnergyFlow).filter(
            EnergyFlow.timestamp  # type: ignore
            == session.execute(select(func.max(EnergyFlow.timestamp))).scalar()
        )

        results_min_timestamp = session.exec(min_timestamp_query).first()
        results_max_timestamp = session.exec(max_timestamp_query).first()
        return results_min_timestamp, results_max_timestamp


energyflow_crud = CRUDEnergyFlow(EnergyFlow)
