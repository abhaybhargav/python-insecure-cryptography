# Insecure Encryption Practices Demo

This project demonstrates insecure encryption practices using a FastAPI application. It's designed for educational purposes to showcase the differences between secure and insecure encryption methods.

**Warning**: This application intentionally uses insecure practices and should never be used in a production environment.

## Features

- User signup and login API endpoints
- Insecure mode: 3DES encryption in ECB mode
- Secure mode: AES-256 encryption in GCM mode
- In-memory user storage
- Docker containerization

## Prerequisites

- Docker
- Python 3.9+ (for local development)

## Setup

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/insecure-encryption-demo.git
   cd insecure-encryption-demo
   ```

2. Build the Docker image:
   ```
   docker build -t insecure-encryption-demo .
   ```

## Running the Application

### Insecure Mode (Default)

To run the application in insecure mode (using 3DES in ECB mode):

```
docker run -p 8880:8880 insecure-encryption-demo
```

### Secure Mode

To run the application in secure mode (using AES-256 in GCM mode):

```
docker run -p 8880:8880 -e SECURE_MODE=true insecure-encryption-demo
```

The application will be accessible at `http://localhost:8880`.

## API Endpoints

### Signup

- URL: `/signup`
- Method: POST
- Body:
  ```json
  {
    "username": "testuser",
    "password": "testpassword"
  }
  ```

### Login

- URL: `/login`
- Method: POST
- Body:
  ```json
  {
    "username": "testuser",
    "password": "testpassword"
  }
  ```

## Testing the API

You can use curl or any API testing tool like Postman to test the endpoints.

1. Signup a new user:
   ```
   curl -X POST http://localhost:8880/signup -H "Content-Type: application/json" -d '{"username": "testuser", "password": "testpassword"}'
   ```

2. Login with the created user:
   ```
   curl -X POST http://localhost:8880/signup -H "Content-Type: application/json" -d '{"username": "testuser", "password": "testpassword"}'
   ```

## Security Considerations

This application demonstrates the following insecure practices:

1. Use of 3DES in ECB mode (in insecure mode)
2. Hard-coded encryption key for 3DES
3. Logging of encrypted passwords

In a real-world scenario, these practices would be severe security risks. Always use secure encryption methods, proper key management, and never log sensitive information like passwords.

## Development

For local development without Docker:

1. Install dependencies:
   ```
   pip install fastapi uvicorn pycryptodome
   ```

2. Run the application:
   ```
   python app.py
   ```

To run in secure mode locally, set the `SECURE_MODE` environment variable:

```
SECURE_MODE=true python app.py
```

## License

This project is for educational purposes only. Use at your own risk.