from google.cloud.firestore import Client
from repositories.bill_repository import BillRepository
from schemas.bill_schema import BillCreate, BillUpdate
from datetime import date

class BillService:
    def __init__(self, repository: BillRepository):
        self.repository = repository

    def list_all_bills(self, db: Client, user_id: str):
        bills = self.repository.get_all(db, user_id)
        return [self._add_calculated_fields(b) for b in bills]

    def get_bills_by_month(self, db: Client, user_id: str, month: int, year: int):
        bills = self.repository.get_monthly_bills(db, user_id, year, month)
        return [self._add_calculated_fields(b) for b in bills]

    def create_bill(self, db: Client, bill_in: BillCreate, user_id: str):
        # Asignamos el user_id del token al objeto antes de guardar
        bill_in.user_id = user_id
        bill_data = self.repository.create(db, bill_in)
        return self._add_calculated_fields(bill_data)

    def update_bill(self, db: Client, user_id: str, bill_id: str, bill_in: BillUpdate):
        # Verificamos propiedad antes de actualizar
        bill = self.repository.get_by_id(db, bill_id)
        if not bill or bill.get("user_id") != user_id:
            return None
        
        update_data = bill_in.dict(exclude_unset=True)
        # Aseguramos formato de fecha si vienen objetos date en el update
        for field in ["due_date", "payment_date"]:
            if isinstance(update_data.get(field), date):
                update_data[field] = update_data[field].isoformat()
            
        updated_bill = self.repository.update(db, bill_id, update_data)
        return self._add_calculated_fields(updated_bill)

    def mark_bill_as_paid(self, db: Client, user_id: str, bill_id: str):
        # Primero verificamos que la factura exista y sea del usuario
        bill = self.repository.get_by_id(db, bill_id)
        if not bill or bill.get("user_id") != user_id:
            return None
        
        # Lógica de toggle: si está pagada, la ponemos pendiente. Si no, la pagamos.
        if bill.get("status") == "paid":
            update_data = {"status": "unpaid", "payment_date": None}
        else:
            update_data = {
                "status": "paid", 
                "payment_date": date.today().isoformat(),
                "is_provisional": False
            }

        updated_bill = self.repository.update(db, bill_id, update_data)
        return self._add_calculated_fields(updated_bill)

    def delete_bill(self, db: Client, user_id: str, bill_id: str):
        bill = self.repository.get_by_id(db, bill_id)
        if not bill or bill.get("user_id") != user_id:
            return False
        return self.repository.delete(db, bill_id)

    def _add_calculated_fields(self, bill: dict):
        if not bill:
            return None
            
        due_date_str = bill.get("due_date")
        if due_date_str:
            # Convertir string ISO "YYYY-MM-DD" a objeto date
            due_date_obj = date.fromisoformat(due_date_str)
            days_left = (due_date_obj - date.today()).days
            bill["days_until_due"] = days_left
        
        return bill
