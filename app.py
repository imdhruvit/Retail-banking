from flask import Flask, render_template, request,jsonify
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
            sql = "SELECT PASSWORD,Type from userstore where Username=%s"
            cur.execute(sql,(uname,))
            record = cur.fetchone()
            if(record[0]==password):
                if(record[1]=='Exec'):
                    return render_template('executive.html')
                elif(record[1]=='Cashier'):
                    return render_template('cashier.html')
            else:
                return 'Incorrect Username/Password'

        finally:
            cur.close()

@app.route('/create_customer', methods=['GET', 'POST'])
def create_customer():
    if request.method == "POST":
        id = request.form['id']
        Name = request.form['Name']
        Age = request.form['Age']
        Address = request.form['Address']
        State = request.form['State']
        City = request.form['City']
        try:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO customer(id,Name,Age,Address,State,City) VALUES (%s,%s,%s,%s,%s,%s)",(id,Name,Age,Address,State,City))
            mysql.connection.commit()
            return("done")
        except Exception as e:
            return(str(e))
        finally:
            cur.close()
    return render_template('create_customer.html')

@app.route('/customer_search', methods=['GET', 'POST'])
def customer_search():
    if request.method == "POST":
        id = request.form['id']
        print(id)
        try:
            cur = mysql.connection.cursor()
            sql = "SELECT id,Name,Age,Address,State,City from customer where id=%s"
            cur.execute(sql,(id,))
            record = cur.fetchone()
            print(record)
            return {"result":record}
        except Exception as e:
            return(str(e))
        finally:
            cur.close()
    if request.method == "GET":
        return render_template('customer_search.html')

@app.route('/update_customer', methods=['GET', 'POST'])
def update_customer():
    if request.method == "POST":
        print(request.form)
        id = request.form['id']
        Name = request.form['ncn']
        Age = request.form['nage']
        Address = request.form['na']
        try:
            cur = mysql.connection.cursor()
            val = (Name,Age,Address,id)
            cur.execute("UPDATE customer SET Name=%s,Age=%s,Address=%s WHERE id=%s",val)
            mysql.connection.commit()
            return("done")
        except Exception as e:
            return(str(e))
        finally:
            cur.close()
    elif request.method == "GET":
        return render_template('update_customer.html')

@app.route('/get_old_data', methods=['POST'])
def get_old_data():
    id = request.form['ssn']
    try:
        cur = mysql.connection.cursor()
        sql = "SELECT Name,Age,Address from customer where id=%s"
        cur.execute(sql,(id,))
        record = cur.fetchone()
        return jsonify(record)
    except Exception as e:
        return(str(e))
    finally:
        cur.close()
if __name__ == '__main__':
        app.run()
