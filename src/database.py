from datetime import datetime
import enum
from typing import Optional
from sqlalchemy import Float, ForeignKey, TypeDecorator, create_engine, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, Session, declarative_base, relationship, mapped_column, Mapped

Base = declarative_base()

# Database setup
DATABASE_URL = "sqlite:///./flipperdb.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class DBStrEnum(TypeDecorator):
    impl = String
    cache_ok = True
    """
    Enables passing in a Python enum and storing the enum's *value* in the db.
    The default would have stored the enum's *name* (ie the string).
    """

    def __init__(self, enumtype, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._enumtype = enumtype

    def process_bind_param(self, value, dialect):
        if isinstance(value, enum.Enum):
            return value.value

        return value

    def process_result_value(self, value, dialect):
        if value is None:
            return ""
        return self._enumtype(value)

class VehicleStatus(enum.Enum):
    ACTIVE = "active"
    SOLD = "sold"
    INACTIVE = "inactive"

class PartStatus(enum.Enum):
    IN_BIN = "in_bin"
    LISTED = "listed"
    SOLD = "sold"
    SCRAPPED = "scrapped"

class ListingStatus(enum.Enum):
    ACTIVE = "active"
    SOLD = "sold"
    INACTIVE = "inactive"


class ListingPlatform(enum.Enum):
    EBAY = "EBAY"
    FACEBOOK = "MARKETPLACE"
    CRAIGSLIST = "CRAIGSLIST"
    SHOPIFY = "SHOPIFY"


# SQLAlchemy Model
class Vehicle(Base):
    __tablename__ = "Vehicle"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    make: Mapped[str]
    model: Mapped[str]
    year: Mapped[int]
    vin: Mapped[str] = mapped_column(unique=True)
    purchase_price_c: Mapped[float]
    auction_fee_c: Mapped[float]
    status: Mapped[str]
    purchase_date: Mapped[datetime]


class Part(Base):
    __tablename__ = "Part"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    vehicle_id: Mapped[int] = mapped_column(ForeignKey("Vehicle.id"))
    vehicle = relationship(Vehicle, foreign_keys=[vehicle_id])
    name: Mapped[str]
    oem_number: Mapped[str]
    condition_note: Mapped[str]
    loc_locker: Mapped[str]
    loc_bin: Mapped[str]
    est_value_c: Mapped[float]
    status: Mapped[str]

class Listing(Base):
    __tablename__ = "Listing"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    part_id: Mapped[int] = mapped_column(ForeignKey("Part.id"))
    part = relationship(Part, foreign_keys=[part_id])
    platform: Mapped[ListingPlatform] = mapped_column(DBStrEnum(ListingPlatform))
    external_id: Mapped[str]
    url: Mapped[str]
    price_c: Mapped[float]
    fees_c: Mapped[float]
    status: Mapped[str]
    listed_datetime: Mapped[datetime]
    sold_datetime: Mapped[Optional[datetime]] = mapped_column(nullable=True)


# Database helper
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
