from typing import Sequence
from csv import DictReader
from io import StringIO

from fastapi import APIRouter, Depends, UploadFile, Form, status

from sqlmodel import Session

from app.utils import Logger, get_session

from app.core.crud.energyflow_crud import (
    energyflow_crud,
    energyflow_upload_crud,
)

from app.core.models import energyflow_model

router = APIRouter()


@router.get("/", response_model=list[energyflow_model.EnergyFlowRead])
async def get_energyflows(
    *, session: Session = Depends(get_session)
) -> Sequence[energyflow_model.EnergyFlow]:
    return energyflow_crud.get_multi(session=session)


@router.get("/{id}", response_model=energyflow_model.EnergyFlowRead)
async def get_energyflow(
    *, id: int, session: Session = Depends(get_session)
) -> energyflow_model.EnergyFlow:
    energyflow = energyflow_crud.get(session=session, id=id)

    if not energyflow:
        Logger.exception(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Energyflow with id {id} not found",
        )

    return energyflow


@router.post("/", status_code=status.HTTP_201_CREATED)
async def post_energyflow(
    *,
    form_data: energyflow_model.EnergyFlowCreate,
    session: Session = Depends(get_session),
) -> None:
    check_energyflow = energyflow_crud.get_by_timestamp(
        session=session, timestamp=form_data.timestamp
    )

    if check_energyflow:
        Logger.exception(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Energyflow with timestamp {form_data.timestamp} already exists",  # noqa: E501
        )

    energyflow_crud.create(session=session, obj_in=form_data)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_energyflow(
    *,
    id: int,
    session: Session = Depends(get_session),
) -> None:
    # Don't allow the user to delete the default energyflow
    if id == 1:
        Logger.exception(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Energyflow with id {id} is not allowed to be deleted",
        )

    eneryflow = energyflow_crud.get(session=session, id=id)

    if not eneryflow:
        Logger.exception(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Energyflow with id {id} not found",
        )

    energyflow_crud.remove(session=session, id=id)


@router.get(
    "/upload", response_model=list[energyflow_model.EnergyFlowUploadRead]
)
async def get_energyflow_uploads(
    *, session: Session = Depends(get_session)
) -> Sequence[energyflow_model.EnergyFlowUpload]:
    return energyflow_upload_crud.get_multi(session=session)


@router.get(
    "/upload/{id}", response_model=energyflow_model.EnergyFlowUploadRead
)
async def get_energyflow_upload(
    *, id: int, session: Session = Depends(get_session)
) -> energyflow_model.EnergyFlowUpload:
    energyflow_upload = energyflow_upload_crud.get(session=session, id=id)

    if not energyflow_upload:
        Logger.exception(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"EnergyflowUpload with id {id} not found",
        )

    return energyflow_upload


@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_energyflow(
    *,
    name: str = Form(...),
    description: str = Form(...),
    file: UploadFile,
    session: Session = Depends(get_session),
) -> None:
    check_energyflow_upload = energyflow_upload_crud.get_by_name(
        session=session, name=name
    )

    if check_energyflow_upload:
        Logger.exception(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"EnergyflowUpload with name {name} already exists",
        )

    get_energyflow_upload = energyflow_upload_crud.get_multi(session=session)

    id_to_set = 1

    if len(get_energyflow_upload) > 0:
        id_to_set = get_energyflow_upload[-1].id + 1

    try:
        contents = file.file.read().decode("utf-8-sig")
        with StringIO(contents) as f:
            reader = DictReader(f, delimiter=";", skipinitialspace=True)
            for row in reader:
                energy_used = float(row["energy_used"].replace(",", "."))
                solar_produced = float(row["solar_produced"].replace(",", "."))

                energyflow_crud.create(
                    session=session,
                    obj_in=energyflow_model.EnergyFlowCreate(
                        timestamp=int(row["timestamp"]),
                        energy_used=energy_used,
                        solar_produced=solar_produced,
                        energyflow_upload_id=id_to_set,
                    ),
                )
    except Exception as e:
        Logger.exception(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing CSV file: {str(e)}",
        )
    finally:
        file.file.close()

    energyflow_upload_crud.create(
        session=session,
        obj_in=energyflow_model.EnergyFlowUploadCreate(
            name=name, description=description
        ),
    )


@router.delete("/upload/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_energyflow_upload(
    *,
    id: int,
    session: Session = Depends(get_session),
) -> None:
    # Don't allow the user to delete the default energyflow
    if id == 1:
        Logger.exception(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"EnergyflowUpload with id {id} is not allowed to be deleted",  # noqa: E501
        )

    eneryflow_upload = energyflow_upload_crud.get(session=session, id=id)

    if not eneryflow_upload:
        Logger.exception(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"EnergyflowUpload with id {id} not found",
        )

    energyflow_upload_crud.remove(session=session, id=id)
