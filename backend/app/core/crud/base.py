from typing import Any, Generic, Optional, Type, TypeVar, Sequence

from fastapi.encoders import jsonable_encoder

from sqlmodel import SQLModel, Session, select

ModelType = TypeVar("ModelType", bound=SQLModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=SQLModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=SQLModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """CRUD object with default methods to Create, Read, Update, Delete

    :param ModelType:
        A SQLModel class
    :param CreateSchemaType:
        A SQLModel schema class for creating objects
    :param UpdateSchemaType:
        A SQLModel schema class for updating objects
    """

    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get(self, *, session: Session, id: int) -> Optional[ModelType]:
        """Get a single object by id

        :param session:
            A SQLModel session
        :param id:
            The id to get
        """

        return session.get(self.model, id)

    def get_multi(
        self, *, session: Session, skip: int = 0, limit: int = 5000
    ) -> Sequence[ModelType]:
        """Get multiple objects

        :param session:
            A SQLModel session
        :param skip:
            The number of objects to skip
        :param limit:
            The number of objects to limit to
        """

        return session.exec(select(self.model).offset(skip).limit(limit)).all()

    def create(
        self, *, session: Session, obj_in: CreateSchemaType
    ) -> ModelType:
        """Create a single object

        :param session:
            A SQLModel session
        :param obj_in:
            The new database object with values
        """

        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore

        session.add(db_obj)
        session.commit()
        session.refresh(db_obj)

        return db_obj

    def update(
        self,
        *,
        session: Session,
        db_obj: ModelType,
        obj_in: UpdateSchemaType | dict[str, Any]
    ) -> ModelType:
        """Update a single object

        :param session:
            A SQLModel session
        :param db_obj:
            The database object to update
        :param obj_in:
            The new database object with updated values
        """

        obj_data = jsonable_encoder(db_obj)

        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        session.add(db_obj)
        session.commit()
        session.refresh(db_obj)

        return db_obj

    def remove(self, *, session: Session, id: int) -> None:
        """Delete a single object

        :param session:
            A SQLModel session
        :param id:
            The id to delete
        """
        obj = session.get(self.model, id)

        session.delete(obj)
        session.commit()
