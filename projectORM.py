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
engine = create_engine("postgresql+psycopg2://postgres:1@localhost/postgres")

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

#Lee    
class Medicine(Base):
    __tablename__ = "Medicine"

    mID: Mapped[int] = mapped_column(Integer, primary_key=True)
    price: Mapped[int] = mapped_column(Integer)
    medName: Mapped[str] = mapped_column(String)
    wholeID: Mapped[int] = mapped_column(Integer, ForeignKey("Wholesaler.wholeID"))

    medicine: Mapped["Medicine"] = relationship(
        back_populates="wholesaler", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"Medicine(mID={self.mID!r}, name={self.medName!r}, price={self.price!r}, wholeID={self.wholeID!r})"
#Lee    
class Wholesaler(Base):
    __tablename__ = "Wholesaler"

    wholeID: Mapped[int] = mapped_column(Integer, primary_key=True)
    wholesalerName: Mapped[str] = mapped_column(String)
    wPhoneNum : Mapped[int] = mapped_column(Integer)
    wAddress : Mapped[str] = mapped_column(String)
    zipCode : Mapped[int] = mapped_column(Integer)
    cityState : Mapped[str] = mapped_column(String)

    wholesaler: Mapped["Wholesaler"] = relationship(back_populates="medicine")

    def __repr__(self) -> str:
        return f"Wholesaler(wholeID={self.wholeID!r}, name={self.wholesalerName!r}, phoneNum={self.wPhoneNum!r}, address={self.wAddress!r}, {self.zipCode!r}, {self.cityState!r})"

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

#Lee
medicine_entries = [
    Medicine(mID=1, medName="Ibuprofen", price=25.99, wholeID=1),
    Medicine(mID=2, medName="Amoxicillin", price=12.50, wholeID=2),
    Medicine(mID=3, medName="Acetaminophen", price=30.00, wholeID=1),
    Medicine(mID=4, medName="Metformin", price=45.75, wholeID=2),
    Medicine(mID=5, medName="Insulin", price=99.99, wholeID=1),
]

#Lee
wholesaler_entries = [
    Wholesaler(wholeID=1, wholesalerName="MediSupplies, Inc.", wPhoneNum="111-222-3333", wAddress="10 Health Blvd, Suite 100, 60602, Chicago, IL", line1="10 Health Blvd", line2="Suite 100", zipcode="60602", cityState="Chicago, IL"),
    Wholesaler(wholeID=2, wholesalerName="Pharma Distributers LLC", wPhoneNum="444-555-6666", wAddress="20 Medicine Way, Building A, 10002, New York, NY", line1="20 Medicine Way", line2="Building A", zipcode="10002", cityState="New York, NY"),
    Wholesaler(wholeID=3, wholesalerName="Global Meds Supply", wPhoneNum="777-888-9999", wAddress="30 Pharma Street, Warehouse 5, 90002, Los Angeles, CA", line1="30 Pharma Street", line2="Warehouse 5", zipcode="90002", cityState="Los Angeles, CA"),
    Wholesaler(wholeID=4, wholesalerName="Medico Wholesale", wPhoneNum = "222-333-4444", wAddress="45 Medical Park, Building 5, 60605, Chicago, IL", line1="45 Medical Park", line2="Building 5", zipcode="60605", cityState="Chicago, IL")
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
    .join(Prescription.pharmacist)
    .where(Prescription.pTitle == "Lead Pharmacist")
)
results = session.scalars(k_query).one()
for prescription in results:
    print(f"Priscription ID: {prescription.presID}, Issued by {prescription.pharmacist.pTitle}")
