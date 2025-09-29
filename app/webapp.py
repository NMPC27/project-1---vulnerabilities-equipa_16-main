from flask import Flask
from flask import request
from flask import render_template
from flask import session
import sqlite3 as sql
import re
import os
from werkzeug.utils import safe_join

email_check = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
def verify_email(email):
	return True


password_check= re.compile('[@_!#$%^&*()<>?/\|}{~:]')
def verify_password(password):
	return True


app = Flask(__name__)

app.secret_key = b'@A~,;N^s`d7b\a"P' #-> time to brute force = 1Tn years

@app.route("/") 
def index():
	if 'username' in session:
		return render_template('index.html',user=session["username"])

	return render_template('index.html')

@app.route("/products")
def products():
	db = sql.connect("webDB.db")
	result = db.execute("SELECT ID_product,name,img_path FROM products;")
	rows = result.fetchall()
	db.close()

	lista_produtos=[]
	for row in rows:
		id=row[0]
		name=row[1]
		img=row[2].split("%")
		lista_produtos.append([id,name,img[0]])

	if 'username' in session:
		return render_template('products.html',lista=lista_produtos,user=session["username"])

	return render_template('products.html',lista=lista_produtos)

@app.route("/about")
def about():
	if 'username' in session:
		return render_template('about.html',user=session["username"])

	return render_template('about.html')

@app.route("/login_page")
def login_page(*args):
	if len(args)>0 :
		return render_template('login.html',alert=args[0])
	return render_template('login.html')

@app.route("/login",methods=['GET']) #! atençao ao erro do GET # Method Not Allowed
def login():
	user=request.args.get('user', '')
	password=request.args.get('password', '')

	db = sql.connect("webDB.db")
	result = db.execute("SELECT * from users WHERE user='"+user+"' AND pass='"+password+"';")
	if result.fetchall():
		db.close()
		session['username'] = user
		return account()
	else:
		db.close()
		return login_page(1)
	

@app.route("/sign_up",methods=['GET']) #! atençao ao erro do GET # Method Not Allowed
def sign_up():
	user=request.args.get('user', '')
	password=request.args.get('password', '')
	email=request.args.get('email', '')

	db = sql.connect("webDB.db")
	result = db.execute("SELECT user FROM users WHERE user='"+user+"';")
	data = result.fetchall()
	db.close()

	if data!=[]:
		return login_page(4)#username ja usado
	if not(verify_email(email)):
		return login_page(2)#email n valido
	if not(verify_password(password)):
		return login_page(3)#pass n valida

	#adicionar à db
	db = sql.connect("webDB.db")
	db.execute("INSERT INTO users VALUES (NULL,'"+user+"','"+password+"',"+"0"+",'"+email+"',NULL);")
	db.commit()
	db.close()

	session['username'] = user
	return render_template('add_avatar.html')

@app.route("/add_avatar",methods=['POST'])
def add_avatar():
	if 'username' in session:
		file = request.files['avatar']
		user_path=os.path.join(os.path.dirname(os.path.abspath(__file__)),"static/user_data",session['username'])
		os.mkdir(user_path)
		filename = file.filename
		file.save(os.path.join(user_path, filename))

		db = sql.connect("webDB.db")
		db.execute("UPDATE users SET avatar='"+filename+"' WHERE user='"+session['username']+"';")
		db.commit()
		db.close()

		return account()

	return index()

@app.route("/account")
def account(*fix):
	if 'username' in session:
		db = sql.connect("webDB.db")
		result = db.execute("SELECT * FROM users WHERE user='"+session["username"]+"';")
		data = result.fetchall()
		db.close()

		return render_template('account.html',user=data[0][1],money=data[0][3],email=data[0][4],avatar=os.path.join("static/user_data",session["username"],data[0][5]),fix=fix)
	return login_page()

@app.route('/<item>')
def products_item(item):

	if item=="all":
		return products()

	db = sql.connect("webDB.db")
	result = db.execute("SELECT ID_product,name,img_path FROM products;")
	rows = result.fetchall()
	db.close()

	lista_produtos=[]
	for row in rows:
		name=row[1]
		if item in name.lower(): #! DANGER sql possible injection
			id=row[0]
			img=row[2].split("%")
			lista_produtos.append([id,name,img[0]])

	if 'username' in session:
			return render_template('products.html',lista=lista_produtos,user=session["username"])

	return render_template('products.html',lista=lista_produtos)

