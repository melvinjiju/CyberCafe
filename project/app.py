from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'your_secret_key'


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'cybercafe'
mysql = MySQL(app)

timedata = None
message = ""
@app.route('/')
def home():
    return render_template('index.html', data = message)

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    sys_id = request.form['sys_id']
    cur = mysql.connection.cursor()

    # Execute SQL query to retrieve user data
    cur.execute("SELECT * FROM auth_table WHERE user = %s AND pass = %s", (username, password))
    
    # Fetch the result
    user = cur.fetchone()
    # Close the cursor
    if user and username == 'admin' and sys_id == 'C10':
        session['username'] = username
        return render_template("dashboard.html")
    
    if user and username != 'admin':
        # User exists, perform your login logic
        session['username'] = username 
        cur.execute("SELECT NOW() AS current_datetime;")
        timedata = cur.fetchone()
        session['timedata'] = timedata
        session['sys_id'] = sys_id
        cur.execute("INSERT INTO billing_table(user, start_time, sys_id)VALUES (%s,%s,%s);", (username, timedata,sys_id))
        cur.execute("update sys_table set user = %s where sys_id = %s", (username, sys_id))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('user_dashboard'))
    else:
        # User does not exist or incorrect credentials
        message = "Invalid credentials!!"
        return render_template('index.html', data = message)


@app.route('/user_dashboard')
def user_dashboard():
    username = session['username']
    cur = mysql.connection.cursor()
    cur.execute("select name from user_table where user = %s", (username, ))
    res = cur.fetchone()
    cur.close()
    return render_template('user_dashboard.html', data = res[0])


@app.route('/logout', methods = ['POST'])
def logout():
    timer = request.form['timerValue']
    print(timer)
    timedata = session['timedata']
    username = session['username']
    sys_id = session['sys_id']
    cur = mysql.connection.cursor()
    timer_float = float(timer)
    cosst = timer_float/5
    data = "Please pay : " + "₹" + str(timer_float/5) 
    cur.execute('update billing_table set end_time = NOW(), tot_time = %s, cost = %s where user = %s and start_time = %s', (timer, cosst, username, timedata))
    cur.execute("update sys_table set user = null where sys_id = %s", (sys_id, ))
    mysql.connection.commit()
    cur.close()
    session.pop('username', None)
    session.pop('timedata', None)
    session.pop('sys_id', None)
    return render_template('thank_user.html', cost = data )

@app.route('/about')
def about():
    return render_template('index2.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/signup_form', methods=['POST'])
def signup_form():
    
    username = request.form['username']
    password = request.form['password']
    gender = request.form['gender']
    contact = request.form['contact']
    age = request.form['age']
    name = request.form['name']
    # Insert user details into the user table
    
    cursor = mysql.connection.cursor()
    cursor.execute('INSERT INTO user_table (user, name, age, contact, gender) VALUES (%s, %s, %s, %s, %s);', (username, name, age, contact, gender))
    cursor.execute('INSERT INTO auth_table (user, pass) VALUES (%s, %s);', (username, password))
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for('home'))

@app.route('/customer')
def customer():
    return render_template('customer.html')

@app.route('/customer_form', methods=['POST'])
def customer_form():
    search_name = request.form['customerName']
    try:
    # Retrieve customer details from the database based on the search_name
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM user_table WHERE user = %s", (search_name,))
        searched_customer = cur.fetchone()
        cur.close()
    except:
        flash('Customer not found', 'error')
        return redirect(url_for('customer'))
    
    if searched_customer is not None:
        # Render a template to display the customer details
        return render_template('customer_details.html', customer=searched_customer)
    else:
        # Flash an error message
        flash('Customer not found', 'error')

        # Redirect to the customer search page
        return redirect(url_for('customer'))


@app.route('/delete')
def delete():
    return render_template('delete.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/delete_form', methods=['POST'])
def delete_form():
    
    delete_name = request.form['deleteName']
        # Delete the customer from the database
    cur = mysql.connection.cursor()
    res = cur.execute("DELETE FROM auth_table WHERE user = %s", (delete_name, ))
    cur.execute("DELETE FROM user_table WHERE user = %s", (delete_name, ))
    mysql.connection.commit()
    cur.close()
    if res == 0:
         flash('Customer not found', 'error')

    # Redirect to the customer search page
         return redirect(url_for('delete'))
    else:
        flash('Customer deleted successfully', 'success')
        return redirect(url_for('delete'))
   
    
        
    
@app.route('/admin_logout')
def admin_logout():
    # Assuming 'login' is the name of the route for your login page
    session.pop('username', None)
    return redirect(url_for('home'))

@app.route('/billing')
def billing():
    return render_template('billing.html')

@app.route('/billing_form', methods = ['POST'])
def billing_form():
    search = request.form['customerName']
    try:
        cur = mysql.connection.cursor()
        cur.execute("select * from billing_table where user = %s", (search, ))
        res = cur.fetchall()
        cur.execute("select name from user_table where user = %s", (search, ))
        name = cur.fetchone()
        cur.close()
    except:
        flash('User not found', 'error')
        redirect(url_for('billing'))
    if name is not None:
        # Render a template to display the customer details
        return render_template('billing_details.html', customers = res, cus_name = name[0])
    else:
        # Flash an error message
        flash('Customer not found', 'error')

        # Redirect to the customer search page
        return redirect(url_for('billing'))    
    

@app.route('/update')
def update():
    return render_template('update.html')

@app.route('/current_users')
def current_users():
    cur = mysql.connection.cursor()
    cur.execute("select * from sys_table")
    res = cur.fetchall()
    cur.close()
    return render_template('current_users.html', data = res)

@app.route('/update_users', methods = ['POST'])
def update_users():
    search = request.form['customerName']
    session['search'] = search
    cur = mysql.connection.cursor()
    cur.execute("select * from user_table where user = %s;", (search, ))
    res = cur.fetchone()
    cur.close()
    if res is not None:
        # Render a template to display the customer details
        return render_template('update_form.html', customer = res)
    else:
        # Flash an error message
        flash('Customer not found', 'error')

        # Redirect to the customer search page
        return redirect(url_for('update'))    
    

@app.route('/update_form', methods = ['POST'])
def update_form():
    search = session['search']
    name = request.form['name']
    age = request.form['age']
    contact = request.form['contact']
    gender = request.form['gender']
    cur = mysql.connection.cursor()
    print(name)
    cur.execute("update user_table set name = %s, age = %s, contact = %s, gender = %s where user = %s;", (name, age, contact, gender, search))
    mysql.connection.commit()
    cur.close()
    session.pop('search', None)
    return render_template('dashboard.html')
    
if __name__ == '__main__':
    app.run(debug=True) 