# Imports
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
@app.route("/admin")
def Admin():
    # refresh()
    return render_template('index.html')

# Guest Login
@app.route("/guest")
def Guest():
    refresh()
    return render_template('guest_index.html')

# Enter new data
@app.route('/data', methods=['GET', 'POST'])
def data():
    # Connect to Database
    con = sqlite3.connect('C:/Users/Samuel Trostle/Desktop/RoundBallSiteV9/db.roundball', check_same_thread=False)
    c = con.cursor()

    if request.method == 'POST':

        State = request.form.getlist('State')[0]
        Race = request.form.getlist('Race')[0]

        Date = request.form.getlist('Date')[0]
        Field1 = request.form.getlist('String1')[0]
        Field2 = request.form.getlist('String2')[0]
        Source = request.form.getlist('Source')[0]
        Headline = request.form.getlist('Headline')[0]

        ID = request.form.getlist('ID')[0]

        table = State + '_' + Race

        # Florida)
        if State == 'florida' and Race == 'senate':
            Nelson = Field1
            Scott = Field2
            print(Nelson)
            c.execute('INSERT INTO {} (Date, Nelson, Scott, Source, Headline) VALUES (?, ?, ?, ?, ?)'
                      .format(table), (Date, Nelson, Scott, Source, Headline))

        # Not Florida
        elif State != '' and State != 'florida':
            c.execute('INSERT INTO {} (Date, Democrat, Republican, Source, Headline) VALUES (?, ?, ?, ?, ?)'
                      .format(table), (Date, Field1, Field2, Source, Headline))

        elif 'ID' != '':
            ID = request.form.getlist('ID')[0]
            c.execute("DELETE FROM {} WHERE ID=?".format(table), (ID,))

        elif 'ID' != '' and 'Date' 'Democrat' 'Republican' 'Source' 'Headline' == '':
            ID = request.form.getlist('ID')[0]
            c.execute("DELETE FROM {} WHERE ID=?".format(table), (ID,))

        c.execute("DELETE FROM {} WHERE Date = ''".format(table))

        con.commit()
        # Change table to dataframe
        dataframe = pd.read_sql("SELECT * FROM {}".format(table), con)

        # Change dataframe to CSV
        dataframe.to_csv('/Users/Samuel Trostle/Desktop/RoundBallSiteV9/static/states/{}/{}.csv'.format(State,table),
                         mode='w', sep=',', index=False, encoding='utf-8')
        print('refreshed')

        return render_template('index.html')

    else:
        return render_template('PollsForm1.html')


@app.route('/VAdata', methods=['GET', 'POST'])
def VAdata():
    # Connect to Database
    con = sqlite3.connect('C:/Users/Samuel Trostle/Desktop/RoundBallSiteV9/db.roundball', check_same_thread=False)
    c = con.cursor()

    if request.method == 'POST':

        State = request.form.getlist('State')[0]
        Race = request.form.getlist('Race')[0]

        Date = request.form.getlist('Date')[0]

        Field1 = request.form.getlist('String1')[0]
        Field2 = request.form.getlist('String2')[0]
        Field3 = request.form.getlist('String1')[0]
        Field4 = request.form.getlist('String2')[0]
        Field5 = request.form.getlist('String1')[0]

        Source = request.form.getlist('Source')[0]
        Headline = request.form.getlist('Headline')[0]

        ID = request.form.getlist('ID')[0]

        table = State + '_' + Race

        # Virginia
        if State != '':
            c.execute('INSERT INTO {} (Date, Kaine, Comstock, Ingraham, Fiorina, Stewart, Source, Headline) '
                      'VALUES (?,?,?, ?, ?, ?, ?,?)' .format(table), (Date, Field1, Field2, Field3, Field4, Field5,
                                                                      Source, Headline))
        # Removal
        elif 'ID' != '':
            ID = request.form.getlist('ID')[0]
            c.execute("DELETE FROM {} WHERE ID=?".format(table), (ID,))

        elif 'ID' != '' and 'Date' 'Democrat' 'Republican' 'Source' 'Headline' == '':
            ID = request.form.getlist('ID')[0]
            c.execute("DELETE FROM {} WHERE ID=?".format(table), (ID,))

        c.execute("DELETE FROM {} WHERE Date = ''".format(table))

        con.commit()
        # Change table to dataframe
        dataframe = pd.read_sql("SELECT * FROM {}".format(table), con)

        # Change dataframe to CSV
        dataframe.to_csv('/Users/Samuel Trostle/Desktop/RoundBallSiteV9/static/states/{}/{}.csv'.format(State,table),
                         mode='w', sep=',', index=False, encoding='utf-8')
        print('refreshed')

        return render_template('index.html')

    else:
        return render_template('PollsFormVA.html')

# Florida
@app.route('/fl', methods=['GET', 'POST'])
def fl():
    # refresh()
    return render_template('/states/FLSenate.html')

# Virginia
@app.route('/va', methods=['GET', 'POST'])
def va():
    # refresh()
    return render_template('/states/VASenate.html')


# Run main application
@app.route("/")
def main():
    return render_template('guest_index.html')

if __name__ == "__main__":
    app.run(debug=True)
