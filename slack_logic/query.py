
from slack_logic.util import *
from logic.util import *
from logic.hello import *
import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from sqlalchemy import create_engine, MetaData, Table
from langchain_community.llms import Ollama
from urllib.parse import quote_plus
from langchain.sql_database import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from langchain import LLMChain, PromptTemplate
from langchain.chains.conversation.memory import ConversationBufferWindowMemory

app = App(token=os.environ.get(BOT_TOKEN))

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
    db_chain = SQLDatabaseChain.from_llm(llm=llm, db=db, verbose=True, memory=ConversationBufferWindowMemory(k=2))
    print("Generated SQLDatabaseChain from Ollama and SQLDatabase with verbose output")
    return db_chain, llm

def itteration(metadata):
    table_names = metadata.tables.keys()
    for table_name in table_names:
        table = metadata.tables[table_name]
        columns = table.columns.keys()
        print("Table Name:", table_name)
        print("Column Names:", columns)
    return table_names, table_name, columns

def prompt_temp(table_names, history, human_input):
    prompt_template = f"""
                You are a very intelligent AI assistant who is expert in identifying relevant questions from user and converting them into SQL queries to generate answers.
                Please use the below context to write the MySQL queries, don't use Microsoft SQL Server queries.

                Context:
                You must query against the connected database, which has the following table(s): {', '.join(table_names)}.
                Example of questions:
                Example 1:
                    Question: What is the total count of employees?
                    SQL Query:
                    SELECT COUNT(EmployeeID) AS TotalEmployees FROM "table name";

                Example 2:
                    Question: Who are the employees working in the HR department?
                    SQL Query:
                    SELECT EmployeeName FROM "table name" WHERE EmployeeRole = 'HR';

                Based on the above examples, convert the following question into an SQL query and return the result in the following format:
                Example:1 - There are 521 total employees.
                Example:2 - The employees working in the HR department are: John, Suzy, Lola
                As an expert, you must use joins whenever required.

                {history}
                Human: {human_input}
                Assistant:
        """
    print('Prompt Template Generated')
    prompt = PromptTemplate(
        input_variables = ['history', 'human_input'],
        template=prompt_template
    )
    return prompt

def query_employees(human_input, say):
    greetings = hello_list()
    db_chain, llm = generate_db_chain()
    _, metadata = generate_engine_and_metadata()

    table_names = metadata.tables.keys()
    try:
        if 'analyze' in human_input.lower():
            say('Analyzing...')
            prompt_template = prompt_temp(table_names, history="", human_input=human_input)
            full_prompt = f'{[prompt_template]} \n\nQuestion: {human_input.lower()}'
            response = db_chain.invoke({"query": full_prompt})
            if response:
                if 'result' in response:
                    print("Found result in response:", response['result'])
                    return response['result']
                else:
                    print("Could not find an answer to the question")
                    return f'Unfortunately, I could not find an answer to your question: \n"{human_input.lower()}"'
            else:
                print("Failed to extract answer from the response.")
                return "Failed to extract answer from the response."

        elif any(greet.lower() in human_input.lower() for greet in greetings) or'help' in human_input.lower():
            print("Greetings detected.")
            return f'Greetings! You can usse Use "Analyze" in front of your sentence, followed by your question to activate natural language processing and talk with the Databse, or use LLM to talk with the Large Language Model.'

        elif 'llm' in human_input.lower():
            say('Thinking...')
            processed_input = human_input.lower().replace('llm', '').strip()
            response = llm(processed_input)
            return response

        else:
            print("No specific action for the question.")
            return f"""
                I apologize for any confusion. As a model trained in natural language processing, my capabilities are linked to the {'. '.join(table_names)} database. I'm here to assist with any queries or information you might need concerning it. Use "Analyze" in front of your sentence, followed by your question to activate natural language processing and talk with the Databse, or use LLM to talk with the Large Language Model.'
            """

    except Exception as e:
        print(f'Error during processing: {e}')

@app.message(".*")
def message_handler(message, say, logger):
    try:
        print(message)

        output = query_employees(human_input=message['text'], say=say)
        say(output)
    except Exception as e:
        print(f"Error handling message: {e}")
        say("Sorry, I encountered an error while processing your request.")

@app.event("app_mention")
def handle_app_mention_events(body, say, logger):
    try:
        logger.info(body)
        message_text = body['event']['text']
        output = query_employees(human_input=message_text, say=say)
        say(output)
    except Exception as e:
        logger.error(f"Error handling app mention: {e}")
        say("Sorry, I encountered an error while processing your request.")