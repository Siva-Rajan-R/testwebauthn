import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from fastapi import APIRouter,HTTPException,Depends,BackgroundTasks,Query,Response,Request
from fastapi.responses import JSONResponse
from webauthn import generate_registration_options,verify_registration_response,options_to_json
from webauthn.helpers.structs import AuthenticatorSelectionCriteria,AuthenticatorAttachment,AttestationConveyancePreference
from ..schemas.resgisteration import Register,Verify
from database.operation import RegisterWebauthnEmployee,Session
from database.main import get_db_session
import secrets
import uuid
from icecream import ic
from ..dependencies.email import accept_email,forgot_email
from ..dependencies.greet import register_accept_greet,forgot_accept_greet,NOT_FOUND
import time
import base64
from redis import Redis
import json

# from dotenv import load_dotenv
# load_dotenv()

RP_ID=os.getenv("RP_ID")
RP_NAME=os.getenv("RP_NAME")
EXPECTED_ORIGIN=os.getenv("EXPECTED_ORIGIN")
EXPECTED_RP_ID=os.getenv("EXPECTED_RP_ID")
REDIS_SERVER_URL=os.getenv("REDIS_SERVER_URL")


router=APIRouter(
    tags=["Webauthn Register"]
)

# challenges=dict()
# waiting_lis=dict()


@router.post("/employee/registeration")
async def register_employee(details:Register,session:Session=Depends(get_db_session)):
    try:
        obj=RegisterWebauthnEmployee(
            session=session,
            employee_name=details.employee_name,
            employee_email=details.employee_email,
        )
        if details.is_forgot:
            await obj.is_employee_exists()
        else:
            await obj.is_employee_notexists()

        options=generate_registration_options(
            rp_id=RP_ID,
            rp_name=RP_NAME,
            user_id=secrets.token_bytes(16),
            user_name=details.employee_email,
            user_display_name=details.employee_name,
            challenge=secrets.token_bytes(32),
            authenticator_selection=AuthenticatorSelectionCriteria(
                authenticator_attachment=AuthenticatorAttachment.PLATFORM
            ),attestation=AttestationConveyancePreference.DIRECT
        )

        ic(options)
        #to store challenge
        redis_cache=Redis.from_url(REDIS_SERVER_URL)
        redis_cache.set(details.employee_email,options.challenge)

        #challenges[details.employee_email]=options.challenge
        return options_to_json(options)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"something went wrong --> details : {e}"
        )

@router.post("/employee/registeration/verify")
async def employee_verify(details:Verify,bgt:BackgroundTasks,request:Request):
    raw_id=details.credentials.get("rawId",0)
    #challenges.get(details.employee_email,0)
    redis_cache=Redis.from_url(REDIS_SERVER_URL)
    ex_challenge=redis_cache.get(details.employee_email)
    ic("hello wrold")
    ic(ex_challenge)
    if not raw_id or not ex_challenge:
        raise HTTPException(
            status_code=404,
            detail="raw id or challenge not found"
        )
    details.credentials["raw_id"]=raw_id

    try:
        response=verify_registration_response(
            credential=details.credentials,
            expected_challenge=ex_challenge,
            expected_origin=EXPECTED_ORIGIN,
            expected_rp_id=EXPECTED_RP_ID
        )
        ic(response)

        #to delete challenge
        redis_cache.delete(details.employee_email)
        #del challenges[details.employee_email]
        
        link_id=str(uuid.uuid5(uuid.uuid4(),details.employee_email))

        # waiting_lis[link_id]={
        #     "employee_email":details.employee_email,
        #     "employee_name":details.employee_name,
        #     "public_key":response.credential_public_key,
        #     "sign_count":response.sign_count,
        #     "aaguid":response.aaguid,
        #     "credential_id":response.credential_id
        # }

        credentials={
            "employee_email":details.employee_email,
            "employee_name":details.employee_name,
            "public_key":base64.b64encode(response.credential_public_key).decode("utf-8"),
            "sign_count":response.sign_count,
            "aaguid":response.aaguid,
            "credential_id":base64.b64encode(response.credential_id).decode("utf-8")
        }
        ic("next")
        redis_cache.setex(link_id,120,json.dumps(credentials))
        ic("i think so")
        href=f"{request.base_url}employee/registeration/store/{link_id}"
        ic(href)
        if details.is_forgot:
            bgt.add_task(forgot_email,href,details.employee_email,details.employee_name)
        else:
            bgt.add_task(accept_email,href,details.employee_email,details.employee_name)

        return JSONResponse(
            status_code=200,
            content="registered successfully waiting for conformation"
        )
    
    except HTTPException:
        raise
    except Exception as e:
        ic(e)
        raise HTTPException(
            status_code=500,
            detail=f"something went wrong --> details : {e}"
        )

@router.get("/employee/registeration/store/{link_id}")
async def store_employee_register(link_id:str,bgt:BackgroundTasks,session:Session=Depends(get_db_session),is_forgot:bool=Query(False)):
    #waiting_lis.get(link_id)
    redis_cache=Redis.from_url(REDIS_SERVER_URL)
    registeration_cred=redis_cache.get(link_id)
    if registeration_cred:
        registeration_cred=json.loads(registeration_cred)
        ic(registeration_cred)
        if registeration_cred:
            ic("hello from stored",registeration_cred)
            obj=RegisterWebauthnEmployee(
                    session=session,
                    employee_name=registeration_cred.get("employee_name"),
                    employee_email=registeration_cred.get("employee_email"),
                )
            
            if is_forgot:
                greet_content=forgot_accept_greet(registeration_cred.get("employee_email"),registeration_cred.get("employee_name"))
                bgt.add_task(
                    obj.update_registered_employee,
                    base64.b64decode(registeration_cred.get("credential_id")),
                    base64.b64decode(registeration_cred.get("public_key")),
                    registeration_cred.get("sign_count"),
                    registeration_cred.get("aaguid")
                )
            else:
                greet_content=register_accept_greet(registeration_cred.get("employee_email"),registeration_cred.get("employee_name"))
                bgt.add_task(
                    obj.add_registered_employee,
                    base64.b64decode(registeration_cred.get("credential_id")),
                    base64.b64decode(registeration_cred.get("public_key")),
                    registeration_cred.get("sign_count"),
                    registeration_cred.get("aaguid")
                )

            #del waiting_lis[link_id]
            redis_cache.delete(link_id)
            return Response(content=greet_content,media_type="text/html")
    return Response(
        status_code=404,
        content=NOT_FOUND,
        media_type="text/html"
    )


