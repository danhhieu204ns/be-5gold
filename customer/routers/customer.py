import shutil
from typing import List
from fastapi import File, UploadFile, status, APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from configs.database import get_db
from configs.authentication import get_current_user
from customer.models.customer import Customer
from customer.schemas.customer import *
import math
import os


UPLOAD_DIR = "uploads/cccd"
os.makedirs(UPLOAD_DIR, exist_ok=True)


router = APIRouter(
    prefix= "/customer",
    tags=["Customer"]
)
    

@router.get("/all",
            response_model=ListCustomerResponse,
            status_code=status.HTTP_200_OK)
async def get_all_customer(
        db: Session = Depends(get_db),
    ):

    try:
        customers = db.query(Customer).all()
        return ListCustomerResponse(
            customers=customers, 
            total_data=len(customers)
        )
    
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )


@router.get("/pageable", 
            response_model=CustomerPageableResponse, 
            status_code=status.HTTP_200_OK)
async def get_customer_pageable(
        page: int = 1,
        page_size: int = 10,
        db: Session = Depends(get_db)
    ):

    try:
        total = db.query(Customer).count()
        total_page = math.ceil(total / page_size)
        customers = db.query(Customer).limit(page_size).offset((page - 1) * page_size).all()
        return CustomerPageableResponse(
            total_data=total,
            total_page=total_page,
            customers=customers
        )
    
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    

@router.get("/{customer_id}", 
            status_code=status.HTTP_200_OK,  
            response_model=CustomerResponse)
async def get_customer_by_id(
        customer_id: int, 
        db: Session = Depends(get_db)
    ):

    try:
        customer = db.query(Customer).filter(Customer.id == customer_id).first()
        if not customer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Không tìm thấy khách hàng"
            )
        return CustomerResponse(customer=customer)
    
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    

@router.post("/create")
async def create_customer(
        newCustomer: CustomerCreate, 
        db: Session = Depends(get_db), 
    ):
    
    try:
        cccd = db.query(Customer).filter(Customer.cccd == newCustomer.cccd).first()
        if cccd:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, 
                detail="Số CCCD đã tồn tại"
            )

        customer = Customer(
            full_name=newCustomer.full_name,
            cccd=newCustomer.cccd,
            phone_number=newCustomer.phone_number,
            address=newCustomer.address,
            is_new=newCustomer.is_new
        )
        db.add(customer)
        db.commit()

        return JSONResponse(
            status_code=status.HTTP_201_CREATED, 
            content={
                "message": "Thêm khách hàng thành công"
            }
        )
    
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    

@router.post("/upload-cccd/{customer_id}")
def upload_cccd_image(
        customer_id: int,
        cccd_image: UploadFile = File(...),
        db: Session = Depends(get_db)
    ):
    
    try:
        customer = db.query(Customer).filter(Customer.id == customer_id).first()
        if not customer:
            raise HTTPException(status_code=404, detail="Khách hàng không tồn tại")

        file_path = os.path.join(UPLOAD_DIR, f"cccd_{customer.cccd}.jpg")

        with open(file_path, "wb") as f:
            shutil.copyfileobj(cccd_image.file, f)

        customer.cccd_path = file_path
        db.commit()

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message": "Upload ảnh CCCD thành công"
            }
        )

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )   
    

@router.put("/update/{customer_id}")
async def update_customer(
        customer_id: int, 
        updateCustomer: CustomerUpdate, 
        db: Session = Depends(get_db)
    ):
    
    try:
        customer = db.query(Customer).filter(Customer.id == customer_id)
        if not customer.first():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"Khách hàng không tồn tại"
            )

        customer.update(updateCustomer.dict())
        db.commit()

        return JSONResponse(
            status_code=status.HTTP_200_OK, 
            content={
                "message": "Cập nhật khách hàng thành công"
            }
        )
    
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )


@router.delete("/delete/{customer_id}")
async def delete_customer(
        customer_id: int, 
        db: Session = Depends(get_db)
    ):

    try:
        customer = db.query(Customer).filter(Customer.id == customer_id)
        if not customer.first():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"Khách hàng không tồn tại"
            )

        customer.delete()
        db.commit()

        return JSONResponse(
            status_code=status.HTTP_200_OK, 
            content={
                "message": "Xóa khách hàng thành công"
            }
        )
    
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )


@router.delete("/delete_many")
async def delete_many_customer(
        customer_ids: List[int], 
        db: Session = Depends(get_db)
    ):

    try:
        customers = db.query(Customer).filter(Customer.id.in_(customer_ids))
        if not customers.first():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"Khách hàng không tồn tại"
            )

        customers.delete(synchronize_session=False)
        db.commit()

        return JSONResponse(
            status_code=status.HTTP_200_OK, 
            content={
                "message": "Xóa khách hàng thành công"
            }
        )
    
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    

@router.delete("/delete-all")
async def delete_all_customer(
        db: Session = Depends(get_db)
    ):

    try:
        db.query(Customer).delete()
        db.commit()

        return JSONResponse(
            status_code=status.HTTP_200_OK, 
            content={
                "message": "Xóa tất cả khách hàng thành công"
            }
        )
    
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
