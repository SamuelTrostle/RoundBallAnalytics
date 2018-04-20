# Imports
from flask import Flask, render_template, redirect, url_for, request, g
import csv, sqlite3
import pandas as pd

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def login():
    return render_template('national_congress.html')


state_page = {
    'fls':'florida_senate.html', 'vas':'virginia_senate.html', 'national':'national_congress.html'
}

@app.route('/<state_name>')
def index(state_name):
    return render_template(state_page[state_name])


# Access Input
@app.route('/admin', methods=['GET', 'POST'])
def admin():

    if request.method == 'POST':
        admin = request.form.getlist('admin')[0]

        if admin == 'root':
            return render_template('PollsForm1.html')
        else:
            return render_template('AdminPass.html')
    else:
        return render_template('AdminPass.html')

# Enter new data
@app.route('/data', methods=['GET', 'POST'])
def data():
    # Connect to Database
    con = sqlite3.connect('C:/Users/Samuel Trostle/Desktop/RoundBallSiteV1.0/db.roundball', check_same_thread=False)
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

        if 'ID' != '':
            ID = request.form.getlist('ID')[0]
            c.execute("DELETE FROM {} WHERE ID=?".format(table), (ID,))

        if 'ID' != '' and 'Date' 'Democrat' 'Republican' 'Source' 'Headline' == '':
            ID = request.form.getlist('ID')[0]
            c.execute("DELETE FROM {} WHERE ID=?".format(table), (ID,))

        c.execute("DELETE FROM {} WHERE Date = ''".format(table))

        con.commit()
        # Change table to dataframe
        dataframe = pd.read_sql("SELECT * FROM {}".format(table), con)

        # Change dataframe to CSV
        dataframe.to_csv('/Users/Samuel Trostle/Desktop/RoundBallSiteV1.0/static/states/{}/{}.csv'.format(State, table),
                         mode='w', sep=',', index=False, encoding='utf-8')
        print('refreshed')

        return render_template('/states/{}.html'.format(table))

    else:
        return render_template('PollsForm1.html')


@app.route('/VAdata', methods=['GET', 'POST'])
def VAdata():
    # Connect to Database
    con = sqlite3.connect('C:/Users/Samuel Trostle/Desktop/RoundBallSiteV1.0/db.roundball', check_same_thread=False)
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
        dataframe.to_csv('/Users/Samuel Trostle/Desktop/RoundBallSiteV1.0/static/states/{}/{}.csv'.format(State,table),
                         mode='w', sep=',', index=False, encoding='utf-8')
        print('refreshed')

        return render_template('national_congress.html')

    else:
        return render_template('/other/PollsFormVA.html')


if __name__ == "__main__":
    app.run(debug=True)
