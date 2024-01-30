"""This file contains the model for the Energyflow table.

The Energyflow table is used to store all the energy usage and the
internal yield of green energy that is available to be used in the simulation.
"""

from sqlmodel import SQLModel, Field


class EnergyFlowBase(SQLModel):
    "Energyflow model that saves the energyflow in the database."

    timestamp: int = Field(nullable=False, index=True)  # in unix
    energy_used: float = Field(nullable=False)  # in kWh
    solar_produced: float = Field(nullable=False)  # in kWh


class EnergyFlow(EnergyFlowBase, table=True):
    id: int = Field(primary_key=True)


class EnergyFlowRead(EnergyFlowBase):
    pass


class EnergyFlowCreate(EnergyFlowBase):
    pass


class EnergyFlowUpdate(EnergyFlowBase):
    pass
