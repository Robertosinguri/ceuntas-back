from fastapi import APIRouter, Depends, status
from typing import List
from google.cloud.firestore import Client
from database.firebase_config import get_db
from schemas.bill_schema import BillCreate, BillUpdate, BillResponse
from repositories.bill_repository import BillRepository
from services.bill_service import BillService
from services.auth_service import get_current_user
from controllers.bill_controller import BillController

router = APIRouter(prefix="/bills", tags=["bills"])

# Initialize manually without a DI container for simplicity
def get_bill_controller():
    repository = BillRepository()
    service = BillService(repository)
    return BillController(service)

@router.post("/", response_model=BillResponse, status_code=status.HTTP_201_CREATED)
def create_bill(
    bill_in: BillCreate, 
    db: Client = Depends(get_db), 
    current_user: dict = Depends(get_current_user),
    controller: BillController = Depends(get_bill_controller)
):
    return controller.create_bill(db, bill_in, current_user["uid"])

@router.get("/", response_model=List[BillResponse])
def get_all_bills(
    db: Client = Depends(get_db), 
    current_user: dict = Depends(get_current_user),
    controller: BillController = Depends(get_bill_controller)
):
    return controller.list_all(db, current_user["uid"])

@router.get("/monthly", response_model=List[BillResponse])
def get_monthly_bills(
    month: int,
    year: int,
    db: Client = Depends(get_db), 
    current_user: dict = Depends(get_current_user),
    controller: BillController = Depends(get_bill_controller)
):
    return controller.get_monthly_bills(db, current_user["uid"], month, year)

@router.patch("/{bill_id}/pay", response_model=BillResponse)
def pay_bill(
    bill_id: str,
    db: Client = Depends(get_db), 
    current_user: dict = Depends(get_current_user),
    controller: BillController = Depends(get_bill_controller)
):
    return controller.mark_as_paid(db, current_user["uid"], bill_id)

@router.put("/{bill_id}", response_model=BillResponse)
def update_bill(
    bill_id: str,
    bill_in: BillUpdate,
    db: Client = Depends(get_db), 
    current_user: dict = Depends(get_current_user),
    controller: BillController = Depends(get_bill_controller)
):
    return controller.update_bill(db, current_user["uid"], bill_id, bill_in)
@router.delete("/{bill_id}")
def delete_bill(
    bill_id: str,
    db: Client = Depends(get_db), 
    current_user: dict = Depends(get_current_user),
    controller: BillController = Depends(get_bill_controller)
):
    return controller.delete_bill(db, current_user["uid"], bill_id)
