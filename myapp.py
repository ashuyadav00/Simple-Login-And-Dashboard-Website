from flask import Flask, render_template, redirect, url_for, request, abort, flash
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="mydb"
)
mycursor = mydb.cursor()

app = Flask(__name__)

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/register',methods = ['POST', 'GET'])
def register():
	if request.method == 'POST':
		fname = request.form['fname']
		lname = request.form['lname']
		email = request.form['email']
		password = request.form['password']
		confirmpassword = request.form['confirmpassword']
		sql = "SELECT email, password FROM users WHERE email = '{email}' LIMIT 1;".format(email=email)
		mycursor.execute(sql)
		myresult = mycursor.fetchall()
		if len(myresult) != 0:
			error = 'email already registered!'
			return render_template('register.html', error = error)
		elif password == confirmpassword:
			sql = "INSERT INTO users (fname,lname,email,password) VALUES (%s,%s,%s,%s)"
			val = (fname,lname,email,password)
			mycursor.execute(sql, val)
			mydb.commit()
			return redirect(url_for('login'))
		else:
			error = 'passwords are not same'
			return render_template('register.html', error = error)


	return render_template('register.html')

@app.route('/dashboard/<userid>', methods=['POST', 'GET'])
def dashboard(userid):
	if request.method =='POST':
		postname = request.form['postname']
		postdescription = request.form['postdescription']
		sql = "INSERT INTO posts (name,description,user_id) VALUES (%s,%s,%s)"
		val = (postname,postdescription,userid)
		mycursor.execute(sql, val)
		mydb.commit()
		return redirect(url_for('dashboard', userid=userid))
		
	else:
		sql1 = "SELECT name,description from posts where user_id = '{userid}'".format(userid=userid)
		mycursor.execute(sql1)
		printpost = mycursor.fetchall()
		sql2 =" SELECT fname, lname from users where id = '{userid}'".format(userid=userid)
		mycursor.execute(sql2)
		username = mycursor.fetchall()
		return render_template('dashboard.html',result = {"result":printpost, "user_id":userid,"username":username})

@app.route('/login',methods = ['POST', 'GET'])
def login():
	if request.method == 'POST':
		email = request.form['email']
		password = request.form['password']
		sql = "SELECT email, password, id FROM users WHERE email = '{email}' LIMIT 1;".format(email=email)
		mycursor.execute(sql)
		myresult = mycursor.fetchall()
		if len(myresult) == 0:
			error = 'email not found!'
			return render_template('login.html', error = error)
		if email == myresult[0][0]:
			if password == myresult[0][1]:
				userid = myresult[0][2]
				return redirect(url_for('dashboard', userid=userid))
			else:
				error = 'wrong password'
				return render_template('login.html', error = error)
		else:
			error = 'Invalid email Please try again!'
			return render_template('login.html', error = error)
	else:

		return render_template('login.html')

if __name__ == '__main__':
	app.run(debug=True)