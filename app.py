from dotenv import load_dotenv
import streamlit as st
import os
import sqlite3
import pandas as pd
import google.generativeai as genai

# Load all the environment variables
load_dotenv()

# Configure our API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load Google Gemini model and provide SQL query as response
def get_gemini_response(question, prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([prompt[0], question])
    return response.text.strip()  # Remove any extra whitespace

# Function to retrieve query from SQL database
def read_sql_query(sql, db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    try:
        cur.execute(sql)
        rows = cur.fetchall()
        column_names = [description[0] for description in cur.description]
    except sqlite3.OperationalError as e:
        # Handle errors such as incorrect SQL syntax or issues with the query
        st.error(f"SQL error: {e}")
        return [], []
    finally:
        conn.commit()
        conn.close()
    return rows, column_names

# Function to load and display the entire events database
def load_database(db):
    conn = sqlite3.connect(db)
    df = pd.read_sql_query("SELECT * FROM Events", conn)
    conn.close()
    return df

# Define the prompt
prompt = [
    """
    You are an expert in converting English questions to SQL query!
    The SQL database has the name Events and has the following columns - EventID, EventName, 
    OrganizerName, Description, EventDate, Location, Attendees\n\n
    For example,\n
    Example 1 - What is the date of the Tech Conference 2024?, 
    the SQL command will be something like this SELECT EventDate FROM Events WHERE EventName="Tech Conference 2024"; 
    \nExample 2 - List all events scheduled in New Delhi?, 
    the SQL command will be something like this SELECT * FROM Events WHERE Location LIKE "%New Delhi%"; 
    also the sql code should not have ``` in beginning or end and sql word in output
    """
]

# Streamlit app
st.set_page_config(page_title="Text to Query")
st.header("Query GPT")

# Display the entire database
if st.checkbox('Show entire database'):
    df = load_database("events.db")
    st.subheader("Events Database")
    st.dataframe(df)

question = st.text_input("Input: ", key="input")
submit = st.button("Ask the question")

# If submit is clicked
if submit:
    response = get_gemini_response(question, prompt)
    st.write(f"Generated SQL Query: {response}")
    data, columns = read_sql_query(response, "events.db")
    st.subheader("The Response is: ")
    if data:
        df = pd.DataFrame(data, columns=columns)
        st.dataframe(df)
    else:
        st.write("No data found for the given query.")
