


from datetime import datetime
from fastapi import APIRouter
from pydantic import BaseModel

from database import Vehicle, get_db

router = APIRouter(prefix="/vehicles/v1", tags=[{"Vehicles": "Vehicles"}])


class VehicleSchema(BaseModel):
    make: str
    model: str
    year: int
    vin: str
    purchase_price_c: float
    auction_fee_c: float
    status: str
    purchase_date: datetime


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