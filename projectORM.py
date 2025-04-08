#NOTE: Drop the address & user_account tables before running this script
from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String, Integer
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy import Date
from datetime import datetime

#DB Connection: create_engine(DBMS_name+driver://<username>:<password>@<hostname>/<database_name>)
engine = create_engine("postgresql+psycopg2://postgres:1006@localhost/postgres")

#Define Classes/Tables
class Base(DeclarativeBase):
    pass

#Karolina
class Pharmacist(Base):
    __tablename__ = "Pharmacist"
    
    pharmacistID: Mapped[int] = mapped_column(Integer, primary_key=True)
    pFirstName: Mapped[str] = mapped_column(String(55))
    pMiddleName: Mapped[str] = mapped_column(String(55))
    pLastName: Mapped[str] = mapped_column(String(55))
    pTitle: Mapped[str] = mapped_column(String(30))
    prescriptions: Mapped[List["Prescription"]] = relationship(
        back_populates="pharmacist", cascade="all, delete-orphan"
    )
    
    def __repr__(self) -> str: #represents the object as a string 
        return f"Pharmacist(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"

#Karolina
class Prescription(Base):
    __tablename__ = "Prescription"
    
    presID: Mapped[int] = mapped_column(Integer, primary_key=True)
    dateIssued: Mapped[str] = mapped_column(Date)
    patientID: Mapped[int] = mapped_column(Integer, ForeignKey("Patient.patientID"))
    dID: Mapped[int] = mapped_column(Integer, ForeignKey("Doctor.dID"))
    pharmacistID: Mapped[int] = mapped_column(Integer, ForeignKey("Pharmacist.pharmacistID"))
    
    pharmacist: Mapped["Pharmacist"] = relationship(back_populates="prescriptions")
    
    def __repr__(self) -> str:
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"

#Create Tables
Base.metadata.create_all(engine)

#pharmacist entries Karolina
pharmacists_entries = [
    Pharmacist(pharmacistID=1, pFirstName='Robert', pMiddleName='Alan', pLastName='Wilson', pTitle='Pharmacist'),
    Pharmacist(pharmacistID=2, pFirstName='Jessica', pMiddleName='Marie', pLastName='Lopez', pTitle='Pharmacist'),
    Pharmacist(pharmacistID=3, pFirstName='Daniel', pMiddleName='Edward', pLastName='Kim', pTitle='Lead Pharmacist'),
]

#prescription entries Karolina
prescriptions_entries = [
    Prescription(presID=1001, dateIssued=datetime.strptime('2025-03-01', '%Y-%m-%d').date(), patientID=1, dID=1, pharmacistID=1),
    Prescription(presID=1002, dateIssued=datetime.strptime('2025-03-02', '%Y-%m-%d').date(), patientID=2, dID=2, pharmacistID=2),
    Prescription(presID=1003, dateIssued=datetime.strptime('2025-03-03', '%Y-%m-%d').date(), patientID=3, dID=3, pharmacistID=3),
    Prescription(presID=1004, dateIssued=datetime.strptime('2025-03-04', '%Y-%m-%d').date(), patientID=4, dID=4, pharmacistID=2),
    Prescription(presID=1005, dateIssued=datetime.strptime('2025-03-05', '%Y-%m-%d').date(), patientID=5, dID=5, pharmacistID=3),
    Prescription(presID=1006, dateIssued=datetime.strptime('2025-03-06', '%Y-%m-%d').date(), patientID=6, dID=2, pharmacistID=1),
    Prescription(presID=1007, dateIssued=datetime.strptime('2025-03-07', '%Y-%m-%d').date(), patientID=7, dID=3, pharmacistID=2),
    Prescription(presID=1008, dateIssued=datetime.strptime('2025-03-07', '%Y-%m-%d').date(), patientID=7, dID=3, pharmacistID=3),
    Prescription(presID=1009, dateIssued=datetime.strptime('2025-03-08', '%Y-%m-%d').date(), patientID=7, dID=3, pharmacistID=2),
    Prescription(presID=1010, dateIssued=datetime.strptime('2025-03-08', '%Y-%m-%d').date(), patientID=3, dID=3, pharmacistID=1),
    Prescription(presID=1011, dateIssued=datetime.strptime('2025-03-08', '%Y-%m-%d').date(), patientID=4, dID=4, pharmacistID=2),
    Prescription(presID=1012, dateIssued=datetime.strptime('2025-03-09', '%Y-%m-%d').date(), patientID=2, dID=2, pharmacistID=3),
    Prescription(presID=1013, dateIssued=datetime.strptime('2025-03-10', '%Y-%m-%d').date(), patientID=1, dID=1, pharmacistID=3),
    Prescription(presID=1014, dateIssued=datetime.strptime('2025-03-11', '%Y-%m-%d').date(), patientID=5, dID=5, pharmacistID=3),
]


#Insert Data
with Session(engine) as session:
    session.add_all(pharmacists_entries)
    session.add_all(prescriptions_entries)
    session.commit()

# Simple Queries
session = Session(engine)  

k_query = (
    select(Prescription)
    .join(Pharmacist, Prescription.pharmacistID == Pharmacist.pharmacistID)
    .where(Prescription.pharmacistID == 2)
)
results =  session.scalars(k_query).one()
print("Prescribed by Pharmacist 2: " + results.pharmacistID)





#Join Query
stmt = (
    select(Address)
    .join(Address.user)
    .where(User.name == "sandy")
    .where(Address.email_address == "sandy@sqlalchemy.org")
)
sandy_address = session.scalars(stmt).one()
print("Sandy's Address: " + sandy_address.email_address)

#Updates Sandy's email
sandy_address.email_address = "sandy_cheeks@sqlalchemy.org"

#Adds address for Patrick
stmt = select(User).where(User.name == "patrick")
patrick = session.scalars(stmt).one()
patrick.addresses.append(Address(email_address="patrickstar@sqlalchemy.org"))
session.commit()

#Show updated addresses
print("\n## Address Table Contents - After Update ##")
addresses = session.query(Address)  
for address in addresses:  
    print("Email Address: " + address.email_address)

#Deletes one of Sandy's email addresses (sandy_cheeks@...)
sandy = session.get(User, 2) #2 is the primary key (id)
sandy.addresses.remove(sandy_address)
session.commit()

#Shows updated addresses
print("\n## Address Table Contents - After Delete##")
addresses = session.query(Address)  
for address in addresses:  
    print("Email Address: " + address.email_address)