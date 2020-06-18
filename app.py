from flask import Flask, render_template, request, jsonify, flash, session,redirect,url_for
from flask_mysqldb import MySQL
import os
import json
import math

app = Flask(__name__, static_url_path='',
            static_folder='static', template_folder='templates')
app.secret_key = 'sdsd15sd6fsf'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'toor'
app.config['MYSQL_DB'] = 'retail_bank'

mysql = MySQL(app)

class CustomJsonEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(CustomJsonEncoder, self).default(obj)

# Route to Home page
@app.route('/')
def index():
    return render_template("login.html")

# Route to Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        details = request.form
        uname = details['uname']
        password = details['pass']
        session['username'] = uname

        try:
            cur = mysql.connection.cursor()
            sql = "SELECT PASSWORD,Type from userstore where Username=%s"
            cur.execute(sql, (uname,))
            record = cur.fetchone()
            session['role'] = record[1]
            if(record[0] == password):
                if(record[1] == 'Exec'):
                    return render_template('executive.html')
                elif(record[1] == 'Cashier'):
                    return render_template('cashier.html')
            else:
                return 'Incorrect Username/Password'

        finally:
            cur.close()

    elif request.method == "GET":
        if 'username' in session:
            if session['role'] == 'Exec':
                return render_template('executive.html')
            elif session["role"] == 'Cashier':
                return render_template('cashier.html')
        else:
            return render_template('login.html')

# Route to Logout page
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('username', None)
    session.pop('role', None)
    return render_template('login.html')

# Route to create customer page
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
            cur.execute("SELECT max(Cust_id) from customer")
            maxid = cur.fetchone()
            Cust_id = int(maxid[0]) + 1
            cid = '0' * \
                (9 - (math.floor(math.log(Cust_id, 10) + 1))) + str(Cust_id)
            cur.execute("INSERT INTO customer(id,Name,Age,Address,State,City,Cust_id,Message,Timestamp) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,CURRENT_TIMESTAMP())",
                        (id, Name, Age, Address, State, City,cid,'Customer created'))
            mysql.connection.commit()
            flash('Successfully created customer')
            return redirect(url_for('create_customer'))
        except Exception as e:
            return(str(e))
        finally:
            cur.close()
    elif request.method == "GET":
        if 'username' in session:
            if session['role'] == 'Exec':
                return render_template('create_customer.html')
            else:
                return render_template('cashier.html')
        else:
            return render_template('login.html')

# Route to delete customer page
@app.route('/delete_customer', methods=['GET', 'POST'])
def delete_customer():
    if request.method == "POST":
        id = request.form['id']
        try:
            cur = mysql.connection.cursor()
            sql = "DELETE from customer where id =%s;"
            cur.execute(sql, (id,))
            mysql.connection.commit()
            return("done")
        except Exception as e:
            return(str(e))

        finally:
            cur.close()
    elif request.method == "GET":
        if 'username' in session:
            if session['role'] == 'Exec':
                return render_template('delete_customer.html')
            else:
                return render_template('cashier.html')
        else:
            return render_template('login.html')

# Route to Search customer page
@app.route('/search_customer', methods=['GET', 'POST'])
def search_customer():
    if request.method == "GET":
        if 'username' in session:
            if session['role'] == 'Exec':
                return render_template('search_customer.html')
            else:
                return render_template('cashier.html')
        else:
            return render_template('login.html')

# Route to Search account page
@app.route('/search_account', methods=['GET', 'POST'])
def search_account():
    if request.method == "GET":
        if 'username' in session:
            return render_template('search_account.html')
        else:
            return render_template('login.html')

