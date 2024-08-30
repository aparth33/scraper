from fastapi import HTTPException, Security
from fastapi.security.api_key import APIKeyHeader

API_KEY = "my_static_token"
api_key_header = APIKeyHeader(name="Authorization")

def get_current_user(api_key: str = Security(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Could not validate credentials")
    return api_key
