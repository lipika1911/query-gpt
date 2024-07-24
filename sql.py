import sqlite3

# Connect to SQLite
connection = sqlite3.connect("events.db")

# Create a cursor object to insert, create, or retrieve results
cursor = connection.cursor()

# Create the Events table
table_info = """
CREATE TABLE IF NOT EXISTS Events (
    EventID INTEGER PRIMARY KEY AUTOINCREMENT,
    EventName TEXT NOT NULL,
    OrganizerName TEXT NOT NULL,
    Description TEXT,
    EventDate DATETIME NOT NULL,
    Location TEXT,
    Attendees INTEGER
);
"""

cursor.execute(table_info)

# Clear existing data (Optional, only if you want to reset the table)
cursor.execute('DELETE FROM Events')

# Insert sample records
sample_data = [
    ('Tech Conference 2024', 'Tech Innovations Pvt Ltd', 'Annual tech conference discussing emerging technologies.', '2024-08-15 09:00:00', 'India Habitat Centre, New Delhi', 500),
    ('Music Festival 2024', 'Music Events India', 'A summer festival featuring popular music bands.', '2024-07-20 15:00:00', 'JLN Stadium, New Delhi', 2000),
    ('Art Exhibition', 'National Gallery of Modern Art', 'Exhibition showcasing contemporary art by local artists.', '2024-09-10 11:00:00', 'National Gallery of Modern Art, Mumbai', 300),
    ('Startup Pitch Night', 'Innovate Ventures', 'Event where startups pitch their ideas to investors.', '2024-10-05 18:00:00', 'The Club, Mumbai', 150),
    ('Food Expo 2024', 'Gourmet Events Ltd.', 'Exhibition of gourmet food and culinary innovations.', '2024-11-12 10:00:00', 'Bangalore International Exhibition Centre, Bangalore', 800),
    ('Charity Gala Dinner', 'Help Foundation', 'Gala dinner to raise funds for charity.', '2024-12-01 19:00:00', 'Taj Palace Hotel, New Delhi', 200),
    ('Fitness Workshop', 'FitLife India', 'Workshop on fitness and healthy living.', '2024-08-25 09:00:00', 'Community Hall, Pune', 100),
    ('Science Fair', 'Science Club India', 'Annual science fair featuring student projects and experiments.', '2024-09-20 10:00:00', 'School Auditorium, Hyderabad', 500),
    ('Book Launch Event', 'Literary Publishers', 'Launch event for the latest book by renowned author.', '2024-10-15 17:00:00', 'Oxford Bookstore, Kolkata', 200),
    ('Theater Play - Hamlet', 'Kala Academy', 'Performance of Shakespeare\'s Hamlet.', '2024-11-05 20:00:00', 'Rangsharda Auditorium, Mumbai', 400)
]

cursor.executemany('''
    INSERT INTO Events (EventName, OrganizerName, Description, EventDate, Location, Attendees)
    VALUES (?, ?, ?, ?, ?, ?)
''', sample_data)

# Display all records
print("The inserted records are:")
data = cursor.execute('SELECT * FROM Events').fetchall()
for row in data:
    print(row)

# Commit changes and close the connection
connection.commit()
connection.close()