# Route to Update customer page
@app.route('/update_customer', methods=['GET', 'POST'])
def update_customer():
    if request.method == "POST":
        id = request.form['id']
        Name = request.form['ncn']
        Age = request.form['nage']
        Address = request.form['na']
        try:
            cur = mysql.connection.cursor()
            val = (Name, Age, Address, id)
            cur.execute(
                "UPDATE customer SET Name=%s,Age=%s,Address=%s WHERE id=%s", val)
            mysql.connection.commit()
            return("done")
        except Exception as e:
            return(str(e))
        finally:
            cur.close()
    elif request.method == "GET":
        if 'username' in session:
            if session['role'] == 'Exec':
                return render_template('update_customer.html')
            else:
                return render_template('cashier.html')
        else:
            return render_template('login.html')

# Search customer
@app.route('/search_c', methods=['POST'])
def search_c():
    id = request.form['ssn']
    sel = request.form['sel']
    if str(sel) == '1':
        try:
            cur = mysql.connection.cursor()
            sql = "SELECT id,Cust_id,Name,Age,Address,State,City,Timestamp from customer where id=%s"
            cur.execute(sql, (id,))
            record = cur.fetchone()
            return jsonify(record)
        except Exception as e:
            return(str(e))
        finally:
            cur.close()
    elif str(sel) == '2':
        try:
            cur = mysql.connection.cursor()
            sql = "SELECT id,Cust_id,Name,Age,Address,State,City,Timestamp from customer where Cust_id=%s"
            cur.execute(sql, (id,))
            record = cur.fetchone()
            return jsonify(record)
        except Exception as e:
            return(str(e))
        finally:
            cur.close()

# Search account
@app.route('/search_a', methods=['POST'])
def search_a():
    id = request.form['ssn']
    sel = request.form['sel']
    if str(sel) == '1':
        try:
            cur = mysql.connection.cursor()
            sql = "SELECT Cust_id, Account_id, Type, Amount, Message, Timestamp from account where Account_id=%s"
            cur.execute(sql, (id,))
            record = cur.fetchone()
            return jsonify(record)
        except Exception as e:
            return(str(e))
        finally:
            cur.close()
    elif str(sel) == '2':
        try:
            cur = mysql.connection.cursor()
            sql = "SELECT Cust_id, Account_id, Type, Amount, Message, Timestamp from account where Cust_id=%s"
            cur.execute(sql, (id,))
            record = cur.fetchone()
            return jsonify(record)
        except Exception as e:
            return(str(e))
        finally:
            cur.close()

# Route to Create account page
@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if request.method == "POST":
        Type = request.form['Type']
        Cust_id = request.form['id']
        Amount = request.form['Amount']
        try:
            cur = mysql.connection.cursor()
            cur.execute("SELECT max(Account_id) from account")
            maxid = cur.fetchone()
            Account_id = int(maxid[0]) + 1
            accId = '0' * \
                (9 - (math.floor(math.log(Account_id, 10) + 1))) + str(Account_id)
            cur.execute("INSERT INTO account(Type,Cust_id,Account_id,Amount,Message,Timestamp) VALUES (%s,%s,%s,%s,%s,CURRENT_TIMESTAMP())",
                        (Type, Cust_id, accId, Amount, "Account Created"))
            mysql.connection.commit()
            return("Success")
        except Exception as e:
            return(str(e))
        finally:
            cur.close()
    elif request.method == "GET":
        if 'username' in session:
            if session['role'] == 'Exec':
                return render_template('create_account.html')
            else:
                return render_template('cashier.html')
        else:
            return render_template('login.html')

