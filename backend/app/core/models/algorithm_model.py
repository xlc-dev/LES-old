from sqlmodel import SQLModel, Field


class AlgorithmBase(SQLModel):
    name: str = Field(index=True, unique=True, nullable=False)
    description: str = Field(nullable=False)


class Algorithm(AlgorithmBase, table=True):
    id: int = Field(primary_key=True)


class AlgorithmRead(AlgorithmBase):
    id: int


class AlgorithmCreate(AlgorithmBase):
    pass


class AlgorithmUpdate(AlgorithmBase):
    pass
