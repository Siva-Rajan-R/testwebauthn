import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from fastapi import APIRouter,HTTPException,Depends
from webauthn import generate_registration_options,verify_registration_response,options_to_json
from webauthn.helpers.structs import AuthenticatorSelectionCriteria,AuthenticatorAttachment,AttestationConveyancePreference
from ..schemas.resgisteration import Register,Verify
from database.operation import RegisterWebauthnEmployee,Session
from database.main import get_db_session
import secrets
from icecream import ic
from dotenv import load_dotenv
load_dotenv()

RP_ID=os.getenv("RP_ID")
RP_NAME=os.getenv("RP_NAME")
EXPECTED_ORIGIN=os.getenv("EXPECTED_ORIGIN")
EXPECTED_RP_ID=os.getenv("EXPECTED_RP_ID")

router=APIRouter(
    tags=["Webauthn Register"]
)

challenges=dict()

@router.post("/employee/registeration")
async def register_employee(details:Register,session:Session=Depends(get_db_session)):
    try:
        await RegisterWebauthnEmployee(
            session=session,
            employee_name=details.employee_name,
            employee_email=details.employee_email,
        ).is_employee_notexists()

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
        challenges[details.employee_email]=options.challenge
        return options_to_json(options)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"something went wrong --> details : {e}"
        )

@router.post("/employee/registeration/verify")
async def employee_verify(details:Verify,session:Session=Depends(get_db_session)):
    raw_id=details.credentials.get("rawId",0)
    ex_challenge=challenges.get(details.employee_email,0)
    
    if not raw_id or not challenges:
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

        del challenges[details.employee_email]

        return await RegisterWebauthnEmployee(
            session=session,
            employee_name=details.employee_name,
            employee_email=details.employee_email,
        ).add_registered_employee(
            public_key=response.credential_public_key,
            sign_count=response.sign_count,
            aaguid=response.aaguid,
            credential_id=response.credential_id
        )
    except HTTPException:
        raise
    except Exception as e:
        ic(e)
        raise HTTPException(
            status_code=500,
            detail=f"something went wrong --> details : {e}"
        )