# Route to Deposite money page
@app.route('/deposit_money', methods=['GET', 'POST'])
def deposit_money():
    if request.method == "POST":
        Cust_id = request.form['cid']
        Account_id = request.form['Account_id']
        Type = request.form['Type']
        Amount = request.form['bal']
        DAmount = request.form['DAmount']
        try:
            cur = mysql.connection.cursor()
            sql = "SELECT Amount from retail_bank.account where Account_id=%s"
            cur.execute(sql, (Account_id,))
            record = cur.fetchone()

            val = (record, DAmount, "account created", Account_id)
            cur.execute(
                "UPDATE retail_bank.account SET Amount=%s+%s , Message=%s,Timestamp = CURRENT_TIMESTAMP() WHERE Account_id=%s", val)

            sql = "SELECT CURRENT_DATE()"
            cur.execute(sql)
            re = cur.fetchone()

            val = (Account_id, re[0], "Deposit", DAmount)
            sql = "INSERT INTO retail_bank.transactions (Account_id,trans_date,descript,amount) VALUES (%s,%s,%s,%s)"
            cur.execute(sql, val)

            mysql.connection.commit()
            return("done")
        except Exception as e:
            return(str(e))
        finally:
            cur.close()
    elif request.method == "GET":
        if 'username' in session:
            if session['role'] == 'Cashier':
                return render_template('deposit_money.html')
            else:
                return render_template('executive.html')
        else:
            return render_template('login.html')

# Route to withdraw page
@app.route('/withdraw_money', methods=['GET', 'POST'])
def withdraw_money():
    if request.method == "POST":
        Cust_id = request.form['cid']
        Account_id = request.form['Account_id']
        Type = request.form['Type']
        Amount = request.form['bal']
        WAmount = request.form['WAmount']
        try:
            cur = mysql.connection.cursor()
            sql = "SELECT Amount from retail_bank.account where Account_id=%s"
            cur.execute(sql, (Account_id,))
            rec = cur.fetchone()

            val = (rec, WAmount, "account created", Account_id)
            cur.execute(
                "UPDATE retail_bank.account SET Amount=%s-%s , Message=%s,Timestamp = CURRENT_TIMESTAMP() WHERE Account_id=%s", val)

            sql = "SELECT CURRENT_DATE()"
            cur.execute(sql)
            r = cur.fetchone()

            val = (Account_id, r[0], "Withdraw", WAmount)
            sql = "INSERT INTO retail_bank.transactions (Account_id,trans_date,descript,amount) VALUES (%s,%s,%s,%s)"
            cur.execute(sql, val)

            mysql.connection.commit()
            return("done")
        except Exception as e:
            return(str(e))
        finally:
            cur.close()
    elif request.method == "GET":
        if 'username' in session:
            if session['role'] == 'Cashier':
                return render_template('withdraw_money.html')
            else:
                return render_template('executive.html')
        else:
            return render_template('login.html')

# Get old data
@app.route('/get_old_data', methods=['POST'])
def get_old_data():
    id = request.form['ssn']
    try:
        cur = mysql.connection.cursor()
        sql = "SELECT Name,Age,Address from customer where id=%s"
        cur.execute(sql, (id,))
        record = cur.fetchone()
        return jsonify(record)
    except Exception as e:
        return(str(e))
    finally:
        cur.close()

# Route to View customer page
@app.route('/view_cust', methods=['GET'])
def view_cust():
    if request.method == "GET":
        if 'username' in session:
            if session['role'] == 'Exec':
                try:
                    cur = mysql.connection.cursor()
                    cur.execute(
                        "SELECT id, Cust_id, Message, Timestamp from customer")
                    data = cur.fetchall()
                    mysql.connection.commit()

                except Exception as e:
                    return(str(e))
                finally:
                    cur.close()

                return render_template('view_cust.html', data=data)
                return render_template('create_customer.html')
            else:
                return render_template('cashier.html')
        else:
            return render_template('login.html')

# Route to View account page
@app.route('/view_acc', methods=['GET', 'POST'])
def view_acc():
    if request.method == "GET":
        if 'username' in session:
            if session['role'] == 'Exec':
                try:
                    cur = mysql.connection.cursor()
                    cur.execute(
                        "SELECT Type, Cust_id, Account_id, Message, Timestamp from account")
                    data = cur.fetchall()
                    mysql.connection.commit()

                except Exception as e:
                    return(str(e))
                finally:
                    cur.close()

                return render_template('view_acc.html', data=data)
            else:
                return render_template('cashier.html')
        else:
            return render_template('login.html')

