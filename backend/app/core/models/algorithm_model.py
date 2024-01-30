"""This file contains the model for the Algorithm table.

The Algorithm table is used to store all the algorithms that are available
to use in the simulation. The algorithms are used to plan in schedulable loads
into available timeslots.
"""

from typing import Optional

from sqlmodel import SQLModel, Field


class AlgorithmBase(SQLModel):
    """Algoritm model that saves algorithms in the database.

    max_temperature contains the the amount of trials being done for simulated
        annealing, and how fast it decays.
    algorithm contains the code for creating the planning
    """

    name: str = Field(index=True, unique=True, nullable=False)
    description: str = Field(nullable=False)
    max_temperature: Optional[int] = Field(nullable=True)
    algorithm: str = Field(nullable=False)


class Algorithm(AlgorithmBase, table=True):
    id: int = Field(primary_key=True)


class AlgorithmRead(AlgorithmBase):
    id: int


class AlgorithmCreate(AlgorithmBase):
    pass


class AlgorithmUpdate(AlgorithmBase):
    pass
