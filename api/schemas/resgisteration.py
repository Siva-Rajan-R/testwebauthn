from pydantic import BaseModel,EmailStr

class Register(BaseModel):
    employee_email:EmailStr
    employee_name:str

class Verify(BaseModel):
    credentials:dict
    employee_email:EmailStr
    employee_name:str