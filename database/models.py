from database.main import Engine,Base
from sqlalchemy import Column, Integer, String, Boolean,ForeignKey,LargeBinary,Float
from sqlalchemy.orm import relationship

class Employee(Base):
    __tablename__ = "employee"

    employee_id = Column(String,unique=True, primary_key=True)
    employee_name = Column(String, nullable=False)
    employee_email = Column(String, unique=True, nullable=False)

    # Relationship to WebAuthn Credentials
    credentials =relationship("WebAuthnCredential",back_populates="employee")

class WebAuthnCredential(Base):
    __tablename__ = "webauthn_credentials"

    id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    employee_id = Column(String, ForeignKey("employee.employee_id"), nullable=False)
    credential_id = Column(String, unique=True, nullable=False)
    public_key = Column(LargeBinary, nullable=False)
    sign_count = Column(Integer, default=0)
    aaguid = Column(String, nullable=True) 

    employee = relationship("Employee", back_populates="credentials")

class ProtectedResourcesAccessCredentials(Base):
    __tablename__="protected_resources_access_credentials"
    id=Column(Integer,primary_key=True,autoincrement=True)
    latitude=Column(Float,nullable=False)
    longitude=Column(Float,nullable=False)
    ip_address=Column(String,nullable=False)

class Resources(Base):
    __tablename__="resources"
    resource_id=Column(Integer,primary_key=True,autoincrement=True)
    resource=Column(String,nullable=False)
    is_protected=Column(Boolean,nullable=False)

Base.metadata.create_all(Engine)