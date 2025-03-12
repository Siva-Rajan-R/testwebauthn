from sqlalchemy.orm import declarative_base,sessionmaker
from sqlalchemy import create_engine
import os
"""from dotenv import load_dotenv
load_dotenv()"""

Engine=create_engine(os.getenv("DATABASE_URL"))
Base=declarative_base()

def get_db_session():
    Session=sessionmaker(bind=Engine)
    session=Session()
    try:
        yield session
    finally:
       session.close()
