from langchain_community.utilities import SQLDatabase
from langchain.agents.agent_types import AgentType
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain_community.chat_models import AzureChatOpenAI
from langchain_community.utilities import SQLDatabase
from langchain_community.llms import OpenAI
from langchain.agents import create_sql_agent
from langchain_community.agent_toolkits import SQLDatabaseToolkit
import pandas as pd
import sqlite3
import openai
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
import sqlite3
import json
from sqlalchemy import create_engine
from langchain_core.prompts import (
    ChatPromptTemplate,
    FewShotPromptTemplate,
    MessagesPlaceholder,
    PromptTemplate,
    SystemMessagePromptTemplate,
)


def load_json_to_dataframes(json_list):
    dataframes = []
    for json_obj in json_list:
        df = pd.DataFrame(json_obj, index=[9])
        dataframes.append(df)
    return dataframes


def json_file_to_tuples(file_path):
    """
        Reads JSON data from a file and converts it into a list of tuples,
        where each tuple contains the values from one of the JSON objects.

        Parameters:
        - file_path (str): The path to the JSON file.

        Returns:
        - list of tuples: Each tuple contains the values from one of the JSON objects.
        """
    # Open and load the JSON data from the file
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Extract values and convert them to tuples
    values_tuples = [tuple(item.values()) for item in data]
    return values_tuples


# Function to clean and format a single tuple into an SQL insert command
def format_tuple_as_insert(data_tuple, table_name):

    # Clean the tuple by removing '\r' and escaping single quotes
    cleaned_tuple = tuple(value.replace('\r', '').replace("'", "''") for value in data_tuple)
    # Format the tuple as an SQL insert command
    values_str = ', '.join(f"'{value}'" for value in cleaned_tuple)
    return f"INSERT INTO {table_name} (מספר_מבנה, אבן_דרך, איטרציה, סטטוס, תחנה, שלב_אכלוס, ימים_בסטטוס_נוכחי) VALUES ({values_str});\n"


# # Configure the baseline configuration of the OpenAI library for Azure OpenAI Service.
# openai.api_base = "https://azure-open-ao-new.openai.azure.com/"
# openai.api_key = "e3fcd2d5bcbf4bbb84810b386eb43ca0"
# openai.api_version = "2023-05-15"
# openai.api_type = "azure"
# #

# data = json_file_to_tuples("מספר_מבנה.json")
# # Specify the name of the table
# table_name = 'mivnim'
# #
# Path to your SQL file
# sql_file_path = 'initialize_mivnim_table.sql'
# # Path to your SQLite database
# db_path = 'kaham_database_new.db'
#
# # Connect to the SQLite database
# conn = sqlite3.connect(db_path)
# cursor = conn.cursor()
# #
# # Read and execute the SQL commands from the file
# with open(sql_file_path, 'r', encoding='utf-8') as sql_file:
#     sql_script = sql_file.read()
#     # If your SQL script contains multiple commands, you might need to split them
#     # This depends on whether your SQL commands are separated by `;` and newlines
#     for command in sql_script.split(';'):
#         # Skip any empty commands after splitting
#         if command.strip():
#             cursor.execute(command)
#
# # Commit the changes to the database and close the connection
# conn.commit()
# conn.close()
#
# print("SQL script executed successfully.")
#

# conn = sqlite3.connect(db_path)
# cursor = conn.cursor()
#
# # Execute the test query
# cursor.execute("SELECT * FROM mivnim LIMIT 10;")
#
# # Fetch and print the results
# rows = cursor.fetchall()
# for row in rows:
#     print(row)
#
# # Close the connection
# conn.close()




# # Open (or create) the SQL file
# with open('initialize_mivnim_table.sql', 'w', encoding='utf-8') as file:
#     # Write each data tuple to the file as an insert command
#     for data_tuple in data:
#         insert_command = format_tuple_as_insert(data_tuple, table_name)
#         file.write(insert_command)
#
# print("SQL insert commands have been written to insert_commands.sql")


