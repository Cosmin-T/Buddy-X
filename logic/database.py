from logic.util import *
import pymysql
from urllib.parse import quote_plus
from mysql.connector import Error
import streamlit as st
import time
import random
from faker import Faker

def generate_database():
    connection = None
    cursor = None
    info1 = info2 = info3 = info4 = None

    try:
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password=PASS
        )
        if connection.open:
            info1 = st.info('Connection Established Successfully')
            cursor = connection.cursor()

            cursor.execute('SHOW DATABASES')
            databases = [db[0] for db in cursor.fetchall()]
            if DATABASE_NAME in databases:
                info2 = st.info(f'Database {DATABASE_NAME} already exists')

            else:
                cursor.execute(f'CREATE DATABASE {DATABASE_NAME}')
                info3 = st.info(f'Database {DATABASE_NAME} created successfully')

            cursor.execute(f'USE {DATABASE_NAME}')
            create_table_query = """
            CREATE TABLE IF NOT EXISTS Employees (
                EmployeeID INT AUTO_INCREMENT PRIMARY KEY,
                EmployeeName VARCHAR(255),
                EmployeeEmail VARCHAR(255),
                EmployeeRole VARCHAR(255),
                EmployeeStartDate DATE,
                EmployeeEndDate DATE,
                EmploymentType VARCHAR(50),
                ContractType VARCHAR(50),
                ContractDetails TEXT,
                PhoneNumber VARCHAR(15),
                EmergencyContactInformation TEXT,
                DateOfBirth DATE,
                SocialSecurityNumber VARCHAR(11),
                PhysicalAddress TEXT,
                SalaryInformation DECIMAL(10, 2),
                EducationAndQualifications TEXT,
                WorkSchedule TEXT,
                PerformanceReviews TEXT,
                TotalDaysOff INT,
                AvailableDaysOff INT,
                RemainingDaysOff INT,
                DepartmentEmailAddresses TEXT,
                SpecialInformation TEXT,
                InternalRules TEXT
            )"""
            cursor.execute(create_table_query)

        time.sleep(5)
        if info1 is not None:
            info1.empty()
        if info2 is not None:
            info2.empty()
        if info3 is not None:
            info3.empty()
        if info4 is not None:
            info4.empty()

    except Error as e:
        print(f'Error: {e}')
    finally:
        if cursor is not None and connection is not None:
            cursor.close()
            connection.close()
            print('MySQL connection is closed')

def add_random_employee(connection):
    cursor = connection.cursor()

    faker = Faker()
    for _ in range(500):
        EmployeeName = faker.name()
        EmployeeEmail = faker.email()
        EmployeeRole = faker.job()
        EmployeeStartDate = faker.date_between(start_date='-5y', end_date='today')
        EmployeeEndDate = faker.date_between(start_date=EmployeeStartDate, end_date='today')
        EmploymentType = random.choice(['Full-Time', 'Part-Time', 'Contract'])
        ContractType = random.choice(['Permanent', 'Temporary', 'Internship'])
        ContractDetails = faker.text(max_nb_chars=200)
        PhoneNumber = faker.phone_number()[:15]
        EmergencyContactInformation = faker.text(max_nb_chars=100)
        DateOfBirth = faker.date_of_birth(tzinfo=None, minimum_age=18, maximum_age=65).isoformat()
        SocialSecurityNumber = faker.ssn()
        PhysicalAddress = faker.address()
        SalaryInformation = round(random.uniform(30000, 100000), 2)
        EducationAndQualifications = faker.text(max_nb_chars=200)
        WorkSchedule = faker.text(max_nb_chars=100)
        PerformanceReviews = faker.text(max_nb_chars=200)
        TotalDaysOff = random.randint(0, 30)
        AvailableDaysOff = random.randint(0, TotalDaysOff)
        RemainingDaysOff = TotalDaysOff - AvailableDaysOff
        DepartmentEmailAddresses = faker.email()
        SpecialInformation = faker.text(max_nb_chars=200)
        InternalRules = faker.text(max_nb_chars=200)

        insert_query = """
        INSERT INTO Employees (
            EmployeeName, EmployeeEmail, EmployeeRole, EmployeeStartDate, EmployeeEndDate,
            EmploymentType, ContractType, ContractDetails, PhoneNumber, EmergencyContactInformation,
            DateOfBirth, SocialSecurityNumber, PhysicalAddress, SalaryInformation, EducationAndQualifications,
            WorkSchedule, PerformanceReviews, TotalDaysOff, AvailableDaysOff, RemainingDaysOff,
            DepartmentEmailAddresses, SpecialInformation, InternalRules
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        try:
            cursor.execute(insert_query, (
                EmployeeName, EmployeeEmail, EmployeeRole, EmployeeStartDate, EmployeeEndDate,
                EmploymentType, ContractType, ContractDetails, PhoneNumber, EmergencyContactInformation,
                DateOfBirth, SocialSecurityNumber, PhysicalAddress, SalaryInformation, EducationAndQualifications,
                WorkSchedule, PerformanceReviews, TotalDaysOff, AvailableDaysOff, RemainingDaysOff,
                DepartmentEmailAddresses, SpecialInformation, InternalRules
            ))
            connection.commit()
            print("Employee added successfully.")
        except Error as e:
            print(f'Error: {e}')
            connection.rollback()

def truncate_employees(connection):
    cursor = connection.cursor()
    truncate_query = "TRUNCATE TABLE Employees"

    try:
        cursor.execute(truncate_query)
        connection.commit()
        print("Employees table truncated successfully.")
    except Error as e:
        print(f'Error: {e}')
        connection.rollback()

def close_database_connection(connection):
    if connection:
        connection.close()

def connect_to_database():
    connection = None
    info1 = None
    try:
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password=PASS,
            port=3306,
            database=DATABASE_NAME,
        )
        info1 = st.info('Connection Established Successfully')

        time.sleep(5)
        if info1 is not None:
            info1.empty()

        return connection
    except pymysql.Error as e:
        print(f'Error: {e}')
        return None