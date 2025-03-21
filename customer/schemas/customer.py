from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date


class CustomerBase(BaseModel):
    full_name: Optional[str] = None
    cccd: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None
    is_new: Optional[bool] = True

    class Config:
        from_attributes = True


class CustomerCreate(CustomerBase):
    full_name: str
    cccd: str


class CustomerUpdate(CustomerBase):
    pass 


class CustomerResponse(CustomerBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class ListCustomerResponse(BaseModel):
    customers: list[CustomerResponse]
    total_data: int

    class Config:
        from_attributes = True


class CustomerPageableResponse(BaseModel):
    customers: list[CustomerResponse]

    total_pages: int
    total_data: int

    class Config:
        from_attributes = True
