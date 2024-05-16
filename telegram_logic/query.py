
from telegram_logic.util import *
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
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

columns = []

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
    global columns
    table_names = metadata.tables.keys()
    for table_name in table_names:
        table = metadata.tables[table_name]
        columns = list(table.columns.keys())
        print("Table Name:", table_name)
        print("Column Names:", columns)
    return table_names, table_name, columns

def prompt_temp(table_names, history, human_input):
    global columns
    prompt_template = f"""
        You are an AI assistant specializing in SQL query generation for a database containing employee information. Please use the context below to formulate SQL queries.

        **Context:**
        You must query against the connected database, which has the following table(s): {', '.join(table_names)} and the following column(s): {', '.join(columns)}

        **EXAMPLE:**
        Question: What is the total count of employees?
        SQL Query: SELECT COUNT(EmployeeID) AS TotalEmployees FROM Employees;
        SQL Result: [(521,)]
        Answer: There are 521 total employees.

        **RETURN BACK ONLY THE ANSWER**

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

def query_employees(human_input):
    db_chain, _ = generate_db_chain()
    _, metadata = generate_engine_and_metadata()

    table_names = metadata.tables.keys()
    try:
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
            print("No specific action for the question.")
            return f"""
                I apologize for any confusion. As a model trained in natural language processing, my capabilities are linked to the {'. '.join(table_names)} database. I'm here to assist with any queries or information you might need concerning it.
            """

    except Exception as e:
        print(f'Error during processing: {e}')

async def  start_command(update:Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hi, how can I help you?')

def handle_repsonse(text):
    return query_employees(text)

async def handle_message(update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text
    print(f'User: {update.message.chat.id} in {message_type}: {text}')

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text = text.replace(BOT_USERNAME, '').strip()
            response = handle_repsonse(new_text)
        else:
            print('Bot was not mentioned in the group. No response sent.')
            return
    else:
        response = handle_repsonse(text)

    print(f'Bot: {response}')
    await update.message.reply_text(response)

async def error(update:Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')