from pydantic import BaseModel
from datetime import date
from typing import Optional
from enum import Enum

class BillStatus(str, Enum):
    UNPAID = "unpaid"
    PAID = "paid"
    OVERDUE = "overdue"

class BillType(str, Enum):
    SERVICE = "service"
    INVOICE = "invoice"

class BillBase(BaseModel):
    name: str
    amount: float
    due_date: date
    category: Optional[str] = "Otros"  # Ej: Hogar, Auto, Servicios
    user_id: Optional[str] = None
    description: Optional[str] = None
    type: BillType = BillType.SERVICE
    invoice_number: Optional[str] = None
    google_event_id: Optional[str] = None
    is_provisional: bool = False

class BillCreate(BillBase):
    pass

class BillUpdate(BaseModel):
    name: Optional[str] = None
    amount: Optional[float] = None
    due_date: Optional[date] = None
    category: Optional[str] = None
    status: Optional[BillStatus] = None
    payment_date: Optional[date] = None
    description: Optional[str] = None
    google_event_id: Optional[str] = None
    is_provisional: Optional[bool] = None

class BillResponse(BillBase):
    id: str
    status: BillStatus
    payment_date: Optional[date] = None
    days_until_due: Optional[int] = None # Campo calculado para el dashboard

    class Config:
        from_attributes = True
        json_encoders = {
            date: lambda v: v.isoformat()
        }
