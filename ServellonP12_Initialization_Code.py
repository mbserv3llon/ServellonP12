# Initialize code

import sqlite3

# Establish a connection
conn=sqlite3.connect("points.db")

# Instantiate a cursor
curs=conn.cursor()

# Use the cursor to make changes to the database
curs.execute('''
             CREATE TABLE PointsTable(
             id INTEGER(1,1) PRIMARY KEY,
             Latitude FLOAT,
             Longitude FLOAT,
             Description TEXT)''')

startingPoints = (
(34.0549,118.2426,'Los Angeles, home of the Dodgers'),
(40.7128,74.0060,"New York, home of the Yankees"),
(37.7749,122.4194,'San Francisco, home of the Giants'),
(43.6532,79.3832,'Toronto, home of the Blue Jays'),
(27.9517,82.4588,'Tampa Bay, home of the Rays')
)

for row in startingPoints:
  sqlCmd = '''
INSERT INTO PointsTable (Latitude, Longitude, Description) 
Values (%s,%s,'%s')
''' % row
  curs.execute(sqlCmd)

# Commit changes
conn.commit()

# Close connection
conn.close()
