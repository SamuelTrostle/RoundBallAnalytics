from flask import Flask, render_template, redirect, url_for, request, g
import csv, sqlite3
import pandas as pd
import hashlib
import models as dbHandler
app = Flask(__name__)

# Connect to Database
con = sqlite3.connect('C:/Users/Samuel Trostle/Desktop/RoundBallSiteV7/db.roundball', check_same_thread=False)
c = con.cursor()

def check_password(hashed_password, user_password):
    return hashed_password == hashlib.md5(user_password.encode()).hexdigest()

def validate(username, password):
    con = sqlite3.connect('C:/Users/Samuel Trostle/Desktop/RoundBallSiteV7/db.roundball')
    completion = False
    with con:
                c = con.cursor()
                c.execute("SELECT * FROM Users")
                rows = c.fetchall()
                for row in rows:
                    dbUser = row[0]
                    dbPass = row[1]
                    if dbUser==username:
                        completion=check_password(dbPass, password)
    return completion


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        completion = validate(username, password)
        if completion ==False:
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('secret'))
    return render_template('login.html', error=error)

@app.route('/secret')
def secret():
    return "You have successfully logged in"

# ----------------------------------------------------------

@app.route('/data', methods=['GET', 'POST'])
def data():
    if request.method == 'POST':
        Date = request.form.getlist('Date')[0]
        Democrat = request.form.getlist('Democrat')[0]
        Republican = request.form.getlist('Republican')[0]
        Source = request.form.getlist('Source')[0]
        Headline = request.form.getlist('Headline')[0]

        c.execute(
            'INSERT INTO CongressionalRace (Date, Democrat, Republican, Source, Headline) VALUES (?, ?, ?, ?, ?)',
            (Date, Democrat, Republican, Source, Headline))
        con.commit()
        # Change table to dataframe
        dataframe = pd.read_sql("SELECT * FROM CongressionalRace", con)

        # Change dataframe to CSV
        dataframe.to_csv('/Users/Samuel Trostle/Desktop/RoundBallSiteV7/static/outputFile.csv', mode='w', sep=',',
                         index=False,
                         encoding='utf-8')
        return 'done'
    # return to index after seconds
    else:
        return render_template('PollsForm1.html')
# Remove entry



# Run main application
@app.route("/")
def main():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
