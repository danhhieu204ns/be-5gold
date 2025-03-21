from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String, text, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from configs.database import Base


class Contract(Base):
    __tablename__ = "contracts"

    id = Column(Integer, primary_key=True, nullable=False, index=True)
    contract_number = Column(String, nullable=False, unique=True)
    loan = Column(Integer, nullable=True)
    interest_rate = Column(Float, nullable=True)
    duration = Column(Integer, nullable=True)
    start_date = Column(Date, nullable=True)
    daily_payment = Column(Integer, nullable=True)
    period = Column(Integer, nullable=True)
    
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    customer_id = Column(Integer, ForeignKey('customers.id', ondelete='CASCADE'), nullable=False)
    customer = relationship("Customer", back_populates="contracts")
