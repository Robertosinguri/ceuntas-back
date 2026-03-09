from google.cloud.firestore import Client
from services.report_service import ReportService

class ReportController:
    def __init__(self, report_service: ReportService):
        self.report_service = report_service

    def get_annual_report(self, db: Client, user_id: str):
        return self.report_service.generate_annual_report(db, user_id)
