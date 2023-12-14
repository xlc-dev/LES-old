from sqlmodel import SQLModel

from app.core.models.costmodel_model import CostModel
from app.core.models.twinworld_model import TwinWorld


class SimulationData(SQLModel):
    twin_world: list[TwinWorld]
    cost_model: list[CostModel]
