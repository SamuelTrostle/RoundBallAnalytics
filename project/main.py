from flask import Flask, render_template, redirect, url_for, request, g
import csv, sqlite3
import pandas as pd
app = Flask(__name__)

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':

        # Check for Admin Priv
        if request.form['username'] == 'admin' and request.form['password'] == 'admin':
            return redirect(url_for('Admin'))

        #Check for Guest Priv
        elif request.form['username'] == 'guest' or request.form['password'] == 'guest':
            return redirect(url_for('Guest'))

        # Failed Login
        else:
            error = 'Invalid Credentials. Please try again.'
    return render_template('loginForm.html', error=error)

# Admin Login
@app.route("/Admin")
def Admin():
    return render_template('index.html')

# Guest Login
@app.route("/Guest")
def Guest():
    return render_template('guest_index.html')

# ----------------------------------------------------------

@app.route('/data', methods=['GET', 'POST'])
def data():
    # Connect to Database
    con = sqlite3.connect('C:/Users/Samuel Trostle/Desktop/RoundBallSiteV7/db.roundball', check_same_thread=False)
    c = con.cursor()
    if request.method == 'POST':
        Date = request.form.getlist('Date')[0]
        Democrat = request.form.getlist('Democrat')[0]
        Republican = request.form.getlist('Republican')[0]
        Source = request.form.getlist('Source')[0]
        Headline = request.form.getlist('Headline')[0]

        c.execute(
            'INSERT INTO conrace (Date, Democrat, Republican, Source, Headline) VALUES (?, ?, ?, ?, ?)',
            (Date, Democrat, Republican, Source, Headline))
        con.commit()
        # Change table to dataframe
        dataframe = pd.read_sql("SELECT * FROM conrace", con)

        # Change dataframe to CSV
        dataframe.to_csv('/Users/Samuel Trostle/Desktop/RoundBallSiteV7/static/conrace.csv', mode='w', sep=',',
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
    return render_template('guest_index.html')

if __name__ == "__main__":
    app.run(debug=True)
