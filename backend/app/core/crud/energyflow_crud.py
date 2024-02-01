from sqlmodel import Session, select
from sqlalchemy import func

from app.core.crud.base import CRUDBase
from app.core.models.energyflow_model import (
    EnergyFlow,
    EnergyFlowCreate,
    EnergyFlowUpdate,
    EnergyFlowUpload,
    EnergyFlowUploadCreate,
    EnergyFlowUploadUpdate,
)


class CRUDEnergyFlow(CRUDBase[EnergyFlow, EnergyFlowCreate, EnergyFlowUpdate]):
    def get_by_timestamp(self, *, session: Session, timestamp: int):
        "Get a single EnergyFlow by timestamp"

        return session.exec(
            select(EnergyFlow).where(EnergyFlow.timestamp == timestamp)
        ).first()

    def get_by_solar_produced(
        self, *, session: Session, limit: int = 10000, offset: int = 0
    ):
        "Get all EnergyFlow by solar_produced"

        return session.exec(
            select(EnergyFlow)
            .where(EnergyFlow.solar_produced > 0)
            .where(EnergyFlow.id >= offset)
            .where(EnergyFlow.id < offset + limit)
            .order_by(EnergyFlow.solar_produced.desc())  # type: ignore
        ).all()

    def get_all_sorted_by_timestamp(
        self, *, session: Session, id: int, limit: int = 10000, offset: int = 0
    ):
        "Get all EnergyFlow sorted by timestamp"

        return session.exec(
            select(EnergyFlow)
            .where(EnergyFlow.energyflow_upload_id == id)
            .order_by(EnergyFlow.timestamp.asc())  # type: ignore
            .limit(limit)
            .offset(offset)
        ).all()

    def get_start_end_date(self, *, session: Session, id: int):
        "Get the start and end date of the EnergyFlow table"

        min_timestamp_query = (
            select(EnergyFlow)
            .where(EnergyFlow.energyflow_upload_id == id)
            .filter(
                EnergyFlow.timestamp  # type: ignore
                == session.execute(
                    select(func.min(EnergyFlow.timestamp))
                ).scalar()
            )
        )
        max_timestamp_query = (
            select(EnergyFlow)
            .where(EnergyFlow.energyflow_upload_id == id)
            .filter(
                EnergyFlow.timestamp  # type: ignore
                == session.execute(
                    select(func.max(EnergyFlow.timestamp))
                ).scalar()
            )
        )

        results_min_timestamp = session.exec(min_timestamp_query).first()
        results_max_timestamp = session.exec(max_timestamp_query).first()
        return results_min_timestamp, results_max_timestamp


class EnergyFlowUploadCRUD(
    CRUDBase[EnergyFlowUpload, EnergyFlowUploadCreate, EnergyFlowUploadUpdate]
):
    def get_by_name(self, *, session: Session, name: str):
        "Get a single EnergyFlowUpload by name"

        return session.exec(
            select(EnergyFlowUpload).where(EnergyFlowUpload.name == name)
        ).first()


energyflow_crud = CRUDEnergyFlow(EnergyFlow)
energyflow_upload_crud = EnergyFlowUploadCRUD(EnergyFlowUpload)
