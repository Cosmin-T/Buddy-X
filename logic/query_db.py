# query_db.py

from logic.database import *
from logic.util import *
from logic.hello import *
from sqlalchemy import create_engine, MetaData, Table
from langchain_community.llms import Ollama
from urllib.parse import quote_plus
from langchain.sql_database import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
import re

def initialize_database():
    conn_details = {
        'user': 'root',
        'password': PASS,
        'host': 'localhost',
        'port': 3306,
        'database': DATABASE_NAME
    }

    print('Prepare Database')
    return conn_details

def generate_engine_and_metadata():
    conn_details = initialize_database()
    connection_string = f"mysql+pymysql://{conn_details['user']}:{quote_plus(conn_details['password'])}@{conn_details['host']}:{conn_details['port']}/{conn_details['database']}"
    print(f"Initialize Connection")
    engine = create_engine(connection_string)
    print(f"Database Connected")
    metadata = MetaData()
    metadata.reflect(bind=engine)
    print("Metadata reflected")
    return engine, metadata

def generate_db_chain():
    engine, _ = generate_engine_and_metadata()
    llm = Ollama(model="codellama")
    print("Initialized Ollama with model 'codellama'")
    db = SQLDatabase(engine)
    print("Initialized SQLDatabase with engine")
    db_chain = SQLDatabaseChain.from_llm(llm=llm, db=db, verbose=True)
    print("Generated SQLDatabaseChain from Ollama and SQLDatabase with verbose output")
    return db_chain

def itteration(metadata):
    table_names = metadata.tables.keys()
    for table_name in table_names:
        table = metadata.tables[table_name]
        columns = table.columns.keys()
        print("Table Name:", table_name)
        print("Column Names:", columns)
    return table_names, table_name, columns

def prompt_temp(table_names):
    prompt_template = f"""
                You are a very intelligent AI assistant who is expert in identifying relevant questions from user and converting them into SQL queries to generate answers. Please use the below context to write the MySQL queries, don't use Microsoft SQL Server queries.
                Context:
                You must query against the connected database, which has the following table(s): {', '.join(table_names)}.
                Example of questions with responses:
                Example 1:
                    Question: What is the total count of employees?
                    SQL Query:
                    SELECT COUNT(EmployeeID) AS TotalEmployees FROM "table name";
                    Response:
                    There are 521 total employees.

                Example 2:
                    Question: Who are the employees working in the HR department?
                    SQL Query:
                    SELECT EmployeeName FROM "table name" WHERE EmployeeRole = 'HR';
                    Response:
                    The employees working in the HR department are: John, Suzy, Lola
                As an expert, you must use joins whenever required.
                """
    print('Prompt Template Generated')
    return prompt_template

def query_employees(question):
    greetings = hello_list()
    db_chain = generate_db_chain()
    _, metadata = generate_engine_and_metadata()

    try:
        if 'analyze' in question.lower():
            table_names = metadata.tables.keys()
            prompt_template = prompt_temp(table_names)
            full_prompt = f'{prompt_template} \n\nQuestion: {question}'
            response = db_chain.invoke({"query": full_prompt})
            if response:
                if 'result' in response:
                    print("Found result in response:", response['result'])
                    return response['result']
                else:
                    print("Could not find an answer to the question")
                    return f'Unfortunately, I could not find an answer to your question: \n"{question}"'
            else:
                print("Failed to extract answer from the response.")
                return "Failed to extract answer from the response."

        elif any(greet.lower() in question.lower() for greet in greetings):
            print("Greetings detected.")
            return f"Greetings! How can I assist you with the database today?"

        else:
            print("No specific action for the question.")
            return f"""
                I apologize, I am a model that understands natural language processing, I am currently connected to the database and can help you with any questions you might have in regards to it. The tables in the database include: {', '.join(table_names)}.
            """

    except Exception as e:
        print(f'Error during processing: {e}')