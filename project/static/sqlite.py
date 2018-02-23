import csv
import sqlite3

# Create Database
connection = sqlite3.connect('RoundBall.db')
cursor = connection.cursor()

cursor.execute('DROP TABLE IF EXISTS congressionalTable')
cursor.execute("CREATE TABLE congressionalTable ( Date, Democrat, Republican, Source, Headline)")
connection.commit()

#  Load CSV file into CSV reader
csvfile = open('Congressional1.csv', encoding="utf8")
creader = csv.reader(csvfile, delimiter=',', quotechar='|')

# Iterate through the CSV reader and insert values into the Database
for t in creader:
    cursor.execute('INSERT INTO congressionalTable VALUES (?,?,?,?,?)', t)

# Queries
cursor.execute("SELECT Date, Democrat, Republican, Headline from congressionalTable")
for row in cursor:
   print("Date = ", row[0])
   print("Democrat = ", row[1])
   print("Republican = ", row[2])
   print("Headline = ", row[3], "\n")

# Close the csv file, commit changes and close the connection
csvfile.close()
connection.commit()
connection.close()
