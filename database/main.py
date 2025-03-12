from sqlalchemy.orm import declarative_base,sessionmaker
from sqlalchemy import create_engine


Engine=create_engine("postgresql://webauthdatabase_owner:npg_nRtUs85qDNYL@ep-empty-brook-a1ua68v1-pooler.ap-southeast-1.aws.neon.tech/webauthdatabase")
Base=declarative_base()

def get_db_session():
    Session=sessionmaker(bind=Engine)
    session=Session()
    try:
        yield session
    finally:
       session.close()
