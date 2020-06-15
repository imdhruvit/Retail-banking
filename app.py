from flask import Flask, render_template, request
from flask_mysqldb import MySQL
import os
app = Flask(__name__,static_url_path='',static_folder='static',template_folder='templates')

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'toor'
app.config['MYSQL_DB'] = 'retail_bank'

mysql = MySQL(app)

@app.route('/')
def index():
    #initModel()
	#render out pre-built HTML file right on the index page
    return render_template("login.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        details = request.form
        uname = details['uname']
        password = details['pass']
        try:
            cur = mysql.connection.cursor()
            sql = "SELECT PASSWORD from userstore where Username='"+uname+"';"
            cur.execute(sql)
            record = cur.fetchone()
            if(record[0]==password):
                return 'Success'
            else:
                return 'Incorrect Username/Password'

        finally:
            cur.close()

if __name__ == '__main__':
        app.run(debug=True)
