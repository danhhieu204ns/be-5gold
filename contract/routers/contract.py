from fastapi import status, APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from configs.database import get_db
from configs.authentication import get_current_user
from contract.models.contract import Contract
from contract.schemas.contract import *
from customer.models.customer import Customer
from utils.gen_contract_num import generate_contract_code
import math


router = APIRouter(
    prefix= "/contract",
    tags=["Contract"]
)
    

@router.get("/all",
            response_model=ListContractResponse,
            status_code=status.HTTP_200_OK)
async def get_all_contract(
        db: Session = Depends(get_db),
    ):

    try:
        contracts = db.query(Contract).all()
        return ListContractResponse(
            contracts=contracts, 
            total_data=len(contracts)
        )
    
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )


@router.get("/pageable", 
            response_model=ContractPageableResponse, 
            status_code=status.HTTP_200_OK)
async def get_contract_pageable(
        page: int = 1,
        page_size: int = 10,
        db: Session = Depends(get_db)
    ): 

    try:
        contracts = db.query(Contract).limit(page_size).offset((page - 1) * page_size).all()
        total_data = db.query(Contract).count()
        total_page = math.ceil(total_data / page_size)
        return ContractPageableResponse(
            contracts=contracts, 
            total_data=total_data, 
            total_page=total_page
        )
    
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    

@router.get("/{contract_number}", 
            status_code=status.HTTP_200_OK,  
            response_model=ContractResponse)
async def get_contract_by_number(
        contract_number: str,
        db: Session = Depends(get_db)
    ):

    try:
        contract = db.query(Contract).filter(Contract.contract_number.ilike(contract_number)).first()
        if not contract:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Hợp đồng không tồn tại"
            )

        return ContractResponse(contract=contract)
    
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )


@router.post("/create")
async def create_contract(
        newContract: ContractCreate,
        db: Session = Depends(get_db),
    ):

    try:
        customer = db.query(Customer).filter(Customer.id == newContract.customer_id).first()
        if not customer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Khách hàng không tồn tại"
            )

        contract = Contract(
            contract_number=generate_contract_code(db),
            loan=newContract.loan,
            interest_rate=newContract.interest_rate,
            duration=newContract.duration,
            start_date=newContract.start_date,
            daily_payment=newContract.daily_payment,
            period=newContract.period,
            customer_id=newContract.customer_id
        )
        db.add(contract)
        db.commit()

        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "message": "Tạo hợp đồng thành công"
            }
        )
    
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )


@router.put("/update/{contract_number}")
async def update_contract(
        contract_number: str,
        updateContract: ContractUpdate,
        db: Session = Depends(get_db)
    ):

    try:
        contract = db.query(Contract).filter(Contract.contract_number.ilike(contract_number))
        if not contract.first():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Hợp đồng không tồn tại"
            )

        customer = db.query(Customer).filter(Customer.id == updateContract.customer_id).first()
        if not customer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Khách hàng không tồn tại"
            )

        contract.update({
            Contract.loan: updateContract.loan,
            Contract.interest_rate: updateContract.interest_rate,
            Contract.duration: updateContract.duration,
            Contract.start_date: updateContract.start_date,
            Contract.daily_payment: updateContract.daily_payment,
            Contract.period: updateContract.period,
            Contract.customer_id: updateContract.customer_id
        })
        db.commit()

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message": "Cập nhật hợp đồng thành công"
            }
        )
    
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )


@router.delete("/delete/{contract_number}")
async def delete_contract(
        contract_number: str,
        db: Session = Depends(get_db)
    ):

    try:
        contract = db.query(Contract).filter(Contract.contract_number.ilike(contract_number))
        if not contract.first():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Hợp đồng không tồn tại"
            )

        contract.delete()
        db.commit()

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message": "Xóa hợp đồng thành công"
            }
        )
    
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )


@router.delete("/delete_many")
async def delete_many_contract(
        deleteMany: list[int],
        db: Session = Depends(get_db)
    ):  

    try:
        contracts = db.query(Contract).filter(Contract.id.in_(deleteMany))
        if not contracts.first():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Hợp đồng không tồn tại"
            )

        contracts.delete(synchronize_session=False)
        db.commit()

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message": "Xóa nhiều hợp đồng thành công"
            }
        )
    
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    

@router.delete("/delete-all")
async def delete_all_contract(
        db: Session = Depends(get_db)
    ):

    try:
        contracts = db.query(Contract)
        if not contracts.first():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Hợp đồng không tồn tại"
            )

        contracts.delete()
        db.commit()

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message": "Xóa tất cả hợp đồng thành công"
            }
        )

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
