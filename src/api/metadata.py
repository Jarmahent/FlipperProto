from enum import Enum


class API_TAGS(Enum):
    VEHICLES = "Vehicles"
    PARTS = "Parts"
    LISTINGS = "Listings"

metadata_tag_info = [
    {
        "name": API_TAGS.VEHICLES.value,
        "name": API_TAGS.PARTS.value,
        "name": API_TAGS.LISTINGS.value,
    }
]
