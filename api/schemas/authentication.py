from pydantic import BaseModel,EmailStr

class Authenticate(BaseModel):
    employee_email:EmailStr
    employee_name:str

class Verify(BaseModel):
    employee_email:EmailStr
    employee_name:str
    credentials:dict
    latitude:float
    longitude:float