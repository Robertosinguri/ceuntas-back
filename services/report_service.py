from google.cloud.firestore import Client
from repositories.bill_repository import BillRepository
import pandas as pd

class ReportService:
    def __init__(self, repository: BillRepository):
        self.repository = repository

    def generate_annual_report(self, db: Client, user_id: str):
        bills = self.repository.get_all(db, user_id)
        import datetime
        current_year = datetime.date.today().year
        months_keys = [f"{current_year}-{str(m).zfill(2)}" for m in range(1, 13)]
        month_labels = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]

        if not bills:
            return {"labels": month_labels, "monthly_totals": [0]*12, "lines": []}

        df = pd.DataFrame(bills)
        
        # Asumiendo que 'due_date' existe y es string o date
        df['due_date'] = pd.to_datetime(df['due_date'])
        
        # Limitar al año actual
        df = df[df['due_date'].dt.year == current_year]
        if df.empty:
            return {"labels": month_labels, "monthly_totals": [0]*12, "lines": []}

        # Crear columna de Mes_Año para agrupar
        df['month'] = df['due_date'].dt.strftime('%Y-%m')

        current_month_index = datetime.date.today().month - 1

        # 1. Agrupar totales por mes
        monthly_total_raw = df.groupby('month')['amount'].sum().reindex(months_keys, fill_value=0).tolist()
        # Para el total, simplemente evitamos que caiga a 0 en el futuro
        monthly_total = [val if i <= current_month_index else None for i, val in enumerate(monthly_total_raw)]

        # 2. Agrupar por factura (name) a lo largo de los meses
        lines = []
        for name, group in df.groupby('name'):
            monthly_sum_raw = group.groupby('month')['amount'].sum().reindex(months_keys, fill_value=0).tolist()
            monthly_sum = []
            
            for i, val in enumerate(monthly_sum_raw):
                if i > current_month_index:
                    # Cortar gráfica para meses que aún no han pasado
                    monthly_sum.append(None)
                else:
                    if val != 0:
                        monthly_sum.append(val)
                    else:
                        # Para meses intermedios en el pasado donde no hubo pago, usamos None
                        # El frontend unirá los puntos visualmente con una línea punteada
                        monthly_sum.append(None)

            lines.append({
                "label": name,
                "data": monthly_sum
            })
        # 3. Acumulado anual por mes
        cumulative_totals_raw = df.groupby('month')['amount'].sum().reindex(months_keys, fill_value=0).cumsum().tolist()
        cumulative_totals = [val if i <= current_month_index else None for i, val in enumerate(cumulative_totals_raw)]

        return {
            "labels": month_labels,
            "monthly_totals": monthly_total,
            "cumulative_totals": cumulative_totals,
            "lines": lines
        }
