from flask import Flask, render_template
import csv, sqlite3
import pandas as pd

app = Flask(__name__)


# Connect to Database
cnx = sqlite3.connect('db.roundball')
cur = cnx.cursor()

# Read CSV file, return dataframe
data = pd.read_csv('static/Data1.csv')
# print(data)

# Turn dataframe into SQLite table
data.to_sql('CongressionalRace', cnx, if_exists="replace", index=False)

# Update Table with Form
cur.execute("INSERT INTO CongressionalRace VALUES ('2/24/2018', 0.2, 0.8, 'TESTSAM', 'TESTTWO')")
cnx.commit()

# Change table to dataframe
dataframe = pd.read_sql("SELECT * FROM CongressionalRace", cnx)


# Change dataframe to CSV
dataframe.to_csv('/Users/Samuel Trostle/Desktop/RoundBallSiteV3/static/outputFile.csv', sep=',', index=False, encoding='utf-8')


# Run main application
@app.route("/")
def main():
    return render_template('index.html')

if __name__ == "__main__":
    app.run()
