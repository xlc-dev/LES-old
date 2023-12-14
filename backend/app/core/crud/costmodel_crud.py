from sqlmodel import Session, select

from app.core.crud.base import CRUDBase
from app.core.models.costmodel_model import (
    CostModel,
    CostModelCreate,
    CostModelUpdate,
)


class CRUDCostModel(CRUDBase[CostModel, CostModelCreate, CostModelUpdate]):
    def get_by_name(self, *, session: Session, name: str):
        return session.exec(
            select(CostModel).where(CostModel.name == name)
        ).first()


costmodel_crud = CRUDCostModel(CostModel)
