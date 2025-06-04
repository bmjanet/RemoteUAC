# backend/app/utils/auth.py
from datetime import datetime, timedelta
from jose import JWTError, jwt
from typing import Optional

SECRET_KEY = "I-Love-My-Girlfriend"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # Change if needed, 60 minutes is default AS OF creation

# Generate a JWT token with an expiration time.
# It copies the data to avoid modifitiyng the original dictionary.
# It will expire based on the provided timedelta or default to the defined minutes above.
# Encodes the data as a JWT token using the secret key and algorithm.
#
# Params:
# - data: Dictionary containing the payload for the token.
# - expires_delta: Optional timedelta for custom expiration time.
# # Returns:
# - A string representing the encoded JWT token.
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Verify a JWT token and return the payload if valid.
# If the token is invalid or expired, it returns None.
#
# Params:
# - token: The JWT token to verify.
# Returns:
# - A dictionary containing the decoded payload if the token is valid, or None if invalid.
def verify_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload  # Return the decoded payload if verification is successful
    except JWTError:
        return None  # Return None if the token is invalid or expired
