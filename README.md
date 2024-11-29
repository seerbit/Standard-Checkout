# SeerBit Standard Checkout Integration with FastAPI

This project demonstrates a secure and efficient approach to implementing payment functionality using the SeerBit Standard Checkout API. Built with FastAPI and MongoDB, this application is designed to simplify the process of creating and managing online payments, making it ideal for developers working on financial integrations.

---

## **Features**
- **Payment Initialization**: Create and initialize payments securely using [SeerBit's Standard Checkout API](https://doc.seerbit.com/online-payment/integration-type/standard-checkout).
- **MongoDB Integration**: Store and manage payment records in a robust database for easy retrieval and tracking.
- **RESTful API**: A FastAPI-powered API to handle payment requests with structured validation using Pydantic.

---

## **Tech Stack**
- **[FastAPI](https://fastapi.tiangolo.com/tutorial/)**: A modern, high-performance web framework for building APIs.
- **[SeerBit Standard Checkout API](https://doc.seerbit.com/online-payment/integration-type/standard-checkout)**: A reliable payment API for initiating and managing transactions.
- **[MongoDB](https://www.mongodb.com/)**: A NoSQL database for efficient data storage and management.
- **[Pydantic](https://docs.pydantic.dev/latest/)**: Used for data validation and serialization.
- **[Requests](https://pypi.org/project/requests/)**: Handles HTTP communication with external APIs.
- **[Python Dotenv](https://pypi.org/project/python-dotenv/)**: Manages environment variables for secure configuration.

---

## **Getting Started**

### **Prerequisites**
- Python 3.8 or higher
- A running MongoDB instance (local or cloud-based)
- SeerBit API credentials (Public Key, Encrypted Key, and API URL)
- `.env` file containing the following environment variables:
  ```env
  DATABASE_URL="your_mongodb_connection_string"
  SEERBIT_PAYMENT_API="seerbit_standard_checkout_url"
  ENCRYPTED_KEY="your_seerbit_encrypted_key"
  PUBLIC_KEY="your_public_key"
  ```

---

### **Installation**

1. **Clone the Repository**  
   ```bash
   git clone https://github.com/your-repo/seerbit-fastapi-checkout.git
   cd seerbit-fastapi-checkout
   ```

2. **Install Dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Environment Variables**  
   Create a `.env` file in the project root and add the required keys as shown in the prerequisites.

4. **Start the Application**  
   ```bash
   fastapi dev app.py
   ```

5. **Access the API Documentation**  
   Navigate to [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) to explore and test the endpoints using FastAPI's Swagger UI.

---

## **API Endpoints**

### **1. Create Checkout**
- **Endpoint**: `/checkout/create`  
- **Method**: POST  
- **Request Body**:
  ```json
  {
    "amount": 1000,
    "currency": "NGN",
    "country": "NG",
    "paymentReference": "unique_reference",
    "email": "user@example.com",
    "fullName": "User Name",
    "tokenize": false,
    "callbackUrl": "https://your-callback-url.com"
  }
  ```
- **Response**:
  - **Success**:  
    ```json
    {
      "Message": "Payment is successful!"
    }
    ```
  - **Failure**: Returns an HTTP error with the status code and error details.

---

## **How It Works**
1. **Payment Initialization**:  
   - The client sends payment details to the `/checkout/create` endpoint.  
   - The app validates the data and sends it to the SeerBit API with the necessary headers.  
   - On successful response from SeerBit, the payment data is stored in MongoDB.

2. **Error Handling**:  
   - API failures are captured, and meaningful error messages are returned to the client.  
   - Database insertion errors are also handled gracefully.

3. **Data Security**:  
   - Sensitive keys are stored securely in environment variables.
   - The app uses HTTPS for secure API communication.

---

## **Notes**
- Ensure your MongoDB instance is accessible and properly configured.
- Use a valid `paymentReference` for unique transaction identification.
- Configure your SeerBit callback URL to handle post-payment actions effectively.

---

## **Contributions**
We welcome contributions! Feel free to fork the repository, raise issues, or submit pull requests to improve this project.

---

## **License**
This project is open-source and available under the [MIT License](LICENSE).
