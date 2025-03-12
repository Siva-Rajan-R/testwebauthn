from fastapi import APIRouter,HTTPException,Depends,Form
from fastapi.responses import JSONResponse
from database.main import get_db_session
from sqlalchemy.orm import Session
from database.models import Resources,ProtectedResourcesAccessCredentials
from icecream import ic

router=APIRouter(
    tags=["Add resources information"]
)

@router.post("/resources/add")
def add_resources(
        resource:str=Form(...),
        is_protected:bool=Form(...),
        session:Session=Depends(get_db_session)
):
    try:
        with session.begin():
            session.add(
                Resources(
                    resource=resource,
                    is_protected=is_protected
                )
            )

            return JSONResponse(
                status_code=201,
                content="successfully resources added"
            )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"something went wrong : {e}"
        )
    
@router.post("/resources/add/credentials")
def add_resources_credentials(
    latitude:float=Form(...),
    longitude:float=Form(...),
    ip_address:str=Form(...),
    session:Session=Depends(get_db_session)
):
    try:
        with session.begin():
            session.add(
                ProtectedResourcesAccessCredentials(
                    latitude=latitude,
                    longitude=longitude,
                    ip_address=ip_address
                )
            )

            return JSONResponse(
                status_code=201,
                content="Successfully added resource credentials"
            )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"something went wrong : {e}"
        )
    


    