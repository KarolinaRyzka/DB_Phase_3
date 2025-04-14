from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String, Integer, Float
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy import Date
from datetime import datetime
import psycopg2

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

# Charles
class Patient(Base):
    __tablename__ = "Patient"
    
    patientID: Mapped[int] = mapped_column(Integer, primary_key=True)
    birthdate: Mapped[str] = mapped_column(Date)
    patPhoneNum: Mapped[str] = mapped_column(String(20))
    patFirstName: Mapped[str] = mapped_column(String(55))
    patMiddleName: Mapped[str] = mapped_column(String(55))
    patLastName: Mapped[str] = mapped_column(String(55))
    patLine1: Mapped[str] = mapped_column(String(100))
    patLine2: Mapped[str] = mapped_column(String(100))
    patZipCode: Mapped[str] = mapped_column(String(10))
    patCityState: Mapped[str] = mapped_column(String(20))
    
    prescriptions: Mapped[List["Prescription"]] = relationship(
        back_populates="patient", cascade="all, delete-orphan"    
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
    doctor: Mapped["Doctor"] = relationship(back_populates="prescriptions")
    patient: Mapped["Patient"] = relationship(back_populates="presxriptions")
    
    def __repr__(self) -> str:
        return f"Prescription(presID={self.presID!r}, dateIssued={self.dateIssued!r}, pharmacistID={self.pharmacistID!r})"

#Lee    
class Medicine(Base):
    __tablename__ = "Medicine"

    mID: Mapped[int] = mapped_column(Integer, primary_key=True)
    price: Mapped[float] = mapped_column(Float)
    medName: Mapped[str] = mapped_column(String)
    wholeID: Mapped[int] = mapped_column(Integer, ForeignKey("Wholesaler.wholeID"))
    
    wholesaler: Mapped["Wholesaler"] = relationship(back_populates="medicines")

    def __repr__(self) -> str:
        return f"Medicine(mID={self.mID!r}, name={self.medName!r}, price={self.price!r}, wholeID={self.wholeID!r})"
#Lee    
class Wholesaler(Base):
    __tablename__ = "Wholesaler"

    wholeID: Mapped[int] = mapped_column(Integer, primary_key=True)
    wholesalerName: Mapped[str] = mapped_column(String(100))
    wPhoneNum : Mapped[str] = mapped_column(String(15))
    wAddress : Mapped[str] = mapped_column(String(255))
    line1: Mapped[str] = mapped_column(String(255))
    line2: Mapped[str] = mapped_column(String(255))
    zipCode : Mapped[int] = mapped_column(Integer)
    cityState : Mapped[str] = mapped_column(String(100))

    medicines: Mapped[List["Medicine"]] = relationship(back_populates="wholesaler")

    def __repr__(self) -> str:
        return f"Wholesaler(wholeID={self.wholeID!r}, name={self.wholesalerName!r}, phoneNum={self.wPhoneNum!r}, address={self.wAddress!r})"

#Create Tables
Base.metadata.create_all(engine)

# #pharmacist entries Karolina
pharmacists_entries = [
    Pharmacist(pharmacistID=1, pFirstName='Robert', pMiddleName='Alan', pLastName='Wilson', pTitle='Pharmacist'),
    Pharmacist(pharmacistID=2, pFirstName='Jessica', pMiddleName='Marie', pLastName='Lopez', pTitle='Pharmacist'),
    Pharmacist(pharmacistID=3, pFirstName='Daniel', pMiddleName='Edward', pLastName='Kim', pTitle='Lead Pharmacist'),
]

# #prescription entries Karolina
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
    Wholesaler(wholeID=1, wholesalerName="MediSupplies, Inc.", wPhoneNum="111-222-3333", wAddress="10 Health Blvd, Suite 100, 60602, Chicago, IL", line1="10 Health Blvd", line2="Suite 100", zipCode="60602", cityState="Chicago, IL"),
    Wholesaler(wholeID=2, wholesalerName="Pharma Distributers LLC", wPhoneNum="444-555-6666", wAddress="20 Medicine Way, Building A, 10002, New York, NY", line1="20 Medicine Way", line2="Building A", zipCode="10002", cityState="New York, NY"),
    Wholesaler(wholeID=3, wholesalerName="Global Meds Supply", wPhoneNum="777-888-9999", wAddress="30 Pharma Street, Warehouse 5, 90002, Los Angeles, CA", line1="30 Pharma Street", line2="Warehouse 5", zipCode="90002", cityState="Los Angeles, CA"),
    Wholesaler(wholeID=4, wholesalerName="Medico Wholesale", wPhoneNum = "222-333-4444", wAddress="45 Medical Park, Building 5, 60605, Chicago, IL", line1="45 Medical Park", line2="Building 5", zipCode="60605", cityState="Chicago, IL")
]

