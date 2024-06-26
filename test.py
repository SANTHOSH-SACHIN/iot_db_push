from fastapi import FastAPI
from pydantic import BaseModel
# import psycopg2
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware
import firebase_admin
from firebase_admin import credentials, firestore
import random
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)



cred = credentials.Certificate('hypox-dtect-firebase.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

class Reading(BaseModel):
    bpm: float
    sp02: int

@app.post("/reading")
async def create_reading(reading: Reading):
    try:
        
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")

        # Create a new document in Firestore
        doc_ref = db.collection('sensor_readings').document(timestamp)
        doc_ref.set({
            'reading_num': timestamp,
            'bpm': reading.bpm,
            'sp02': reading.sp02
        })
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "detail": str(e)}
