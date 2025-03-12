from database.models import Employee,WebAuthnCredential,Resources,ProtectedResourcesAccessCredentials
from sqlalchemy import select,exists
from sqlalchemy.orm import Session
from pydantic import EmailStr
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
import uuid
from icecream import ic
from geopy.distance import geodesic

class __RegisterInput:
    def __init__(self,session:Session,employee_name:str,employee_email:EmailStr):
        self.session=session
        self.employee_name = employee_name
        self.employee_email = employee_email

class RegisterWebauthnEmployee(__RegisterInput):
    async def is_employee_notexists(self):
        if self.session.execute(select(Employee.employee_email).where(Employee.employee_email==self.employee_email)).scalar_one_or_none():
            raise HTTPException(
                status_code=409,
                detail="employee already exists"
            )
        return True
    
    async def add_registered_employee(self,credential_id:str,public_key:bytes,sign_count:int,aaguid:str):
        try:
            with self.session.begin():
                await self.is_employee_notexists()

                employee_id=str(uuid.uuid5(uuid.uuid4(),self.employee_email))
                employee=Employee(
                    employee_id = employee_id,
                    employee_name = self.employee_name,
                    employee_email = self.employee_email,
                )

                webauthnncred=WebAuthnCredential(
                    employee_id = employee_id,
                    credential_id = credential_id,
                    public_key = public_key,
                    sign_count = sign_count,
                    aaguid = aaguid
                )

                self.session.add_all([employee,webauthnncred])

                return JSONResponse(
                    status_code=201,
                    content="successfully employee registerd"
                )
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"someething went wrong --> details : {e}"
            )
        
class __AuthenticationInputs:
    def __init__(self,session:Session,employee_email,employee_name):
        self.session=session
        self.employee_email=employee_email
        self.employee_name=employee_name
        
class AuthenticationWebauthnEmployee(__AuthenticationInputs):
    async def is_employee_exists(self):
        verify=self.session.execute(select(Employee.employee_id).where(Employee.employee_email==self.employee_email,Employee.employee_name==self.employee_name)).scalar()
        if not verify:
            raise HTTPException(
                status_code=404,
                detail="employee not found"
            )
        return verify
    
    async def get_credentials(self):
        employee_id=await self.is_employee_exists()
        cred=self.session.execute(
            select(
                WebAuthnCredential.credential_id,
                WebAuthnCredential.aaguid,
                WebAuthnCredential.public_key,
                WebAuthnCredential.sign_count,
                WebAuthnCredential.employee_id
            )
            .where(WebAuthnCredential.employee_id==employee_id)
        ).mappings().all()

        return cred
        
    async def update_sign_count(self,new_sign_count:int,employee_id:str):
        try:
            with self.session.begin():
                if self.session.execute(select(WebAuthnCredential.sign_count).where(WebAuthnCredential.employee_id==employee_id)).scalar_one_or_none()==new_sign_count:
                    ic("409 : the new sign count is already exists")
                self.session.query(WebAuthnCredential).filter(WebAuthnCredential.employee_id==employee_id).update(
                    {
                        WebAuthnCredential.sign_count:new_sign_count
                    }
                )

                return JSONResponse(
                    status_code=200,
                    content="successfully updated"
                )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"something went wrong : {e}"
            )
    
    async def is_employee_eligible(self,latitude:float,longitude:float,ip_address):
        try:
            access_latitude,access_longitude=self.session.execute(select(ProtectedResourcesAccessCredentials.latitude,ProtectedResourcesAccessCredentials.longitude)).all()[0]
            ic(access_latitude,access_longitude)
            geo=geodesic((latitude,longitude),(access_latitude,access_longitude)).kilometers
            ic(geo)

            if self.session.query(
                exists().where(
                    ProtectedResourcesAccessCredentials.ip_address==ip_address
                )
            ).scalar() and geo<=1:
                
                resources=self.session.execute(
                    select(
                        Resources.resource,
                        Resources.is_protected
                    )
                ).mappings().all()

                return {
                    "accessibility_scope":"both protected and unprotected resources",
                    "resources":resources
                }

            resources=self.session.execute(
                    select(
                        Resources.resource,
                        Resources.is_protected
                    ).where(
                        Resources.is_protected==False
                    )
                ).mappings().all()
            return {
                    "accessibility_scope":"unprotected resources only",
                    "resources":resources
                }
        
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"something went wrong : {e}"
            ) 
    
    