#Charles Patient Entries
patient_entries = [
    Patient(patientID=1, patFirstName='John', patMiddleName='Michael', patLastName='Smith', birthdate=datetime.strptime('1985-04-12', '%Y-%m-%d').date(), patPhoneNum='555-123-4567', patLine1='123 Elm St', patLine2='Apt 4B', patZipCode='62701', patCityState='Springfield, IL'),
    Patient(patientID=2, patFirstName='Sarah', patMiddleName=None, patLastName='Johnson', birthdate=datetime.strptime('1990-08-23', '%Y-%m-%d').date(), patPhoneNum='555-234-5678', patLine1='456 Oak St', patLine2=None, patZipCode='63101', patCityState='St. Louis, MO'),
    Patient(patientID=3, patFirstName='James', patMiddleName='Daniel', patLastName='Brown', birthdate=datetime.strptime('1977-01-15', '%Y-%m-%d').date(), patPhoneNum='555-345-6789', patLine1='789 Pine St', patLine2=None, patZipCode='60601', patCityState='Chicago, IL'),
    Patient(patientID=4, patFirstName='Emily', patMiddleName=None, patLastName='Davis', birthdate=datetime.strptime('1995-11-30', '%Y-%m-%d').date(), patPhoneNum='555-456-7890', patLine1='321 Maple St', patLine2='Apt 2A', patZipCode='61602', patCityState='Peoria, IL'),
    Patient(patientID=5, patFirstName='William', patMiddleName='Andrew', patLastName='Miller', birthdate=datetime.strptime('1988-02-10', '%Y-%m-%d').date(), patPhoneNum='555-567-8901', patLine1='987 Cedar St', patLine2='Apt 3C', patZipCode='62701', patCityState='Springfield, IL'),
    Patient(patientID=6, patFirstName='Olivia', patMiddleName=None, patLastName='Martinez', birthdate=datetime.strptime('1988-02-10', '%Y-%m-%d').date(), patPhoneNum='555-678-9012', patLine1='654 Birch St', patLine2='Apt 5D', patZipCode='64101', patCityState='Kansas City, MO'),
    Patient(patientID=7, patFirstName='Benjamin', patMiddleName='Alexander', patLastName='Wilson', birthdate=datetime.strptime('1993-06-14', '%Y-%m-%d').date(), patPhoneNum='555-789-0123', patLine1='432 Willow St', patLine2=None, patZipCode='60601', patCityState='Chicago, IL'),
    Patient(patientID=8, patFirstName='Sophia', patMiddleName='Grace', patLastName='Moore', birthdate=datetime.strptime('1981-12-22', '%Y-%m-%d').date(), patPhoneNum='555-890-1234', patLine1='876 Spruce St', patLine2='Apt 7A', patZipCode='63101', patCityState='St. Louis, MO'),
    Patient(patientID=9, patFirstName='Ethan', patMiddleName=None, patLastName='Taylor', birthdate=datetime.strptime('1999-07-04', '%Y-%m-%d').date(), patPhoneNum='555-901-2345', patLine1='543 Ash St', patLine2=None, patZipCode='62701', patCityState='Springfield, IL'),
    Patient(patientID=10, patFirstName='Mia', patMiddleName='Elizabeth', patLastName='Anderson', birthdate=datetime.strptime('2002-09-18', '%Y-%m-%d').date(), patPhoneNum='555-012-3456', patLine1='109 Hickory St', patLine2='Apt 1B', patZipCode='60601', patCityState='Chicago, IL'),
    Patient(patientID=11, patFirstName='Noah', patMiddleName=None, patLastName='Thomas', birthdate=datetime.strptime('1996-05-29', '%Y-%m-%d').date(), patPhoneNum='555-123-5678', patLine1='222 Poplar St', patLine2=None, patZipCode='61602', patCityState='Peoria, IL'),
    Patient(patientID=12, patFirstName='Ava', patMiddleName='Lily', patLastName='White', birthdate=datetime.strptime('1992-11-02', '%Y-%m-%d').date(), patPhoneNum='555-234-6789', patLine1='678 Oakwood St', patLine2=None, patZipCode='64101', patCityState='Kansas City, MO'),
    Patient(patientID=13, patFirstName='Mason', patMiddleName='Henry', patLastName='Harris', birthdate=datetime.strptime('1983-04-11', '%Y-%m-%d').date(), patPhoneNum='555-345-7890', patLine1='345 Elmwood St', patLine2=None, patZipCode='60601', patCityState='Chicago, IL'),
    Patient(patientID=14, patFirstName='Isabella', patMiddleName=None, patLastName='Clark', birthdate=datetime.strptime('1997-08-20', '%Y-%m-%d').date(), patPhoneNum='555-456-8901', patLine1='210 Cedarwood St', patLine2=None, patZipCode='62701', patCityState='Springfield, IL'),
    Patient(patientID=15, patFirstName='Logan', patMiddleName='David', patLastName='Lewis', birthdate=datetime.strptime('1991-03-03', '%Y-%m-%d').date(), patPhoneNum='555-567-9012', patLine1='333 Redwood St', patLine2='Apt 6C', patZipCode='61602', patCityState='Peoria, IL'),
    Patient(patientID=16, patFirstName='Ella', patMiddleName=None, patLastName='Robinson', birthdate=datetime.strptime('1986-06-12', '%Y-%m-%d').date(), patPhoneNum='555-678-0123', patLine1='888 Walnut St', patLine2=None, patZipCode='63101', patCityState='St. Louis, MO'),
    Patient(patientID=17, patFirstName='Lucas', patMiddleName='Samuel', patLastName='Hall', birthdate=datetime.strptime('1980-10-01', '%Y-%m-%d').date(), patPhoneNum='555-789-1234', patLine1='555 Maplewood St', patLine2=None, patZipCode='62701', patCityState='Springfield, IL'),
    Patient(patientID=18, patFirstName='Amelia', patMiddleName='Victoria', patLastName='Allen', birthdate=datetime.strptime('1998-01-17', '%Y-%m-%d').date(), patPhoneNum='555-890-2345', patLine1='777 Elmwood St', patLine2='Apt 8B', patZipCode='64101', patCityState='Kansas City, MO'),
    Patient(patientID=19, patFirstName='Elijah', patMiddleName=None, patLastName='King', birthdate=datetime.strptime('1989-09-26', '%Y-%m-%d').date(), patPhoneNum='555-901-3456', patLine1='111 Ashwood St', patLine2=None, patZipCode='60601', patCityState='Chicago, IL'),
    Patient(patientID=20, patFirstName='Charlotte', patMiddleName='Abigail', patLastName='Wright', birthdate=datetime.strptime('2001-12-05', '%Y-%m-%d').date(), patPhoneNum='555-012-4567', patLine1='999 Birchwood St', patLine2='Apt 4D', patZipCode='63101', patCityState='St. Louis, MO'),
    Patient(patientID=21, patFirstName='Alexander', patMiddleName=None, patLastName='Scott', birthdate=datetime.strptime('1984-07-15', '%Y-%m-%d').date(), patPhoneNum='555-123-6789', patLine1='444 Willowwood St', patLine2=None, patZipCode='61602', patCityState='Peoria, IL'),
    Patient(patientID=22, patFirstName='Harper', patMiddleName=None, patLastName='Young', birthdate=datetime.strptime('1994-05-03', '%Y-%m-%d').date(), patPhoneNum='555-234-7890', patLine1='321 Oakview St', patLine2='Apt 3A', patZipCode='60601', patCityState='Chicago, IL'),
    Patient(patientID=23, patFirstName='Daniel', patMiddleName='Matthew', patLastName='Baker', birthdate=datetime.strptime('1979-02-28', '%Y-%m-%d').date(), patPhoneNum='555-345-8901', patLine1='678 Elmview St', patLine2=None, patZipCode='62701', patCityState='Springfield, IL'),
    Patient(patientID=24, patFirstName='Zoey', patMiddleName='Hannah', patLastName='Green', birthdate=datetime.strptime('2003-06-07', '%Y-%m-%d').date(), patPhoneNum='555-456-9012', patLine1='222 Pineview St', patLine2='Apt 2D', patZipCode='64101', patCityState='Kansas City, MO'),
    Patient(patientID=25, patFirstName='Jackson', patMiddleName='Lucas', patLastName='Adams', birthdate=datetime.strptime('1987-11-09', '%Y-%m-%d').date(), patPhoneNum='555-567-0123', patLine1='555 Birchview St', patLine2=None, patZipCode='63101', patCityState='St. Louis, MO'),
]

