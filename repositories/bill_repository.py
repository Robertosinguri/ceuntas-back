from google.cloud.firestore import Client
from schemas.bill_schema import BillCreate, BillUpdate
from datetime import date

class BillRepository:
    def __init__(self):
        self.collection_name = "bills"

    def get_by_id(self, db: Client, bill_id: str):
        doc = db.collection(self.collection_name).document(bill_id).get()
        if doc.exists:
            data = doc.to_dict()
            data["id"] = doc.id
            return data
        return None

    def get_all(self, db: Client, user_id: str):
        bills = []
        docs = db.collection(self.collection_name)\
                 .where("user_id", "==", user_id)\
                 .stream()
        for doc in docs:
            data = doc.to_dict()
            data["id"] = doc.id
            # Convertimos fechas de string a date si es necesario
            bills.append(data)
        return bills

    def get_monthly_bills(self, db: Client, user_id: str, year: int, month: int):
        # En Firestore las queries son potentes. 
        # Buscamos por rango de fechas (asumiendo formato ISO string o date)
        start_date = date(year, month, 1).isoformat()
        # Nota: para simplificar usamos strings ISO, pero Firestore maneja Timestamps
        docs = db.collection(self.collection_name)\
                 .where("user_id", "==", user_id)\
                 .where("due_date", ">=", start_date)\
                 .stream()
        
        bills = []
        for doc in docs:
            data = doc.to_dict()
            data["id"] = doc.id
            bills.append(data)
        return bills

    def create(self, db: Client, bill_in: BillCreate):
        # Firestore genera IDs automáticos si no pasamos uno
        bill_data = bill_in.dict()
        # Convertimos objetos date a strings para Firestore (o Timestamps)
        bill_data["due_date"] = bill_data["due_date"].isoformat()
        bill_data["status"] = "unpaid"
        
        _, doc_ref = db.collection(self.collection_name).add(bill_data)
        bill_data["id"] = doc_ref.id
        return bill_data

    def update(self, db: Client, bill_id: str, update_data: dict):
        doc_ref = db.collection(self.collection_name).document(bill_id)
        doc_ref.update(update_data)
        return self.get_by_id(db, bill_id)

    def delete(self, db: Client, bill_id: str):
        db.collection(self.collection_name).document(bill_id).delete()
        return True
