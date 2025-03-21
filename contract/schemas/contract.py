from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date
from customer.schemas.customer import CustomerResponse


class ContractBase(BaseModel):
    loan: Optional[int] = None
    interest_rate: Optional[float] = None
    duration: Optional[int] = None
    start_date: Optional[date] = None
    daily_payment: Optional[int] = None
    period: Optional[int] = None

    class Config:
        from_attributes = True


class ContractCreate(ContractBase):
    customer_id: int
    loan: int


class ContractUpdate(ContractBase):
    customer_id: int


class ContractResponse(ContractBase):
    id: int
    contract_number: str
    customer: CustomerResponse
    created_at: datetime

    class Config:
        from_attributes = True


class ListContractResponse(BaseModel):
    contracts: list[ContractResponse]
    total_data: int

    class Config:
        from_attributes = True


class ContractPageableResponse(ContractBase):
    contracts: list[ContractResponse]
    total_data: int
    total_page: int

    class Config:
        from_attributes = True