from sqlmodel import SQLModel, Field


class EnergyFlowBase(SQLModel):
    timestamp: int = Field(nullable=False, index=True)
    energy_used: float = Field(nullable=False)
    solar_produced: float = Field(nullable=False)


class EnergyFlow(EnergyFlowBase, table=True):
    id: int = Field(primary_key=True)


class EnergyFlowRead(EnergyFlowBase):
    pass


class EnergyFlowCreate(EnergyFlowBase):
    pass


class EnergyFlowUpdate(EnergyFlowBase):
    pass
