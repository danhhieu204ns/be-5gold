from sqlalchemy import Boolean, Column, Integer, String, text, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from configs.database import Base


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, nullable=False, index=True)
    full_name = Column(String, nullable=False)
    cccd = Column(String, nullable=True)
    cccd_path = Column(String, nullable=True)
    phone_number = Column(String, nullable=True)
    address = Column(String, nullable=True)
    is_new = Column(Boolean, default=True, nullable=True)
    
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    contracts = relationship("Contract", back_populates="customer", uselist=True)