# Route to Delete account page
@app.route('/delete_account', methods=['GET', 'POST'])
def delete_account():
    if request.method == "POST":
        try:
            Account_id = request.form['Account_id']
            cur = mysql.connection.cursor()
            sql = "DELETE from account where Account_id =%s;"
            cur.execute(sql, (Account_id,))
            mysql.connection.commit()
            return("done")
        except Exception as e:
            return(str(e))
        finally:
            cur.close()
    elif request.method == "GET":
        if 'username' in session:
            if session['role'] == 'Exec':
                return render_template('delete_account.html')
            else:
                return render_template('cashier.html')
        else:
            return render_template('login.html')

# Route to Statement page
@app.route('/statement', methods=['GET', 'POST'])
def statement():
    if request.method == "POST":
        id = request.form['Account_id']
        NT = request.form['nt']
        ST = request.form['sdate']
        ET = request.form['edate']

        if(NT):
            try:
                cur = mysql.connection.cursor()
                val = (id, int(NT))
                cur.execute(
                    "SELECT trans_id, trans_date, descript, amount FROM transactions WHERE Account_id=%s ORDER BY trans_date DESC LIMIT %s", val)
                data = cur.fetchall()
                mysql.connection.commit()
            except Exception as e:
                return(str(e))
            finally:
                cur.close()
        elif(ST):
            try:
                cur = mysql.connection.cursor()
                val = (id, ST, ET)
                cur.execute(
                    "SELECT trans_id, trans_date, descript, amount FROM transactions WHERE Account_id=%s and trans_date BETWEEN %s AND %s ORDER BY trans_date DESC", val)
                data = cur.fetchall()
                mysql.connection.commit()

            except Exception as e:
                return(str(e))
            finally:
                cur.close()
        return render_template('statement_op.html', data=data)

    elif request.method == "GET":
        if 'username' in session:
            if session['role'] == 'Cashier':
                return render_template('statement.html')
            else:
                return render_template('executive.html')
        else:
            return render_template('login.html')

# Route to Transfer money page
@app.route('/transfer_money', methods=['GET', 'POST'])
def transfer_money():
    if request.method == "POST":
        Cust_id = request.form['cid']
        SType = request.form['SType']
        TType = request.form['TType']
        TAmount = request.form['TAmount']
        try:
            cur = mysql.connection.cursor()
            cur.execute(
                "SELECT Amount,Account_id from retail_bank.account WHERE Cust_id = %s AND Type = %s", (Cust_id, SType))
            Source = cur.fetchone()
            Samount = Source[0]
            acid = Source[1]
            cur.execute("UPDATE account SET Amount =%s-%s WHERE Account_id = %s AND Type = %s",
                        (Samount, TAmount, acid, SType))

            sql = "SELECT CURRENT_DATE()"
            cur.execute(sql)
            r6 = cur.fetchone()

            cur.execute(
                "SELECT Amount,Account_id from retail_bank.account WHERE Cust_id = %s AND Type = %s", (Cust_id, TType))
            Target = cur.fetchone()
            Tamount = Target[0]
            aid = Target[1]
            cur.execute("UPDATE account SET Amount = %s+%s WHERE Account_id = %s AND Type = %s",
                        (Tamount, TAmount, aid, TType))

            sql = "SELECT CURRENT_DATE()"
            cur.execute(sql)
            r7 = cur.fetchone()

            w2 = (acid, r7[0], "Transfer", TAmount)
            sql = "INSERT INTO transactions (Account_id,trans_date,descript,amount) VALUES (%s,%s,%s,%s)"
            cur.execute(sql, w2)

            mysql.connection.commit()
            return("Success")
        except Exception as e:
            return(str(e))
        finally:
            cur.close()

    elif request.method == "GET":
        if 'username' in session:
            if session['role'] == 'Cashier':
                return render_template('transfer_money.html')
            else:
                return render_template('executive.html')
        else:
            return render_template('login.html')

# Main Function 
if __name__ == '__main__':
    app.run()
