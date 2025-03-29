import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
import os
from fastapi import APIRouter,HTTPException,Depends,BackgroundTasks,Request
from webauthn import generate_authentication_options,verify_authentication_response,options_to_json
from webauthn.helpers.structs import UserVerificationRequirement
from ..schemas.authentication import Authenticate,Verify
from database.operation import AuthenticationWebauthnEmployee,Session
from database.main import get_db_session
import secrets
from redis import Redis
import json
from icecream import ic
from dotenv import load_dotenv
load_dotenv()

RP_ID=os.getenv("RP_ID")
RP_NAME=os.getenv("RP_NAME")
EXPECTED_ORIGIN=os.getenv("EXPECTED_ORIGIN")
EXPECTED_RP_ID=os.getenv("EXPECTED_RP_ID")
REDIS_SERVER_URL=os.getenv("REDIS_SERVER_URL")


router=APIRouter(
    tags=["Webauthn Authentication"]
)

# challenges={}

@router.post("/employee/authentication")
async def employee_authentication(details:Authenticate,session:Session=Depends(get_db_session)):
    await AuthenticationWebauthnEmployee(
        session,
        employee_email=details.employee_email,
        employee_name=details.employee_name
    ).is_employee_exists()

    try:
        options=generate_authentication_options(
            rp_id=RP_ID,
            challenge=secrets.token_bytes(64),
            user_verification=UserVerificationRequirement.REQUIRED,
        )
        ic(options)

        #challenges[details.employee_email]=options.challenge
        redis_cache=Redis.from_url(REDIS_SERVER_URL)
        redis_cache.set(details.employee_email,options.challenge)
        return options_to_json(options)
    
    except HTTPException:
        raise
    except Exception as e:
        ic(e)
        raise HTTPException(
            status_code=500,
            detail=f"somenthing went wrong {e}"
        )

@router.post("/employee/authentication/verify")
async def employee_authentication_verify(details:Verify,request:Request,bgt:BackgroundTasks,session:Session=Depends(get_db_session)):
    ic(request.client.host,details.latitude,details.longitude)
    #challenges.get(details.employee_email,0)
    redis_cache=Redis.from_url(REDIS_SERVER_URL)
    ex_challenge=redis_cache.get(details.employee_email)
    raw_id=details.credentials.get("rawId",0)
    if not raw_id or not ex_challenge:
        raise HTTPException(
            status_code=404,
            detail="raw id or employee not found"
        )
    details.credentials["raw_id"]=raw_id
    obj=AuthenticationWebauthnEmployee(
        session=session,
        employee_email=details.employee_email,
        employee_name=details.employee_name
    )
    credentials=await obj.get_credentials()
    ic(credentials)
    ic(credentials[0])
    try:
        response=verify_authentication_response(
            credential=details.credentials,
            expected_challenge=ex_challenge,
            expected_origin=EXPECTED_ORIGIN,
            expected_rp_id=EXPECTED_RP_ID,
            credential_public_key=credentials[0].get("public_key"),
            credential_current_sign_count=credentials[0].get("sign_count")
        )

        #del challenges[details.employee_email]
        redis_cache.delete(details.employee_email)
        bgt.add_task(obj.update_sign_count,response.new_sign_count,credentials[0].get("employee_id"))
        resource=await obj.is_employee_eligible(details.latitude,details.longitude,request.client.host)
        ic(request.client.host,resource)
        return resource
    except HTTPException:
        raise
    except Exception as e:
        ic(e)
        raise HTTPException(        
                status_code=500,
                detail=f"somenthing went wrong {e}"
            )
