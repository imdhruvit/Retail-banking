from flask import Flask, render_template, request,jsonify
from flask_mysqldb import MySQL
import os,json,math
app = Flask(__name__,static_url_path='',static_folder='static',template_folder='templates')

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

@app.route('/delete_customer', methods=['GET','POST'])
def delete_customer():
    if request.method == "POST":
        id = request.form['id']
        try:
            cur = mysql.connection.cursor()
            sql = "DELETE from customer where id =%s;"
            cur.execute(sql,(id,))
            mysql.connection.commit()
            return("done")
        except Exception as e:
            return(str(e))

        finally:
            cur.close()
    return render_template('delete_customer.html')

@app.route('/search_customer', methods=['GET', 'POST'])
def search_customer():
    if request.method == "GET":
        return render_template('search_customer.html')

@app.route('/update_customer', methods=['GET', 'POST'])
def update_customer():
    if request.method == "POST":
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

@app.route('/search_c', methods=['POST'])
def search_c():
    id = request.form['ssn']
    sel = request.form['sel']
    if str(sel) == '1':
        try:
            cur = mysql.connection.cursor()
            sql = "SELECT id,Cust_id,Name,Age,Address,State,City,Timestamp from customer where id=%s"
            cur.execute(sql,(id,))
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
            cur.execute(sql,(id,))
            record = cur.fetchone()
            return jsonify(record)
        except Exception as e:
            return(str(e))
        finally:
            cur.close()

@app.route('/create_account',methods=['GET','POST'])
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
            accId = '0'*(9-(math.floor(math.log(Account_id, 10)+1))) + str(Account_id)
            cur.execute("INSERT INTO account(Type,Cust_id,Account_id,Amount,Message,Timestamp) VALUES (%s,%s,%s,%s,%s,CURRENT_TIMESTAMP())",(Type,Cust_id,accId,Amount,"Account Created"))
            mysql.connection.commit()
            return("Success")
        except Exception as e:
            return(str(e))
        finally:
            cur.close()
    elif request.method =="GET":
        return render_template('create_account.html')

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
            cur.execute(sql,(Account_id,))
            record = cur.fetchone()

            val = ( record , DAmount ,"account created",Account_id)
            cur.execute("UPDATE retail_bank.account SET Amount=%s+%s , Message=%s,Timestamp = CURRENT_TIMESTAMP() WHERE Account_id=%s",val)

            sql = "SELECT CURRENT_DATE()"
            cur.execute(sql)
            re = cur.fetchone()

            val = ( Account_id , re[0] ,"Deposit",DAmount)
            sql = "INSERT INTO retail_bank.transactions (Account_id,trans_date,descript,amount) VALUES (%s,%s,%s,%s)"
            cur.execute(sql,val)


            mysql.connection.commit()
            return("done")
        except Exception as e:
            return(str(e))
        finally:
            cur.close()
    elif request.method == "GET":
        return render_template('deposit_money.html')


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
            cur.execute(sql,(Account_id,))
            rec = cur.fetchone()

            val = ( rec , WAmount ,"account created",Account_id)
            cur.execute("UPDATE retail_bank.account SET Amount=%s-%s , Message=%s,Timestamp = CURRENT_TIMESTAMP() WHERE Account_id=%s",val)

            sql = "SELECT CURRENT_DATE()"
            cur.execute(sql)
            r = cur.fetchone()

            val = ( Account_id , r[0] ,"Withdraw",WAmount)
            sql = "INSERT INTO retail_bank.transactions (Account_id,trans_date,descript,amount) VALUES (%s,%s,%s,%s)"
            cur.execute(sql,val)


            mysql.connection.commit()
            return("done")
        except Exception as e:
            return(str(e))
        finally:
            cur.close()
    elif request.method == "GET":
        return render_template('Withdraw_money.html')

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

@app.route('/view_cust', methods=['GET', 'POST'])
def view_cust():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, Cust_id, Message, Timestamp from customer")
        data = cur.fetchall()
        mysql.connection.commit()

    except Exception as e:
        return(str(e))
    finally:
        cur.close()

    return render_template('view_cust.html', data=data)

@app.route('/view_acc', methods=['GET', 'POST'])
def view_acc():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT Type, Cust_id, Account_id, Message, Timestamp from account")
        data = cur.fetchall()
        mysql.connection.commit()

    except Exception as e:
        return(str(e))
    finally:
        cur.close()

    return render_template('view_acc.html', data=data)

@app.route('/delete_account', methods=['GET','POST'])
def delete_account():
    if request.method == "POST":
        try:
            Account_id = request.form['Account_id']
            cur = mysql.connection.cursor()
            sql = "DELETE from account where Account_id =%s;"
            cur.execute(sql,(Account_id,))
            mysql.connection.commit()
            return("done")
        except Exception as e:
            return(str(e))
        finally:
            cur.close()
    return render_template('delete_account.html')

@app.route('/statement', methods=['GET','POST'])
def statement():
    return render_template('statement.html')

if __name__ == '__main__':
        app.run()
