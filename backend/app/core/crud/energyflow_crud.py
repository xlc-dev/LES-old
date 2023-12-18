from app.core.crud.base import CRUDBase
from app.core.models.energyflow_model import (
    EnergyFlow,
    EnergyFlowCreate,
    EnergyFlowUpdate,
)


class CRUDEnergyFlow(CRUDBase[EnergyFlow, EnergyFlowCreate, EnergyFlowUpdate]):
    pass


energyflow_crud = CRUDEnergyFlow(EnergyFlow)