# conn = sqlite3.connect('mydatabase.db')
# # Create a cursor object using the cursor() method
#
# cursor = conn.cursor()
# # Create table
#
# cursor.execute('''CREATE TABLE IF NOT EXISTS mivnim
#                (מספר מבנה TEXT, אבן דרך TEXT, איטרציה TEXT, סטטוס TEXT, תחנה TEXT, שלב אכלוס TEXT, ימים בסטטוס נוכחי TEXT)''')
# # Inserting data
#
# cursor.executemany('INSERT INTO mivnim VALUES (?,?,?,?,?,?,?)', data)
#
# # Replace 'your_table_name' with the name of your table
# query = 'SELECT COUNT(*) FROM mivnim'
#
# # Execute the query
# cursor.execute(query)
#
# # Fetch the result
# row_count = cursor.fetchone()[0]
#
# # Check if the table has rows
# if row_count > 0:
#     print(f"The table has {row_count} rows.")
# else:
#     print("The table is empty.")
#
# # conn.close()
#
# engine = create_engine("sqlite:///C:/Users/ltobaly/PycharmProjects/kaham_faster_table_qa/mydatabase.db")
# db = SQLDatabase(engine=engine)
# llm = AzureChatOpenAI(temperature=0, max_tokens=800, openai_api_base=openai.api_base,
#                         openai_api_key=openai.api_key,
#                         openai_api_version=openai.api_version, deployment_name="gpt-35-turbo-16k")
# agent_executor = create_sql_agent(
#     llm=llm,
#     toolkit=SQLDatabaseToolkit(db=db, llm=llm),
#     verbose=True,
#     agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
# )
#
# agent_executor.run(
#     "כמה מבנים יש?"
# )






app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

llm_vars = {}
@app.on_event('startup')
async def init():


    # Configure the baseline configuration of the OpenAI library for Azure OpenAI Service.
    openai.api_base = "https://kahamgpt.openai.azure.com/"
    openai.api_key = "fddbd98c77ae4d979cc758f99502bc79"
    openai.api_version = "2023-05-15"
    openai.api_type = "azure"

#

@app.post("/question")
def llm_question(req: dict):
    # Example usage
    #
    # # Configure the baseline configuration of the OpenAI library for Azure OpenAI Service.
    # openai.api_type = "azure"
    # openai.api_base = "https://bank-hapoalim.openai.azure.com/"
    # openai.api_version = "2023-03-15-preview"

    system_prefix = """You are an agent designed to interact with a SQL database and provide answers in Hebrew.
    Given an input question, create a syntactically correct {dialect} query to run, then look at the results of the query and return the answer.
    Unless the user specifies a specific number of examples they wish to obtain, always limit your query to at most {top_k} results.
    You can order the results by a relevant column to return the most interesting examples in the database.
    Never query for all the columns from a specific table, only ask for the relevant columns given the question.
    You have access to tools for interacting with the database.
    Only use the given tools. Only use the information returned by the tools to construct your final answer.
    You MUST double check your query before executing it. If you get an error while executing a query, rewrite the query and try again.
    In the database you'll find the following tables:
     mivnim (
    מספר_מבנה TEXT,
    אבן_דרך TEXT,
    איטרציה TEXT,
    סטטוס TEXT,
    תחנה TEXT,
    שלב_אכלוס TEXT,
    ימים_בסטטוס_נוכחי TEXT
    );
    mivnim_status (
    מספר_מבנה_ואבן_דרך TEXT,
    האם_ניתן_לסגור_אבן_דרך TEXT,
    מספר_ימים_באבן_דרך TEXT
    );

    
    DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the database.
    
    If the question does not seem related to the database, just return "I don't know" as the answer.
    
    """
    # prompt_template = PromptTemplate(input_variables=["question"], template= system_prefix)
    full_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prefix), ("human", "{input}"), MessagesPlaceholder("agent_scratchpad")
    ]
    )
    db = SQLDatabase.from_uri("sqlite:///kaham_database_new.db")
    inquiry = req['prompt']

    llm = AzureChatOpenAI(temperature=0, max_tokens=800, openai_api_base=openai.api_base,
                          openai_api_key=openai.api_key,
                          openai_api_version=openai.api_version, deployment_name="gpt-35-turbo-16k")
    agent_executor = create_sql_agent(
        llm=llm,
        prompt=full_prompt,
        toolkit=SQLDatabaseToolkit(db=db, llm=llm),
        verbose=True,
        agent_type="openai-tools",
    )

    res = agent_executor.run(inquiry)
    return {"response": res}

