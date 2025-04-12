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

# Faris
class Doctor(Base):
    __tablename__ = "Doctor"
    
    dID: Mapped[int] = mapped_column(Integer, primary_key=True)
    dPhoneNum: Mapped[str] = mapped_column(String(20))
    dName: Mapped[str] = mapped_column(String(100))
    dFirstName: Mapped[str] = mapped_column(String(55))
    dMiddleName: Mapped[str] = mapped_column(String(55))
    dLastName: Mapped[str] = mapped_column(String(55))
    
    prescriptions: Mapped[List["Prescription"]] = relationship(
        back_populates="doctor", cascade="all, delete-orphan"
    )

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
    
    def __repr__(self) -> str:
        return f"Pharmacist(pharmacistID={self.pharmacistID!r}, name={self.pFirstName!r} {self.pMiddleName!r} {self.pLastName!r}, title={self.pTitle!r})"


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
        return f"Prescription(presID={self.presID!r}, dateIssued={self.dateIssued!r}, pharmacistID={self.pharmacistID!r})"

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

# Faris
doctors_entries = [
    Doctor(dID=1, dPhoneNum='312-000-1111', dName='Dr. John Smith', dFirstName='John', dMiddleName='Mark', dLastName='Smith'),
    Doctor(dID=2, dPhoneNum='312-000-2222', dName='Dr. Sarah Lee', dFirstName='Sarah', dMiddleName='Alen', dLastName='Lee'),
    Doctor(dID=3, dPhoneNum='312-000-3333', dName='Dr. Amir Khan', dFirstName='Amir', dMiddleName='Zain', dLastName='Khan'),
    Doctor(dID=4, dPhoneNum='312-000-4444', dName='Dr. Emily Chen', dFirstName='Emily', dMiddleName='Rey', dLastName='Chen'),
    Doctor(dID=5, dPhoneNum='312-000-5555', dName='Dr. David Park', dFirstName='David', dMiddleName='Tom', dLastName='Park'),
]


#Insert Data
with Session(engine) as session:
    session.add_all(pharmacists_entries)
    session.add_all(prescriptions_entries)
    session.add_all(doctors_entries)
    session.commit()

# Simple Queries
session = Session(engine)  

k_query = (
    select(Prescription)
    .join(Prescription.pharmacist)
    .where(Prescription.pTitle == "Lead Pharmacist")
)
results = session.scalars(k_query).one()
for prescription in results:
    print(f"Priscription ID: {prescription.presID}, Issued by {prescription.pharmacist.pTitle}")


# Faris Join Query
doctor_prescription_query = (
    select(Prescription.presID, Prescription.dateIssued, Doctor.dFirstName, Doctor.dLastName)
    .join(Doctor, Prescription.dID == Doctor.dID)
    .limit(10)
)

results = session.execute(doctor_prescription_query).fetchall()

for presID, dateIssued, firstName, lastName in results:
    print(f"Prescription {presID} was issued on {dateIssued} by Dr. {firstName} {lastName}")
