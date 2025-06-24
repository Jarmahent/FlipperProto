


from fastapi import APIRouter

router = APIRouter(prefix="/vehicles/v1", tags=["Vehicles"])



@router.get("/status", summary="Get vehicle status options")
async def get_vehicle_status():
    """
    Returns a list of vehicle status options.
    """
    return {
        "status": [
            "active",
            "sold",
            "scrapped"
        ]
    }