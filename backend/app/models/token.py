"""
Creating a token model using Pydantic.
# backend/app/models/token.py
This module defines a Pydantic model for handling tokens in the application.
"""

from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str