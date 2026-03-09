from google.cloud.firestore import Client
from fastapi import HTTPException, status
from services.bill_service import BillService
from schemas.bill_schema import BillCreate, BillUpdate

class BillController:
    def __init__(self, service: BillService):
        self.service = service

    def create_bill(self, db: Client, bill_in: BillCreate, user_id: str):
        return self.service.create_bill(db, bill_in, user_id)

    def update_bill(self, db: Client, user_id: str, bill_id: str, bill_in: BillUpdate):
        updated_bill = self.service.update_bill(db, user_id, bill_id, bill_in)
        if not updated_bill:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Bill with ID {bill_id} not found"
            )
        return updated_bill

    def get_monthly_bills(self, db: Client, user_id: str, month: int, year: int):
        bills = self.service.get_bills_by_month(db, user_id, month, year)
        if not bills:
            # Not found is okay, return empty list
            return []
        return bills

    def mark_as_paid(self, db: Client, user_id: str, bill_id: str):
        updated_bill = self.service.mark_bill_as_paid(db, user_id, bill_id)
        if not updated_bill:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Bill with ID {bill_id} not found"
            )
        return updated_bill

    def delete_bill(self, db: Client, user_id: str, bill_id: str):
        success = self.service.delete_bill(db, user_id, bill_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Bill with ID {bill_id} not found or unauthorized"
            )
        return {"status": "success"}

    def list_all(self, db: Client, user_id: str):
        return self.service.list_all_bills(db, user_id)
