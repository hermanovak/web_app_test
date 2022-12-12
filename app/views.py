from app import app
from flask_mysqldb import MySQL

from flask import render_template, request, redirect

#import json as serializer

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'test'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
#app.config['MYSQL_CURSORCLASS'] = ''
 
mysql = MySQL()
mysql.init_app(app)

#Creating a connection cursor
#with app.app_context():
        #cursor = mysql.connection.cursor()
#cursor = mysql.connection.cursor()
    
#Executing SQL Statements

@app.route("/")
def index():
    with app.app_context():
        cursor = mysql.connection.cursor()
        #cursor.execute(''' CREATE TABLE example (id INTEGER, name VARCHAR(20)) ''')
        #cursor.execute(''' INSERT INTO emails VALUES (1, 'Kristyna') ''')
        #cursor.execute('''INSERT INTO example (id, name) VALUES (1, 'Jan')''')
        cursor.close()
        mysql.connection.commit()
        return 'Done'
        #return render_template("public/index.html")

@app.route("/about")
def about():
    return "<h1 style='color: red'>About!</h1>"

@app.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    with app.app_context():
        if request.method == "POST":
            req = request.form
        #print(req)
        
            username = req.get("username")
            print(username)
            print(type(username))
            email = username + '@ptc.cz'
       
            cur = mysql.connection.cursor()
            #cursor.execute(''' "INSERT INTO emails (username, email) VALUES ('%s', '%s')", (username, email ''')
            cur.execute("INSERT INTO emails(username, email) VALUES(%s, %s)",(username, email))
            #insert into table (col1, col2) values (%s, %s) % ("'{}'".format(val1)
            mysql.connection.commit()
            cur.close()
            #return 'success'


        #cursor.execute(''' INSERT INTO emails (username, email) VALUES (username, email) ''')
        #cursor.execute('''INSERT INTO `emails` (`username`, `email`) VALUES ('kristyna.hermanova', 'kristyna.hermanova@ptc.cz');''')
        #mysql.connection.commit()
        #cursor.close()
        
        
        #with open('emails.txt', 'a') as variable_file:
        #    variable_file.write("\n" + email)
        #
        #return redirect(request.url)

      
    
    return render_template("public/sign-up.html")


@app.route('/user/<name>')
def users(name):
    with app.app_context():
        cur = mysql.connection.cursor()
        cur.execute("SELECT * from emails")
        data = cur.fetchall()
        
        cur.close()

        return render_template('public/users.html', name=name, data=data)



poll_data = {
   'question1' : 'Are you a physicist?',
    'question2' : 'Are you a radiological assistant?',
} 

@app.route("/questionnaire1", methods=['GET', 'POST'])
def questionnaire1():
    # Check if user is loggedin
    if request.method == 'POST':
        # Create variables for easy access
        Q001 = request.form['Q001']
        Q002 = request.form['Q002']
        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE accounts SET Q001 = %s, Q002 = %s", (Q001, Q002))
        mysql.connection.commit()
        # Redirect to survey
    return render_template('public/survey.html', data=poll_data)
