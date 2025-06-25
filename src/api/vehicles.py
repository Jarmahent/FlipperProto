


from datetime import datetime
from fastapi import APIRouter
from pydantic import BaseModel, ConfigDict
from sqlalchemy import select

from api.metadata import API_TAGS
from database import Vehicle, get_db

router = APIRouter(prefix="/vehicles/v1", tags=[API_TAGS.VEHICLES.value])   


class VehicleSchema(BaseModel):
    make: str
    model: str
    year: int
    vin: str
    purchase_price_c: float
    auction_fee_c: float
    status: str
    purchase_date: datetime

class VehicleReadSchema(VehicleSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int

@router.post("/", summary="Create a new vehicle")
async def create_vehicle(
    vehicle: VehicleSchema
):
    """
    Create a new vehicle in the system.
    
    Returns:
        A success message indicating the vehicle was created.
    """
    session = get_db()
    for session in session:
        dump = vehicle.model_dump()
        vehicle = Vehicle(**dump)
        session.add(vehicle)
        session.commit()



    return {"message": "Vehicle created successfully"}



@router.get("/", summary="Fetch vehicles")
async def get_vehicles() -> list[VehicleReadSchema]:
    """
    Create a new vehicle in the system.
    
    Returns:
        A success message indicating the vehicle was created.
    """
    session = get_db()
    for session in session:
        stmt = select(Vehicle)
        vehicles = session.scalars(stmt).all()

        v_vehicles = [VehicleReadSchema.model_validate(vehicle) for vehicle in vehicles]
        return v_vehicles



    return {"message": "Vehicle created successfully"}