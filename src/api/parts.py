from datetime import datetime
from typing import Optional
from fastapi import APIRouter
from pydantic import BaseModel, ConfigDict
from sqlalchemy import select

from api.metadata import API_TAGS
from database import Part, get_db

router = APIRouter(prefix="/parts/v1", tags=[API_TAGS.PARTS.value])


class PartSchema(BaseModel):
    vehicle_id: int
    name: str
    oem_number: str
    condition_note: str
    loc_locker: str
    loc_bin: str
    est_value_c: float
    status: str

class PartReadSchema(PartSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int

@router.post("/", summary="Create a new part")
async def create_part(
    part: PartSchema
):
    """
    Create a new part in the system.
    
    Returns:
        A success message indicating the part was created.
    """
    session = get_db()
    for session in session:
        dump = part.model_dump()
        part_obj = Part(**dump)
        session.add(part_obj)
        session.commit()

    return {"message": "Part created successfully"}


@router.get("/", summary="Fetch parts")
async def get_parts(
    vehicle_id: Optional[int] = None
) -> list[PartReadSchema]:
    """
    Fetch all parts in the system.
    
    Returns:
        A list of parts.
    """
    session = get_db()
    for session in session:
        stmt = select(Part)
        if vehicle_id is not None:
            stmt = stmt.where(Part.vehicle_id == vehicle_id)
        parts = session.scalars(stmt).all()

        v_parts = [PartReadSchema.model_validate(part) for part in parts]
        return v_parts

    return {"message": "No parts found"}