@app.route('/search', methods=['GET']) #! atençao ao erro do GET # Method Not Allowed
def products_search():
	
	item=request.args.get('search_name', '')
	query=item.split(";")

	rows=[]
	db = sql.connect("webDB.db")

	item = query[0].replace("%'", "")

	result = db.execute("SELECT ID_product,name,img_path FROM products WHERE name LIKE '%"+item+"%';")
	rows = result.fetchall()

	if len(query)>1:
		for i in range(1,len(query)):
			db.execute(query[i])

	db.close()

	lista_produtos=[]#lista de tuplos

	for row in rows:      
		name=row[1]
		if item in name.lower(): #! DANGER sql possible injection
			id=row[0]
			img=row[2].split("%")
			lista_produtos.append([id,name,img[0]])

	if 'username' in session:
			return render_template('products.html',lista=lista_produtos,user=session["username"])

	return render_template('products.html',lista=lista_produtos)


@app.route('/buy/<item>')
def buy_item(item):
	db = sql.connect("webDB.db")
	result = db.execute("SELECT * FROM products WHERE ID_product="+item+";")
	data = result.fetchall()
	db.close()

	name=data[0][1]
	img=data[0][2].split("%")
	price=data[0][3]
	description=data[0][4]

	if 'username' in session:
			return render_template('buy.html',id=item,name=name,img=img,price=price,description=description,user=session["username"])

	return render_template('buy.html',id=item,name=name,img=img,price=price,description=description)

@app.route('/logout')
def logout():
	# remove the username from the session if it's there
	session.pop('username', None)
	return index()

@app.route('/checkout/<item>')
def checkout(item):  
	db = sql.connect("webDB.db")
	result = db.execute("SELECT name,price FROM products WHERE ID_product="+item+";")
	product = result.fetchall()
	
	result = db.execute("SELECT ID,money FROM users WHERE user='"+session['username']+"';")
	user = result.fetchall()

	res=user[0][1]-product[0][1]

	if res>=0:#pode comprar 
		db.execute("UPDATE users SET money="+str(res)+" WHERE ID="+str(user[0][0])+";")
		db.commit()
		db.close()
		return bought(product[0][0])

	else:#n pode comprar
		db.close()
		return bought()

@app.route('/bought')
def bought(*product_name): 
	if product_name==():
		return render_template("bought.html",product_name=None,user=session['username'])

	return render_template("bought.html",product_name=product_name[0],user=session['username'])

@app.route('/changePassword/<username>') 
def changePassword(*args,username):   
	if 'username' in session:
			if len(args)>0:
				return render_template('changePassword.html',alert=args[0],user=username)
			return render_template('changePassword.html',user=username)

	return index()

@app.route('/password_changed/<username>', methods=['GET']) 
def password_changed(username):   
	if 'username' in session:
		pass1=request.args.get('pass1', '')
		pass2=request.args.get('pass2', '')

		if pass1==pass2:
			if verify_password(pass1):
				db = sql.connect("webDB.db")
				db.execute("UPDATE users SET pass='"+pass1+"' WHERE user='"+username+"';")
				db.commit()
				db.close()
				return account(1)
			return changePassword(2)
		else:
			return changePassword(1)


	return index()

@app.route('/client_support', methods=['GET']) 
def client_support():   

	user=None
	if 'username' in session:
		user=session['username']

	nome=request.args.get('name', '')
	msg=request.args.get('msg', '')
	query=msg.split(";")

	db = sql.connect("webDB.db")
	if nome!="":#clicou no form
		result = db.execute("INSERT INTO client_support VALUES (NULL,'"+nome+"','"+query[0]+"');")
		db.commit()
		if len(query)>1:
			for i in range(1,len(query)):
				db.execute(query[i])
				db.commit()
		
	result = db.execute("SELECT name,msg FROM client_support;")
	msgs = result.fetchall()
	db.close()

	return render_template('client_support.html',user=user,msg_list=msgs)



app.run(debug=True)#! true=vulnerabilidades
