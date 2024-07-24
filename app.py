from dotenv import load_dotenv
import streamlit as st
import os
import sqlite3
import pandas as pd
import google.generativeai as genai

load_dotenv()  # Load all the environment variables

# Configure our API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load Google Gemini model and provide SQL query as response
def get_gemini_response(question, prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([prompt[0], question])
    return response.text

# Function to retrieve query from SQL database
def read_sql_query(sql, db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    column_names = [description[0] for description in cur.description]
    conn.commit()
    conn.close()
    return rows, column_names

# Function to load and display the entire student database
def load_database(db):
    conn = sqlite3.connect(db)
    df = pd.read_sql_query("SELECT * FROM STUDENT", conn)
    conn.close()
    return df

# Define the prompt
prompt = [
    """
    You are an expert in converting English questions to SQL query!
    The SQL database has the name STUDENT and has the following columns - NAME, CLASS, 
    SECTION AND MARKS\n\nFor example,\nExample 1 - How many entries of records are present?, 
    the SQL command will be something like this SELECT COUNT(*) FROM STUDENT ;
    \nExample 2 - Tell me all the students studying in Data Science class?, 
    the SQL command will be something like this SELECT * FROM STUDENT 
    where CLASS="Data Science"; 
    also the sql code should not have ``` in beginning or end and sql word in output
    """
]

# Streamlit app
st.set_page_config(page_title="I can retrieve any SQL Query")
st.header("Query GPT")

# Display the entire database
if st.checkbox('Show entire database'):
    df = load_database("student.db")
    st.subheader("Student Database")
    st.dataframe(df)

question = st.text_input("Input: ", key="input")
submit = st.button("Ask the question")

# If submit is clicked
if submit:
    response = get_gemini_response(question, prompt)
    st.write(f"Generated SQL Query: {response}")
    data, columns = read_sql_query(response, "student.db")
    st.subheader("The Response is: ")
    if data:
        df = pd.DataFrame(data, columns=columns)
        st.dataframe(df)
    else:
        st.write("No data found for the given query.")
