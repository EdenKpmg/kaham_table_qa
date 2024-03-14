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
def format_tuple_as_insert_mivnim(data_tuple, table_name):
    # Clean the tuple by removing '\r' and escaping single quotes
    cleaned_tuple = tuple(value.replace('\r', '').replace("'", "''") for value in data_tuple)
    # Format the tuple as an SQL insert command
    values_str = ', '.join(f"'{value}'" for value in cleaned_tuple)
    return f"INSERT INTO {table_name} (מספר_מבנה, אבן_דרך, איטרציה, סטטוס, תחנה, שלב_אכלוס, ימים_בסטטוס_נוכחי) VALUES ({values_str});\n"

def format_tuple_as_insert_mivnim_status(data_tuple, table_name):
    # Assume the data_tuple structure matches the 'mivnim_status' table columns order
    # Clean the tuple by removing '\r' and escaping single quotes
    cleaned_tuple = tuple(value.replace('\r', '').replace("'", "''") for value in data_tuple)

    # Define column names for the 'mivnim_status' table
    columns = ["מספר_מבנה_ואבן_דרך", "האם_ניתן_לסגור_אבן_דרך", "מספר_ימים_באבן_דרך"]

    # Format the tuple as an SQL insert command
    columns_str = ', '.join(columns)  # Convert column names to a string
    values_str = ', '.join(f"'{value}'" for value in cleaned_tuple)
    return f"INSERT INTO {table_name} ({columns_str}) VALUES ({values_str});\n"


# data = json_file_to_tuples("מספר_מבנה_ואבן_דרך.json")
# # Specify the name of the table
# table_name = 'mivnim_status'

# # Open (or create) the SQL file
# with open('initialize_mivnim_status_table.sql', 'w', encoding='utf-8') as file:
#     # Write each data tuple to the file as an insert command
#     for data_tuple in data:
#         insert_command = format_tuple_as_insert_mivnim_status(data_tuple, table_name)
#         file.write(insert_command)


# print("SQL insert commands have been written to insert_commands.sql")


# #
# # Path to your SQL file
# sql_file_path = 'initialize_mivnim_table.sql'
# # Path to your SQLite database
# db_path = 'kaham_database.db'
#
# # Connect to the SQLite database
# conn = sqlite3.connect(db_path)
# cursor = conn.cursor()
#
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


# db = SQLDatabase.from_uri("sqlite:///kaham_database.db")
# print(db.dialect)
# print(db.get_usable_table_names())


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
