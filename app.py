from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from bson import ObjectId
from dotenv import load_dotenv
import requests
import pymongo
import os

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

# MongoDB Setup
database_url = os.getenv('DATABASE_URL')
client = pymongo.MongoClient(database_url)
db = client["standard_checkout_db"]
standard_checkout_collection = db["checkout"]

# SeerBit API endpoint and authorization
seerbit_payment_api = os.getenv('SEERBIT_PAYMENT_API')
encrypted_key = os.getenv('ENCRYPTED_KEY')
public_key = os.getenv('PUBLIC_KEY')

if not public_key:
    raise RuntimeError("PUBLIC_KEY environment variable is not set")
if not encrypted_key:
    raise RuntimeError("ENCRYPTED_KEY environment variable is not set")
if not seerbit_payment_api:
    raise RuntimeError("SEERBIT_PAYMENT_API environment variable is not set")

class StandardCheckout(BaseModel):
    amount: float
    currency: str
    country: str
    paymentReference: str
    email: str
    fullName: str
    tokenize: bool
    callbackUrl: str

@app.post("/checkout/create")
def create_checkout(checkout: StandardCheckout):
    checkout_data = {
        "publicKey": public_key,
        "amount": str(checkout.amount),  # Ensure amount is passed as a string
        "currency": checkout.currency,
        "country": checkout.country,
        "paymentReference": checkout.paymentReference,
        "email": checkout.email,
        "fullName": checkout.fullName,
        "tokenize": str(checkout.tokenize).lower(),  # Convert to string as expected by SeerBit
        "callbackUrl": checkout.callbackUrl
    }

    headers = {
        "Authorization": f"Bearer {encrypted_key}",
        "Content-Type": "application/json"
    }

    # Send POST request to SeerBit API
    response = requests.post(seerbit_payment_api, json=checkout_data, headers=headers)

    if response.status_code == 200:
        response_data = response.json()
        if response_data.get("status") == "SUCCESS":
            # Save to MongoDB
            try:
                standard_checkout_collection.insert_one(checkout_data)
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Database insertion failed: {str(e)}")
            # Return the response message and redirect link
            return {
                "message": response_data["data"].get("message", "Successful"),
                "redirectLink": response_data["data"]["payments"]["redirectLink"]
            }
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Payment status not successful: {response_data.get('message', 'Unknown Error')}"
            )
    else:
        raise HTTPException(
            status_code=response.status_code,
            detail=f"Payment initialization failed: {response.text}"
        )
