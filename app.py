from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from bson import ObjectId
from dotenv import load_dotenv
import requests
import pymongo
import os

#Load environment variables from .env file
load_dotenv()

app = FastAPI()

# MongoDB Setup
database_url = os.getenv('DATABASE_URL')
client = pymongo.MongoClient(database_url)
db = client["standard_checkout_db"]
standard_checkout_collection = db["checkout"]

# SeerBit API endpoint and authorization
seerbit_standard_checkout = os.getenv('SEERBIT_PAYMENT_API')
encrypted_key = os.getenv('ENCRYPTED_KEY')

class StandardCheckout(BaseModel):
    amount: int
    currency: str
    country: str
    paymentReference: str
    email: str
    fullName: str
    tokenize: bool
    callbackUrl: str
public_key = os.getenv('PUBLIC_KEY')
if not public_key:
         raise RuntimeError("PUBLIC_KEY environment variable is not set")

# Create the Standard Checkout Endpoint
@app.post("/checkout/create")
def create_checkout(checkout: StandardCheckout):
    checkout_data = {
        "publicKey": public_key,
        "amount": checkout.amount,
        "currency": checkout.currency,
        "country": checkout.country,
        "paymentReference": checkout.paymentReference,
        "email": checkout.email,
        "fullName": checkout.fullName,
        "tokenize": checkout.tokenize,
        "callbackUrl": checkout.callbackUrl
    }

    headers = {
    "Authorization": f"Bearer {encrypted_key}",
    "Content-Type": "application/json"
    }

    # Send POST request to Standard Checkout API
    response =  requests.post(f"{seerbit_standard_checkout}", json=checkout_data, headers=headers)

    if response.status_code == 200:
        try:
            standard_checkout_collection.insert_one(checkout_data)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Database insertion failed: {str(e)}")
        return {"Message": "Payment is successful!"}
    else: 
        raise HTTPException(status_code=response.status_code, detail=f"Payment not initialized successfully: {response.text}")