doctors_entries = [
    Doctor(dID=1, dPhoneNum='312-000-1111', dName='Dr. John Smith', dFirstName='John', dMiddleName='Mark', dLastName='Smith'),
    Doctor(dID=2, dPhoneNum='312-000-2222', dName='Dr. Sarah Lee', dFirstName='Sarah', dMiddleName='Alen', dLastName='Lee'),
    Doctor(dID=3, dPhoneNum='312-000-3333', dName='Dr. Amir Khan', dFirstName='Amir', dMiddleName='Zain', dLastName='Khan'),
    Doctor(dID=4, dPhoneNum='312-000-4444', dName='Dr. Emily Chen', dFirstName='Emily', dMiddleName='Rey', dLastName='Chen'),
    Doctor(dID=5, dPhoneNum='312-000-5555', dName='Dr. David Park', dFirstName='David', dMiddleName='Tom', dLastName='Park'),
]



#Insert Data
with Session(engine) as session:
    session.add_all(doctors_entries)
    session.add_all(pharmacists_entries)  
    session.add_all(patient_entries)
    session.add_all(wholesaler_entries)
    session.add_all(medicine_entries)    
    session.add_all(prescriptions_entries)

    session.commit()



session = Session(engine)  
# Karolina Query 
prescribedByLeadPharmacist = (
    select(Prescription.presID, Pharmacist.pFirstName, Pharmacist.pLastName )
    .join(Pharmacist, Prescription.pharmacistID == Pharmacist.pharmacistID)
    .where(Pharmacist.pTitle == "Lead Pharmacist")
)
results = session.execute(prescribedByLeadPharmacist).all()
for presID, firstName, lastName in results:
    print(f"Priscription ID: {presID}, Issued by the Lead Pharmacist, {firstName} {lastName}")

# Faris Join Query
doctor_prescription_query = (
    select(Prescription.presID, Prescription.dateIssued, Doctor.dFirstName, Doctor.dLastName)
    .join(Doctor, Prescription.dID == Doctor.dID)
)
results = session.execute(doctor_prescription_query).fetchall()
for presID, dateIssued, firstName, lastName in results:
    print(f"Prescription {presID} was issued on {dateIssued} by Dr. {firstName} {lastName}")

#Lee Query
med_whole_query = (
    select(Medicine)
    .join(Medicine.wholesaler)
)
results = session.scalars(med_whole_query).all()
for r in results:
    print(f"Medicine {r.medName} supplied by wholesaler ID {r.wholeID}, name {r.wholesaler.wholesalerName}")

# Charles Join Query
patient_stmt = (
    select(Prescription.pID, Patient.patZipCode)
    .join(Patient, Prescription.patientID == Patient.patientID) 
    .where(Patient.patCityState == "Chicago, IL")
    .limit(5)
)
results = session.execute(patient_stmt).all()
for pID, patZipCode in results:
    print(f"Patient {pID} will be delivered to Zip Code: {patZipCode}")



