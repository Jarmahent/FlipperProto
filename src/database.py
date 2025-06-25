from datetime import datetime
import enum
from sqlalchemy import Float, ForeignKey, TypeDecorator, create_engine, Column, Integer, String, DateTime
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
    EBAY = "eBay"
    FACEBOOK = "Facebook Marketplace"
    CRAIGSLIST = "Craigslist"
    SHOPIFY = "Shopify"


# SQLAlchemy Model
class Vehicle(Base):
    __tablename__ = "Vehicle"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    make: Mapped[str] = Column(String)
    model: Mapped[str] = Column(String)
    year: Mapped[int] = Column(Integer)
    vin: Mapped[str] = Column(String, unique=True)
    purchase_price_c: Mapped[float] = Column(Float)
    auction_fee_c: Mapped[float] = Column(Float)
    status: Mapped[str] = Column(String)
    purchase_date: Mapped[datetime] = Column(DateTime)


class Part(Base):
    __tablename__ = "Part"
    
    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    vehicle_id: Mapped[int] = mapped_column(ForeignKey("Vehicle.id"))
    name: Mapped[str] = Column(String)
    oem_number: Mapped[str] = Column(String)
    condition_note: Mapped[str] = Column(String)
    loc_locker: Mapped[str] = Column(String)
    est_value_c: Mapped[float] = Column(Float)
    status: Mapped[str] = Column(String)

class Listing(Base):
    __tablename__ = "Listing"
    
    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    part_id: Mapped[int] = mapped_column(ForeignKey("Part.id"))
    platform: Mapped[ListingPlatform] = mapped_column("platform", DBStrEnum(ListingPlatform))
    external_id: Mapped[str] = Column(String)
    url: Mapped[str] = Column(String)
    price_c: Mapped[float] = Column(Float)
    fees_c: Mapped[float] = Column(Float)
    status: Mapped[str] = Column(String)
    listed_datetime: Mapped[datetime] = Column(DateTime)
    sold_datetime: Mapped[datetime] = Column(DateTime, nullable=True)


# Database helper
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

