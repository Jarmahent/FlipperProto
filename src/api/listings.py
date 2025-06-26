from datetime import datetime
from typing import Optional
from fastapi import APIRouter
from pydantic import BaseModel, ConfigDict
from sqlalchemy import select

from api.metadata import API_TAGS
from database import Listing, Part, get_db

router = APIRouter(prefix="/listings/v1", tags=[API_TAGS.LISTINGS.value])


class ListingSchema(BaseModel):
    part_id: int
    platform: str
    external_id: str
    url: str
    price_c: float
    fees_c: float
    status: str
    listed_datetime: Optional[datetime] = None
    sold_datetime: Optional[datetime] = None

class ListingReadSchema(ListingSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int

@router.post("/", summary="Create a new listing")
async def create_listing(
    listing: ListingSchema
):
    """
    Create a new listing.
    
    Returns:
        A success message indicating the listing was created.
    """
    session = get_db()
    for session in session:
        dump = listing.model_dump()
        list_ebj = Listing(**dump)
        session.add(list_ebj)
        session.commit()

    return {"message": "Listing created successfully"}

@router.get("/", summary="Fetch listings")
async def get_listings(
    part_id: Optional[int] = None,
    vehicle_id: Optional[int] = None
) -> list[ListingReadSchema]:
    """
    Fetch all listings in the system.

    Returns:
        A list of listings.
    """
    session = get_db()
    for session in session:
        stmt = select(Listing)
        if part_id is not None:
            stmt = stmt.where(Listing.part_id == part_id)
        if vehicle_id is not None:
            stmt = stmt.join(Listing.part).join(Part.vehicle).where(Part.vehicle_id == vehicle_id)

        listings = session.scalars(stmt).all()

        v_listings = [ListingReadSchema.model_validate(listing) for listing in listings]
        return v_listings

    return {"message": "No listings found"}
