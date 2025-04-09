from pydantic import BaseModel, Field, EmailStr

class LoginSchema(BaseModel):
    email: EmailStr
    senha: str