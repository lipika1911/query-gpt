import sqlite3

#Connect to sqlite
connection=sqlite3.connect("student.db")

#create cursor object to to insert, create or retrieve result
cursor=connection.cursor()

#create the table
table_info="""
create table STUDENT(NAME VARCHAR(25),CLASS VARCHAR(25),SECTION VARCHAR(25),MARKS INT);
"""

cursor.execute(table_info)

#inserting some more records

cursor.execute('''Insert Into STUDENT values('Krish','Data Science','A',90)''')
cursor.execute('''Insert Into STUDENT values('Sudhanshu','Data Science','B',100)''')
cursor.execute('''Insert Into STUDENT values('Darius','Data Science','A',86)''')
cursor.execute('''Insert Into STUDENT values('Vikash','DEVOPS','A',50)''')
cursor.execute('''Insert Into STUDENT values('Dipesh','DEVOPS','A',35)''')

#display all records
print("The inserted records are")
data=cursor.execute('''Select * from STUDENT''')
for row in data:
    print(row)

#commit changes and close the connection
connection.commit()
connection.close()