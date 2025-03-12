from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from routes import registeration,authentication,resources

app=FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)
app.include_router(registeration.router)

app.include_router(authentication.router)

app.include_router(resources.router)
    
