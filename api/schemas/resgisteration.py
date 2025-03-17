from pydantic import BaseModel,EmailStr
from typing import Optional

class Register(BaseModel):
    employee_email:EmailStr
    employee_name:str
    is_forgot:Optional[bool]=False

class Verify(BaseModel):
    credentials:dict
    employee_email:EmailStr
    employee_name:str
    is_forgot:Optional[bool]=False