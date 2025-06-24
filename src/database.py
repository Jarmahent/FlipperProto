import datetime
import enum
from sqlalchemy import Float, create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, Session, declarative_base, relationship

Base = declarative_base()

# Database setup
DATABASE_URL = "sqlite:///./flipperdb.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

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


# SQLAlchemy Model
class Vehicle(Base):
    __tablename__ = "Vehicle"
    
    id: int = Column(Integer, primary_key=True, index=True)
    make: str = Column(String)
    model: str = Column(String)
    year: int = Column(Integer)
    vin: str = Column(String, unique=True)
    purchase_price_c:float = Column(Float)
    auction_fee_c:float = Column(Float)
    status:str = Column(String)
    purchase_date: datetime = Column(DateTime)


class Part(Base):
    __tablename__ = "Part"
    
    id: int = Column(Integer, primary_key=True, index=True)
    vehicle_id: int = relationship("Vehicle", back_populates="parts")
    name: str = Column(String)
    oem_number: str = Column(String)
    condition_note: str = Column(String)
    loc_locker: str = Column(String)
    est_value_c: float = Column(Float)
    status: str = Column(String)

class Listing(Base):
    __tablename__ = "Listing"
    
    id: int = Column(Integer, primary_key=True, index=True)
    part_id: int = relationship("Part", back_populates="listings")
    platform: str = Column(String)
    external_id: str = Column(String)
    url: str = Column(String)
    price_c: float = Column(Float)
    fees_c: float = Column(Float)
    status: str = Column(String)
    listed_datetime: datetime = Column(DateTime)
    sold_datetime: datetime = Column(DateTime, nullable=True)


# Database helper
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

