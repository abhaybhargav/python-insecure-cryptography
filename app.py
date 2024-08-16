import os
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from Crypto.Cipher import DES3, AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import base64
import json
import logging

app = FastAPI()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# In-memory user storage
users = {}

# Encryption key (insecure: hard-coded for demonstration)
DES3_KEY = b'insecurekey1insecurekey2'  # 24 bytes for 3DES
AES_KEY = get_random_bytes(32)  # 32 bytes for AES-256

class User(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    message: str

def get_secure_mode():
    return os.getenv("SECURE_MODE", "false").lower() == "true"

def encrypt_3des(data: str) -> str:
    cipher = DES3.new(DES3_KEY, DES3.MODE_ECB)
    padded_data = pad(data.encode(), DES3.block_size)
    encrypted = cipher.encrypt(padded_data)
    return base64.b64encode(encrypted).decode()

def decrypt_3des(encrypted_data: str) -> str:
    cipher = DES3.new(DES3_KEY, DES3.MODE_ECB)
    encrypted = base64.b64decode(encrypted_data)
    decrypted = cipher.decrypt(encrypted)
    return unpad(decrypted, DES3.block_size).decode()

def encrypt_aes(data: str) -> str:
    cipher = AES.new(AES_KEY, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(data.encode())
    return base64.b64encode(cipher.nonce + tag + ciphertext).decode()

def decrypt_aes(encrypted_data: str) -> str:
    encrypted = base64.b64decode(encrypted_data)
    nonce, tag, ciphertext = encrypted[:16], encrypted[16:32], encrypted[32:]
    cipher = AES.new(AES_KEY, AES.MODE_GCM, nonce=nonce)
    return cipher.decrypt_and_verify(ciphertext, tag).decode()

@app.post("/signup")
async def signup(user: User, secure: bool = Depends(get_secure_mode)):
    if user.username in users:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    if secure:
        encrypted_password = encrypt_aes(user.password)
    else:
        encrypted_password = encrypt_3des(user.password)
    
    users[user.username] = encrypted_password
    return {"message": "User created successfully"}

@app.post("/login", response_model=LoginResponse)
async def login(user: User, secure: bool = Depends(get_secure_mode)):
    if user.username not in users:
        raise HTTPException(status_code=400, detail="User not found")
    
    stored_password = users[user.username]
    
    if secure:
        decrypted_password = decrypt_aes(stored_password)
    else:
        decrypted_password = decrypt_3des(stored_password)
    
    if user.password != decrypted_password:
        raise HTTPException(status_code=400, detail="Incorrect password")
    
    # Log the encrypted password (insecure practice for demonstration)
    logger.info(f"User {user.username} logged in. Encrypted password: {stored_password}")
    
    return {"message": "Login successful"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8880)