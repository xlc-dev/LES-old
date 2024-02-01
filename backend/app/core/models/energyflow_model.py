"""This file contains the model for the Energyflow table.

The Energyflow table is used to store all the energy usage and the
internal yield of green energy that is available to be used in the simulation.
"""

from sqlmodel import SQLModel, Field, Relationship


class EnergyFlowBase(SQLModel):
    "Energyflow model that saves the energyflow in the database"

    timestamp: int = Field(nullable=False, index=True)  # in unix
    energy_used: float = Field(nullable=False)  # in kWh
    solar_produced: float = Field(nullable=False)  # in kWh


class EnergyFlow(EnergyFlowBase, table=True):
    id: int = Field(primary_key=True)

    energyflow_upload: "EnergyFlowUpload" = Relationship(
        back_populates="energyflows"
    )
    energyflow_upload_id: int = Field(foreign_key="energyflowupload.id")


class EnergyFlowRead(EnergyFlowBase):
    pass


class EnergyFlowCreate(EnergyFlowBase):
    energyflow_upload_id: int


class EnergyFlowUpdate(EnergyFlowBase):
    pass


class EnergyFlowUploadBase(SQLModel):
    "Upload table for uploading CSV Energyflows"

    name: str = Field(index=True, unique=True, nullable=False)
    description: str = Field(nullable=False)


class EnergyFlowUpload(EnergyFlowUploadBase, table=True):
    id: int = Field(primary_key=True)

    energyflows: list["EnergyFlow"] = Relationship(
        back_populates="energyflow_upload",
        sa_relationship_kwargs={"cascade": "delete"},
    )


class EnergyFlowUploadRead(EnergyFlowUploadBase):
    id: int


class EnergyFlowUploadCreate(EnergyFlowUploadBase):
    pass


class EnergyFlowUploadUpdate(EnergyFlowUploadBase):
    pass
