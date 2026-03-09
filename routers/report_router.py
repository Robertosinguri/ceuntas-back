from fastapi import APIRouter, Depends
from google.cloud.firestore import Client
from database.firebase_config import get_db
from services.auth_service import get_current_user
from controllers.report_controller import ReportController
from services.report_service import ReportService
from repositories.bill_repository import BillRepository

router = APIRouter(prefix="/reports", tags=["reports"])

def get_report_controller():
    repository = BillRepository()
    service = ReportService(repository)
    return ReportController(service)

@router.get("/annual")
def get_annual_report(
    db: Client = Depends(get_db), 
    current_user: dict = Depends(get_current_user),
    controller: ReportController = Depends(get_report_controller)
):
    return controller.get_annual_report(db, current_user["uid"])
