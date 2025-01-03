from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    func,
    Boolean,
    Index,
)
from sqlalchemy.orm import relationship
from database.db import Base


class Actor(Base):
    __tablename__ = "actor"

    actor_id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(45), nullable=False)
    last_name = Column(String(45), nullable=False, index=True)
    last_update = Column(
        DateTime, nullable=False, default=func.now(), onupdate=func.now()
    )


class Country(Base):
    __tablename__ = "country"

    country_id = Column(Integer, primary_key=True, autoincrement=True)
    country = Column(String(50), nullable=False)
    last_update = Column(
        DateTime,
        nullable=False,
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
    )

    city = relationship("City", back_populates="country")


class Category(Base):
    __tablename__ = "category"

    category_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(25), nullable=False)
    last_update = Column(
        DateTime,
        nullable=False,
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
    )


class City(Base):
    __tablename__ = "city"

    city_id = Column(Integer, primary_key=True, autoincrement=True)
    city = Column(String(50), nullable=False)
    country_id = Column(Integer, ForeignKey("country.country_id"), nullable=False)
    last_update = Column(
        DateTime,
        nullable=False,
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
    )

    country = relationship("Country", back_populates="city")
    address = relationship("Address", back_populates="city")


class Address(Base):
    __tablename__ = "address"

    address_id = Column(Integer, primary_key=True, autoincrement=True)
    address = Column(String(50), nullable=False)
    address2 = Column(String(50))
    district = Column(String(20), nullable=False)
    city_id = Column(Integer, ForeignKey("city.city_id"), nullable=False)
    postal_code = Column(String(10))
    phone = Column(String(20), nullable=False)
    # location = Column(Geometry('Point', srid=0))  # For MySQL with spatial extensions
    last_update = Column(
        DateTime,
        nullable=False,
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
    )

    city = relationship("City", back_populates="address")


class Customer(Base):
    __tablename__ = "customer"

    customer_id = Column(Integer, primary_key=True, autoincrement=True)
    # store_id = Column(Integer, ForeignKey("store.store_id"), nullable=False)
    store_id = Column(Integer, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String)
    address_id = Column(Integer, ForeignKey("address.address_id"), nullable=False)
    active = Column(Boolean, nullable=False, default=True)
    create_date = Column(DateTime, nullable=False)
    last_update = Column(DateTime)

    # __table_args__ = (
    #     Index("idx_fk_store_id", "store_id"),
    #     Index("idx_fk_address_id", "address_id"),
    #     Index("idx_last_name", "last_name"),
    # )

    # store = relationship("Store", backref="customers")
    address = relationship("Address", backref="customers")
