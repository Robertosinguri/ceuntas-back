from fastapi import FastAPI
from routers import bill_router, report_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Cuentas Backend (Firebase Edition)", 
    description="Backend modular con Firestore para el control de cuentas."
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:4200", 
        "http://127.0.0.1:4200",
        "https://cuentas-40610.web.app",
        "https://cuentas-40610.firebaseapp.com",
        "https://api-cuentas.rsdev.dev"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Cuentas API con Firebase está corriendo!"}

# Incluir los routers
app.include_router(bill_router.router, prefix="/api/v1")
app.include_router(report_router.router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
