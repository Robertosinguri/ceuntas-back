import firebase_admin
from firebase_admin import credentials, firestore
import os
from dotenv import load_dotenv

load_dotenv()

# La ruta al archivo JSON que descargas de Firebase Console
SERVICE_ACCOUNT_PATH = os.getenv("FIREBASE_SERVICE_ACCOUNT", "serviceAccountKey.json")

def init_firebase():
    if not firebase_admin._apps:
        cred = credentials.Certificate(SERVICE_ACCOUNT_PATH)
        firebase_admin.initialize_app(cred)
    
    return firestore.client()

# Dependencia para obtener el cliente de Firestore
def get_db():
    db = init_firebase()
    return db
