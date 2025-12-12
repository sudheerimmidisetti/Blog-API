# schemas.py
from pydantic import BaseModel, EmailStr
from typing import List, Optional

# --- Author Schemas ---
class AuthorBase(BaseModel):
    name: str
    email: EmailStr

class AuthorCreate(AuthorBase):
    pass

class AuthorResponse(AuthorBase):
    id: int
    # orm_mode tells Pydantic to read data even if it's not a dict, but an ORM model
    class Config:
        from_attributes = True

# --- Post Schemas ---
class PostBase(BaseModel):
    title: str
    content: str

class PostCreate(PostBase):
    author_id: int

class PostResponse(PostBase):
    id: int
    author_id: int
    # We include the Author object nested inside the Post response
    author: AuthorResponse 

    class Config:
        from_attributes = True