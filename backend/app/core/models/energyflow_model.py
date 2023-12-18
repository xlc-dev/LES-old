from sqlmodel import SQLModel, Field

class EnergyFlowBase(SQLModel):
    timestamp: int = Field(nullable=False)
    energy_used: int = Field(nullable=False)
    solar_produced: int = Field(default=0, nullable=False)


class EnergyFlow(EnergyFlowBase, table=True):
    id: int = Field(primary_key=True)


class EnergyFlowRead(EnergyFlowBase):
     id: int


class EnergyFlowCreate(EnergyFlowBase):
    pass


class EnergyFlowUpdate(EnergyFlowBase):
    pass
