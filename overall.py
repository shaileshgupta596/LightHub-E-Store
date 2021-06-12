from flask import Flask
from flask import url_for,request,render_template,redirect,session,jsonify,flash
#from db import dbconnect
from functools import wraps
import database_interaction
#from mail import Email_verification,Send_Query_Mail
import call_message
import random,os
import json
from werkzeug.utils import secure_filename
import datetime
from flask_mail import Mail,Message

UPLOAD_FOLDER = 'static/images/lights/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
''' start coding for here'''
app.secret_key="abcdffgdefgac"

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

'''*****************************FLASK EMAIL**************************************'''
app.config.update(
	DEBUG=True,
	#EMAIL SETTINGS
	MAIL_SERVER='smtp.gmail.com',
	MAIL_PORT=465,
	MAIL_USE_SSL=True,
	MAIL_USERNAME = '#################',
	MAIL_PASSWORD = '##################'
	)
mail = Mail(app)
'''************************************Commen Part ****************************************'''
def encryption(val):
	val=val.lower()
	val=val.strip()
	nval=''
	for i in val:
		if i!= " ":
			nval=nval+str(ord(i))
	return nval

def login_required(f):
	@wraps(f)
	def wrap(*args ,**kwargs):
		if 'Customer_username_lighthub' in session and 'Customer_loggedin' in session :
			return f(*args ,**kwargs)
		else:
			flash('Please Logged In Yourself')
			return redirect(url_for('login'))

	return wrap

@app.route('/logout')
@login_required
def logout():
	session.clear()
	flash('You Have successfully LoggedOut')
	return redirect(url_for('login'))

def count_and_overallprice(dict1):
	tp=0
	for key ,elem in dict1.items():
		if key != 'tp':
			tp=tp+int(elem['DiscountPrice']) * int(elem['Count'])
	dict1['tp']=tp
	return dict1

def merge_dict(dict1,dict2):
	if isinstance(dict1,dict) and isinstance(dict2,dict):
		#tp=int(dict1['tp'])+int(dict2['tp'])
		main_dict =dict(list(dict1.items()) + list(dict2.items()))
		#main_dict['tp']=tp
		return count_and_overallprice(main_dict)
	else:
		return False

'''************************************CUSTOMER RELATED PROCESS*************************************'''


'''*********************************REGISTRATION RELATED DETAIL****************************************'''
@app.route('/reg',methods=['GET','POST'])
def registration():
	if request.method == 'POST':
		customername=request.form['customername'].lower()
		username=request.form['email'].lower()
		phone_number =request.form['phone_number']
		CostomerId=encryption(username)
		password=request.form['password']
		cnf_password = request.form['cnf_password']

		result =database_interaction.registration_authentication(username,phone_number,password,cnf_password)
		if result == 1:
			otp=random.randint(100000,999999)
			msg=call_message.EmailVerification(username,otp)
			mail.send(msg)
			print(otp)
			session['customername']=customername
			session['username']=username
			session['password']=password
			session['phone_number']=phone_number
			session['otp']=otp
			flash("Otp Successfully Sent on your email  "+username)
			return redirect(url_for('verify_mail'))
			'''
			database_interaction.insert_register_user(customername,username,password,phone_number)
			flash("Congratulations!! You Are Successfully Registered.")
			return redirect(url_for('login'))
			'''
		else:
			flash(result)
			return render_template('registration.html')

	return render_template("registration.html")

@app.route('/verify-mail/',methods=['GET','POST'])
def verify_mail():
	if request.method == 'POST':
		form_otp = request.form['otp']
		if form_otp == str(session['otp']):
			email=session['username']
			cname=session['customername']
			database_interaction.insert_register_user(session['customername'],session['username'],session['password'],session['phone_number'])
			#print(session)
			session.clear()
			#print(session)
			msg=call_message.SuccsessfullyRegister(email,cname)
			mail.send(msg)
			flash("Congratulations!! You Are Successfully Registered.")
			return redirect(url_for('login'))
		else:
			flash('Entered OTP Invalid. Put Correct OTP.')
			return redirect(url_for('verify_mail'))
	return render_template('verify_email.html')

'''********************************LOGIN RELATED WORK**********************************'''

@app.route('/login',methods=['GET','POST'])
def login():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		result=database_interaction.login_authentication(username,password)
		if result ==1:
			session['Customer_username_lighthub']=username
			session['Customer_loggedin']=True
			return redirect(url_for('landing_page'))
		else:
			flash("Credentials Are Wrong Try Again!")
			return render_template('login.html')
	return render_template("login.html")

@app.route('/forgotpassword',methods=['GET','POST'])
def forgot_password():
	if request.method == 'POST':
		username= request.form['username']
		result =database_interaction.checkusername(username)
		if result == 1:
			otp=random.randint(100000,999999)
			print(otp)
			session['username']=username;
			session['otp']=otp
			msg=call_message.ForgotMail(username,otp)
			mail.send(msg)
			flash("OTP has been send to your Email")
			return redirect(url_for('new_password'))
		else:
			flash(result)
			return redirect(url_for('forgot_password'))

	return render_template('forgotpassword.html')

@app.route('/new_password',methods=['GET','POST'])
def new_password():
	if request.method == 'POST':
		if request.form['otp'] == str(session['otp']):
			username =session['username']
			password=request.form['password']
			cnf_password = request.form['cnf_password']
			result =database_interaction.insert_new_password(username,password,cnf_password)
			if result=="success":
				session.clear()
				flash("Password Change Successfully")
				return redirect(url_for('login'))
			else:
				flash(result)
				return render_template("passwordchange.html")
		else:
			flash('OTP Does Not Match')
			return render_template("passwordchange.html")
	return render_template("passwordchange.html")

'''********************************CUSTOMER PROFILE RELATED WORK**********************************'''

@app.route('/customerprofile',methods=['GET','POST'])
@login_required
def customerprofile():
	username_session=""
	if 'Customer_username_lighthub' in session and 'Customer_loggedin' in session:
			username_session=session['Customer_username_lighthub']
	return render_template('customerprofile.html',username=username_session)


@app.route('/address_update_process',methods=['GET','POST'])
@login_required
def address_update_process():
	if request.method == 'POST':
		add1=request.form['add1'].lower()
		add2=request.form['add2'].lower()
		add3=request.form['add3'].lower()
		add4=request.form['add4'].lower()
		add5=request.form['add5'].lower()
		address123=add1+"@"+add2+"@"+add3+"@"+add4+"@"+add5;
		username=session['Customer_username_lighthub']

		result=database_interaction.address_update(username,address123)
		if result == 'success':
			flash('Address Upadted Successfully')
			return redirect(url_for('customerprofile'))
		else:
			flash('Not Updated')
			return redirect(url_for('customerprofile'))
	return render_template('customerprofile.html')


'''********************************CUSTOMER PROFILE DATABASE RELATED WORK**********************************'''

@app.route('/get_individual_customer_detail',methods=['GET','POST'])
@login_required
def get_individual_customer_detail():
	if request.method == 'POST':
		username = request.form['username']
		result=database_interaction.fetch_individual_customer_detail(username)
		result={"CustomerName":result[1],"Username":result[2],'PhoneNumber':result[4],
		'Address':result[5]}
		dic={"Info":result}
		return jsonify(dic)
	return redirect(url_for('exception'))

@app.route('/update_password_form_penal',methods=['POST','GET'])
@login_required
def update_password_form_penal():
	if request.method == 'POST':
		username=session['Customer_username_lighthub']
		old_password=request.form['old_password']
		password=request.form['password']
		cnf_password = request.form['cnf_password']
		result =database_interaction.insert_new_password(username,old_password,password,cnf_password)
		if result=="success":
			flash("Password Change Successfully")
			return redirect(url_for('customerprofile'))
		else:
			flash(result)
			return redirect(url_for('customerprofile'))

@app.route('/update_customer_name',methods=['POST','GET'])
@login_required
def update_customer_name():
	if request.method == 'POST':
		username=session['Customer_username_lighthub']
		customername=request.form['customername']
		result =database_interaction.update_customer_name(username,customername)
		if result=="success":
			flash("Information Change Successfully")
			return redirect(url_for('customerprofile'))
		else:
			flash("Somthing Went Wrong Try Again!!")
			return redirect(url_for('customerprofile'))

@app.route('/update_customer_phone',methods=['POST','GET'])
@login_required
def update_customer_phone():
	if request.method == 'POST':
		username=session['Customer_username_lighthub']
		phone_number=request.form['phone_number']
		result =database_interaction.update_customer_phone(username,phone_number)
		if result=="success":
			flash("Information Change Successfully")
			return redirect(url_for('customerprofile'))
		else:
			flash("Somthing Went Wrong Try Again!!")
			return redirect(url_for('customerprofile'))

@app.route('/update_customer_email',methods=['POST','GET'])
@login_required
def update_customer_email():
	if request.method == 'POST':
		username=session['Customer_username_lighthub']
		emailaddress=request.form['email']
		result =database_interaction.checkusername(emailaddress)
		if result!=1:
			otp=random.randint(100000,999999)
			msg=call_message.EmailVerification(emailaddress,otp)
			mail.send(msg)
			print(otp)
			session['username']=username
			session['emailaddress']=emailaddress
			session['otp']=otp
			flash("otp Has been send to new emailaddress")
			return redirect(url_for('emailverificationfornewemail'))
		else:
			flash("Already Present")
			return redirect(url_for('customerprofile'))

@app.route('/emailverificationfornewemail',methods=['GET','POST'])
@login_required
def emailverificationfornewemail():
	if request.method == 'POST':
		form_otp = request.form['otp']
		if form_otp == str(session['otp']):
			database_interaction.update_customer_email(session['username'],session['emailaddress'])
			#print(session)
			session.clear()
			#print(session)
			flash("Congratulations!! Your New email Registered.")
			return redirect(url_for('login'))
		else:
			flash('Entered OTP Invalid. Put Correct OTP.')
			return redirect(url_for('emailverificationfornewemail'))
	return render_template('emailverificationfornewemail.html')

'''********************************LANDING PAGE RELATED WORK**********************************'''


@app.route('/',methods=['GET','POST'])
def landing_page():
	username_session=""
	if 'Customer_username_lighthub' in session and 'Customer_loggedin' in session:
			username_session=session['Customer_username_lighthub']
	if request.method == 'POST':
		ProductName= request.form['ProductName']
		return redirect(url_for('ProductPage',ProductName=ProductName))
	#print(username_session)
	return render_template('landing.html',username=username_session)
'''********************************LANDING PAGE DATABASE RELATED WORK**********************************'''

@app.route('/getoverall_product_list',methods=['GET','POST'])
def getOverall_Product_List():
	if request.method == 'POST':
		product_list=[]
		ProductDetails=database_interaction.getoverall_product_list()
		for product in ProductDetails:
			product_list.append({"ProductName":product[1],"ProductType":product[2],
				"ProductWarranty":product[3],"ProductSpecification":product[4],
				"ProductPrice":product[5],'ProductImageAddress':product[7],
				'DiscountRate':product[12],'DiscountPrice':product[13]})

		dic={"Info":product_list}
		return jsonify(dic)

@app.route('/get_popular_product_list',methods=['GET','POST'])
def get_popular_product_list():
	if request.method == 'POST':
		sql =request.form['sql']
		product_list=[]
		ProductDetails=database_interaction.getoverall_product_list(sql)
		for product in ProductDetails:
			product_list.append({'id':product[0],'ProductId':product[1],'ProductName':product[2],
				'ProductType':product[3],'ProductWarranty':product[4],
				'ProductSpecification':product[5],
				'ProductPrice':product[6],'ProductImageAddress':product[7],
				'ProductImageAddress1':product[8],'ProductType1':product[9],
				'ProductBrand':product[10],'addeddate':product[11],
				'DiscountRate':product[12],'DiscountPrice':product[13]})

		dic={"Info":product_list}
		return jsonify(dic)

@app.route('/insert_into_watchlist',methods=['POST','GET'])
@login_required
def insert_into_watchlist():
	if request.method == 'POST':
		CustomerId =session['Customer_username_lighthub']
		ProductId =request.form['pid']
		result=database_interaction.add_into_watchlist(CustomerId,ProductId)
		if result=="1":
			dic={"Info":"1"}
			return jsonify(dic)
		if result=="2":
			dic={"Info":"2"}
			return jsonify(dic)
		if result=="3":
			dic={"Info":"3"}
			return jsonify(dic)

	return redirect(url_for('exception'))

@app.route('/get_cn',methods=['GET','POST'])
def get_cn():
	if request.method == "POST":
		username =request.form['username']
		result=database_interaction.get_cn(username)
		dic={"Info":result}
		return jsonify(dic)

	return redirect(url_for('exception'))

'''********************************PRODUCT PAGE RELATED WORK**********************************'''

@app.route('/productpage/<ProductName>',methods=['GET','POST'])
def ProductPage(ProductName):
	username_session=""
	if 'Customer_username_lighthub' in session and 'Customer_loggedin' in session:
			username_session=session['Customer_username_lighthub']
	result=list(database_interaction.ProductDetails1(ProductName))
	return render_template('ProductPage.html',username=username_session,ProductId=ProductName,result=result,session=session)

'''***********************************CART RELATED WORK******************************************'''
@app.route('/add_into_cart',methods=['GET','POST'])
@login_required
def add_into_cart():
	try:
		if request.form['pid'] and request.form['identify']=="cart" and request.method == 'POST':
			pid = request.form['pid']
			product=list(database_interaction.ProductDetails1(pid))
			print(product)
			DictItem ={pid:{'ProductName':product[2],
					'ProductType':product[3],'ProductWarranty':product[4],
					'ProductSpecification':product[5],
					'ProductPrice':int(product[6]),'ProductType1':product[9],
					'ProductBrand':product[10],'ProductImageAddress':product[7],
					'DiscountRate':product[12],'DiscountPrice':product[13],"Count":1},"tp":int(product[13])}

			if 'LightHUb_User_ShoopingCart' in session:
				if len(session['LightHUb_User_ShoopingCart']) -1 >=4:
					flash("Your Cart Limit Reached. Maximum 5 product can be added.")
					return redirect(request.referrer)

				if pid in session['LightHUb_User_ShoopingCart']:
					flash('Product Already Present In your Cart.')
					return redirect(request.referrer)
				else:
					flash("Product Added into Your Cart")
					session['LightHUb_User_ShoopingCart']=merge_dict(session['LightHUb_User_ShoopingCart'],DictItem)
					return redirect(request.referrer)
			else:
				flash("Product Added into Your Cart")
				session['LightHUb_User_ShoopingCart']=DictItem
				return redirect(request.referrer)
		else:
			pid = request.form['pid']
			product=list(database_interaction.ProductDetails1(pid))
			DictItem ={pid:{'ProductName':product[2],
					'ProductType':product[3],'ProductWarranty':product[4],
					'ProductSpecification':product[5],
					'ProductPrice':int(product[6]),'ProductType1':product[9],
					'ProductBrand':product[10],'ProductImageAddress':product[7],
					'DiscountRate':product[12],'DiscountPrice':product[13],"Count":1},"tp":int(product[13])}

			if 'LightHUb_User_ShoopingCart' in session:
				if len(session['LightHUb_User_ShoopingCart']) -1 >=4:
					flash("Your Cart Limit Reached. Maximum 5 product can be added.")
					return redirect(request.referrer)

				if pid in session['LightHUb_User_ShoopingCart']:
					flash('Product Already Present In your Cart.')
					return redirect(url_for('cart'))
				else:
					flash("Product Added into Your Cart")
					session['LightHUb_User_ShoopingCart']=merge_dict(session['LightHUb_User_ShoopingCart'],DictItem)
					return redirect(url_for('cart'))
			else:
				flash("Product Added into Your Cart")
				session['LightHUb_User_ShoopingCart']=DictItem
				return redirect(url_for('cart'))


	except Exception as e:
		print(e)
'''
	finally:
		return redirect(request.referrer) '''
'''***********************************CART PAGE RELATED WORK*************************************'''
@app.route('/cart',methods=['GET','POST'])
@login_required
def cart():
	username_session=""
	if 'Customer_username_lighthub' in session and 'Customer_loggedin' in session:
			username_session=session['Customer_username_lighthub']
	return render_template('cart.html',username=username_session,session=session)

@app.route('/delete_cart_product/<ProductId>/',methods=['GET','POST'])
@login_required
def delete_cart_product(ProductId):
	session['LightHUb_User_ShoopingCart'].pop(ProductId)
	session['LightHUb_User_ShoopingCart']=session['LightHUb_User_ShoopingCart']
	session['LightHUb_User_ShoopingCart']=count_and_overallprice(session['LightHUb_User_ShoopingCart'])
	return redirect(url_for('cart'))

@app.route('/update_product_count_in_session',methods=['GET','POST'])
@login_required
def update_product_count_in_session():
	if request.method == 'POST':
		count=request.form['pid']
		ProductId=request.form['ProductId']
		session['LightHUb_User_ShoopingCart'][ProductId]['Count']=int(count)
		session['LightHUb_User_ShoopingCart']=count_and_overallprice(session['LightHUb_User_ShoopingCart'])
		#print(session['LightHUb_User_ShoopingCart'])

		#session=session
	return redirect(request.referrer)









'''***********************************DB CONNECTIVITY*********************************************'''








'''********************************CONTACT US RELATED WORK***********************************************'''
@app.route('/contactus',methods=['POST','GET'])
def contactus():
	username_session=""
	if 'Customer_username_lighthub' in session and 'Customer_loggedin' in session:
			username_session=session['Customer_username_lighthub']
	return render_template('contactus.html',username=username_session)

'''*******************************ABOUT US RELATED WORK*********************************************'''
@app.route('/aboutus',methods=['POST','GET'])
def aboutus():
	username_session=""
	if 'Customer_username_lighthub' in session and 'Customer_loggedin' in session:
			username_session=session['Customer_username_lighthub']
	return render_template('aboutus.html',username=username_session)
'''***********************************WatchList Releted Work**********************************************'''
@app.route('/watchlist',methods=['POST','GET'])
@login_required
def watchlist():
	username_session=""
	if 'Customer_username_lighthub' in session and 'Customer_loggedin' in session:
			username_session=session['Customer_username_lighthub']
	if request.method == 'POST':
		ProductName= request.form['ProductName']
		return redirect(url_for('ProductPage',ProductName=ProductName))
	return render_template('watchlist.html',username=username_session)


@app.route('/get_watchlist',methods=['GET','POST'])
@login_required
def get_watchlist():
	if request.method == 'POST':
		username=session['Customer_username_lighthub']
		product_list=[]
		ProductDetails=database_interaction.watchlist(username)
		for product in ProductDetails:
			product_list.append({'ProductId':product[1],'ProductName':product[2],
				'ProductType':product[3],'ProductWarranty':product[4],
				'ProductSpecification':product[5],
				'ProductPrice':product[6],'ProductImageAddress':product[7],
				'ProductImageAddress1':product[8],'ProductType1':product[9],
				'ProductBrand':product[10],
				'DiscountRate':product[11],'DiscountPrice':product[12]})

		dic={"Info":product_list}
		return jsonify(dic)
	return redirect(url_for('exception'))

@app.route('/delete_watchlist',methods=['GET','POST'])
@login_required
def delete_watchlist():
	username=session['Customer_username_lighthub']
	result=database_interaction.delete_watchlist(username)
	if result=="1":
		return redirect(url_for('watchlist'))
	return redirect(url_for('exception'))

'''***********************************customer Product Filter*********************************'''
@app.route('/customerproductfilter/<value>',methods=['GET','POST'])
def customerproductfilter(value):
	username_session=""
	if 'Customer_username_lighthub' in session and 'Customer_loggedin' in session:
			username_session=session['Customer_username_lighthub']

	if request.method == 'POST':
		ProductName= request.form['ProductName']
		return redirect(url_for('ProductPage',ProductName=ProductName))
	return render_template('customerproductfilter.html',username=username_session,value=value)

@app.route('/get_customerproductfilter',methods=['GET','POST'])
def get_customerproductfilter():
	print("helloo")
	if request.method == 'POST':
		data = request.form['sql']
		data=json.loads(data)


		product_list=[]
		ProductDetails=database_interaction.customerfilter_product_list(data)
		print("hello")
		for product in ProductDetails:
			product_list.append({'id':product[0],'ProductId':product[1],'ProductName':product[2],
				'ProductType':product[3],'ProductWarranty':product[4],
				'ProductSpecification':product[5],
				'ProductPrice':product[6],'ProductImageAddress':product[7],
				'ProductImageAddress1':product[8],'ProductType1':product[9],
				'ProductBrand':product[10],'addeddate':product[11],
				'DiscountRate':product[12],'DiscountPrice':product[13]})

		dic={"Info":product_list}
		return jsonify(dic)
	else:
		return redirect(url_for('exception'))
'''***********************************EXCEPTIONS******************************************'''
@app.route('/exception',methods=['GET','POST'])
def exception():
	return render_template('exception.html')
'''************************************BUY PRODUCT PAGE RELATED**************************************'''
@app.route('/buyproduct',methods=['GET','POST'])
def buyproduct():
	username_session=""
	if 'Customer_username_lighthub' in session and 'Customer_loggedin' in session:
		username_session=session['Customer_username_lighthub']
	if 'LightHUb_User_ShoopingCart' in session:
		cart=session['LightHUb_User_ShoopingCart']
		print(len(cart))
		if len(cart)-1 < 1:
			flash("Please Add Product in Your Cart.")
			return redirect(url_for('cart'))
	return render_template('buyproduct.html',username=username_session)

'''************************************ PLACE ORDER*********************************************'''
@app.route('/placeorder',methods=['GET','POST'])
def placeorder():
	if "LightHUb_User_ShoopingCart" not in session:
		return redirect(url_for('landing_page'))
	username_session=""
	if 'Customer_username_lighthub' in session and 'Customer_loggedin' in session:
		username_session=session['Customer_username_lighthub']
	return render_template('placeorder.html',username=username_session)

@app.route('/finalpage',methods=['GET','POST'])
def finalpage():
	if "LightHUb_User_ShoopingCart" not in session:
		return redirect(url_for('landing_page'))
	username_session=""
	if 'Customer_username_lighthub' in session and 'Customer_loggedin' in session:
		username_session=session['Customer_username_lighthub']
	return render_template('finalpage.html',session=session,username=username_session)
'''
@app.route('/hi',methods=['GET','POST'])
def hi():
	orderid="LHB64763764736"
	msg=call_message.CustomerPlacedOrder(session,orderid)
	mail.send(msg)
	return render_template('message/sucessfullyplacedorderemail.html')
'''
@app.route('/finalpage_process',methods=['GET','POST'])
def finalpage_process():
	if request.method == 'POST':
		OrderID=request.form['OrderID']
		#print(OrderID)
		username =session['Customer_username_lighthub']
		cart=session['LightHUb_User_ShoopingCart']
		result =database_interaction.OrderPlaceDbWork(username,OrderID,cart)
		if result ==1:
			msg=call_message.CustomerPlacedOrder(session,OrderID)
			mail.send(msg)
			session.pop('LightHUb_User_ShoopingCart')
			print(session)
			dic={"Info":1}
			return jsonify(dic)
		else:
			return redirect(url_for('exception'))


'''*************************************Customer Order****************************************'''
@app.route('/your_orders',methods=['GET','POST'])
@login_required
def your_orders():
	if 'Customer_username_lighthub' in session and 'Customer_loggedin' in session:
		username_session=session['Customer_username_lighthub']
	return render_template('orders.html',username=username_session)

@app.route('/customer_orders',methods=['GET','POST'])
@login_required
def customer_orders():
	if request.method == 'POST':
		orderlist=[]
		username = request.form['username']
		result=database_interaction.customer_orders(username)
		for order in result:
			orderlist.append({"OrderID":order[2],"OrderConfirmation":order[3]
				,"OrderPack":order[4],"OrderDispatch":order[5],
				"OrderDeliverd":order[6],"OrderDate":order[7],"oct":order[8]})
		dic={"Info":orderlist}
		return jsonify(dic)
	return redirect(url_for('exception'))


@app.route('/Indivial_order_details',methods=['GET','POST'])
@login_required
def Indivial_order_details():
	if request.method == 'POST':
		OrderID =request.form['OrderID']
		result=database_interaction.Individual_order_details(OrderID)
		return jsonify({"Info":result})
	else:
		return redirect(url_for('exception'))

@app.route('/cancel_order',methods=['GET','POST'])
@login_required
def cancel_order():
	if request.method == 'POST':
		username= session['Customer_username_lighthub']
		OrderID=request.form['OrderID']
		result=database_interaction.ucancel_order(username,OrderID)
		if result ==1:
			msg=call_message.OrderCancelByUser(username,OrderID)
			mail.send(msg)
			flash("Your Order "+OrderID+" Been Successfully Cancelled.")
			return redirect(url_for('your_orders'))
		else:
			flash("Your Request for Cancellation Failed.")
			return redirect(url_for('your_orders'))
	else:
		return redirect(url_for('exception'))
'''*********************************COMPLTED ORDER PAGE******************************************'''
@app.route('/customercompletedorder',methods=['GET','POST'])
@login_required
def customercompletedorder():
	username_session=""
	if 'Customer_username_lighthub' in session and 'Customer_loggedin' in session:
		username_session=session['Customer_username_lighthub']
		result = database_interaction.customer_Completed_order(username_session)
	return render_template('customercompletedorder.html',username=username_session,result=result)


'''******************************** Custom Product*******************************************'''
@app.route('/custom_product',methods=['GET','POST'])
def custom_product():
	username_session=""
	if 'Customer_username_lighthub' in session and 'Customer_loggedin' in session:
		username_session=session['Customer_username_lighthub']

	if request.method == 'POST':
		customername=request.form['customername']
		email=request.form['email']
		phone_number=request.form['phone_number']
		ProductType=request.form['ProductType']
		Description=request.form['Description']
		Image=request.files['file']


		filename = secure_filename(Image.filename)
		ImageAddress="static/images/lights/"+filename;
		result=database_interaction.Send_Constomize_Infromation(customername,
			email,phone_number,ProductType,Description,ImageAddress)
		if result =="success":
			Image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			flash("Your Information Has been Successfully Send.")
			return redirect(url_for('custom_product'))
		else:
			flash("Something Went Wrong Try Again!!")
			return redirect(url_for('custom_product'))


	return render_template('customizedorder.html',username=username_session)

'''********************************Terms & Condition***************************************'''
@app.route('/Terms&Condition@PrivacyPolicy',methods=['GET','POST'])
def TermsandConditionandPrivacyPolicy():
	username_session=""
	if 'Customer_username_lighthub' in session and 'Customer_loggedin' in session:
		username_session=session['Customer_username_lighthub']
	return render_template('TermsandCondition.html',username=username_session)


@app.route('/rec',methods=['GET','POST'])
def rec():
	username_session=""
	if 'Customer_username_lighthub' in session and 'Customer_loggedin' in session:
		username_session=session['Customer_username_lighthub']
	return render_template('rec.html',username=username_session)






'''*******************************************************************ADMIN PART*****
**********************************************************************************************
**********************************************************************************************
**********************************************************************************************
**********************************************************************************************
**********************************************************************************************
**********************************************************************************************
**********************************************************************************************
**********************************************************************************************
**********************************************************************************************
**********************************************************************************************
**********************************************************************************************
**********************************************************************************************'''


def alogin_required(f):
    @wraps(f)
    def wrap(*args ,**kwargs):
        if 'admin_vishal_gupta_lighthub.com_with_other_3' in session:
            return f(*args ,**kwargs)
        else:
            flash('Please Logged In Yourself')
            return redirect(url_for('adminlogin'))
    return wrap

def already_login(f):
    @wraps(f)
    def wrap(*args ,**kwargs):
        if 'admin_vishal_gupta_lighthub.com_with_other_3' in session:
            flash('You are already loggedin')
            return redirect(url_for('adminhome'))
        else:
            return redirect(url_for('adminlogin'))
    return wrap
'''
@app.route('/logout')
@alogin_required
def logout():
    session.clear()
    flash('You Have successfully LoggedOut')
    return redirect(url_for('adminlogin')) '''

@app.route('/vspologin',methods=['GET','POST'])
def adminlogin():
    if request.method == 'POST':
        username =request.form['username']
        password = request.form['password']

        if username == "lighthub.com" and password == 'light':
            session['admin_vishal_gupta_lighthub.com_with_other_3']=True
            session['adminusername'] = username
            flash('You Have successfully Logged In')
            return redirect(url_for('adminhome'))
        else:
            return render_template('admin/adminlogin.html',elem='WP')
    else:
        return render_template('admin/adminlogin.html')


@app.route('/adminhome',methods=['GET','POST'])
@alogin_required
def adminhome():
    return render_template('admin/adminhome.html')


@app.route('/InsertNewProduct',methods=['GET','POST'])
@alogin_required
def InsertNewProduct():
    return render_template('admin/InsertNewProduct.html')

@app.route('/UpdateProductDetails',methods=['GET','POST'])
@alogin_required
def UpdateProductDetails():
    return render_template('admin/UpdateproductDetails.html')

@app.route('/RemoveProduct',methods=['GET','POST'])
@alogin_required
def RemoveProduct():
    return render_template('admin/RemoveProduct.html')

'''
def encryption(val):
    val=val.lower()
    val=val.strip()
    nval=''

    for i in val:
        if i!= " ":
            nval=nval+str(ord(i))
    return nval'''

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        ProductImage= request.files['file']
        ProductImage1=request.files['file1']
        ProductName=request.form['ProductName'].lower()
        ProductId=encryption(ProductName)
        #print(ProductId)
        ProductType=request.form['ProductType']
        ProductType1=request.form['ProductType1']
        ProductSpecification=request.form['ProductSpecification']
        ProductPrice=request.form['ProductPrice']
        ProductWarranty=request.form['ProductWarranty']
        ProductBrand=request.form['ProductBrand']
        DiscountPrise=request.form['DiscountPrice']

        filename = secure_filename(ProductImage.filename)
        filename1 = secure_filename(ProductImage1.filename)
        ProductImageAddress="static/images/lights/"+filename;
        ProductImageAddress1="static/images/lights/"+filename1
        response=database_interaction.upload_new_product(ProductId,ProductName,ProductType,ProductWarranty,ProductSpecification,ProductPrice,ProductImageAddress,ProductImageAddress1,ProductType1,ProductBrand,DiscountPrise)
        if response == 'success':
            ProductImage.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            ProductImage1.save(os.path.join(app.config['UPLOAD_FOLDER'], filename1))
            flash('Product Sucessfully Added')
            return redirect(url_for('InsertNewProduct'))
        else:
            flash('Product Already Present!')
            return redirect(url_for('InsertNewProduct'))

    else:
        flash('Product Already Present!')
        return render_template('admin/adminhome.html')


@app.route('/admin/AddPartner',methods=['GET','POST'])
@alogin_required
def AddPartner():
    return render_template('admin/AddPartner.html')

@app.route('/admin/AddPartnerProcess',methods=['GET','POST'])
def AddPartnerProcess():
    if request.method == 'POST':
        EnterpriseName=request.form['EnterpriseName']
        OwnerName=request.form['OwnerName'].lower()
        Contact1=request.form['Contact1'].lower()
        Contact2=request.form['Contact2'].lower()
        Contact3=request.form['Contact3'].lower()
        Address=request.form['Address'].lower()
        # for optinal mobile Number
        if len(Contact2) == 0:
            Contact2='-'
        result=database_interaction.InsertPartner(EnterpriseName,OwnerName,Contact1,Contact2,Contact3,Address)
        if result=='success':
            flash('Partner Added Successfully')
            return redirect(url_for('AddPartner'))
            #return render_template('Admin/AddPartner.html',elem='added')
        else:
            return redirect(url_for('exception'))

    else:
        return redirect(url_for('AddPartner'))






@app.route('/admin/PartnerManagement',methods=['GET','POST'])
@alogin_required
def PartnerManagement():
    return render_template('admin/PartnerManagement.html')


@app.route('/update_detail_page_transfer',methods=['GET','POST'])
@alogin_required
def update_detail_page_transfer():
    if request.method == 'POST':
        hiddenpid=request.form['pid']
        print("hello_world")
        return redirect(url_for('updetails',pid=hiddenpid))

@app.route('/updetails/<pid>/')
@alogin_required
def updetails(pid):
    return render_template('admin/updetails.html',pid=pid)
'''***********************************EXCEPTIONS******************************************
@app.route('/exception',methods=['GET','POST'])
def exception():
    return render_template('exception.html') '''



'''*************************************DB CONNECTIVITY ADMIN PART******************************************'''
@app.route('/get_Details_of_Partners',methods=['GET','POST'])
def get_Details_of_Partners():
    if request.method == 'POST':
        partner_list=[]
        PartnerDetails=database_interaction.LoadPartners()
        for partner in PartnerDetails:
            partner_list.append({"EnterpriseId":partner[0],"EnterpriseName":partner[1],"OwnerName":partner[2],"Contact1":partner[3],"Contact2":partner[4],"Contact3":partner[5],"Address":partner[6]})

        dic={"Info":partner_list}
        return jsonify(dic)

@app.route('/get_Details_of_Individual_Partners',methods=['GET','POST'])
def get_Details_of_Individual_Partners():
    if request.method == 'POST':
        postData = request.form['pid']
        #print("sdjbkjdk",postData)
        #print(type(postData))
        partner=database_interaction.LoadIndividualPartners(postData)
        partner={"EnterpriseId":partner[0],"EnterpriseName":partner[1],"OwnerName":partner[2],"Contact1":partner[3],"Contact2":partner[4],"Contact3":partner[5],"Address":partner[6]}

        dic={"Info":partner}
        return jsonify(dic)

@app.route('/remove_partner',methods=['GET','POST'])
def remove_partner():
    if request.method == 'POST':
        postData = request.form['pid']
        partner=database_interaction.RemovePartner(postData)
        if partner == '1':
            flash('Partner Successfully Removed.')
            return redirect(url_for('PartnerManagement'))
        else:
            return redirect(url_for('exception'))


@app.route('/get_LoadProduct',methods=['GET','POST'])
def get_LoadProduct():
    if request.method == 'POST':
        postdata = request.form['option']
        postdata1=request.form['option1']
        #print(postdata)
        product_list1=[]
        products=database_interaction.LoadProduct(postdata,postdata1)
        #print(products)
        for product in products:
            product_list1.append({'id':product[0],'ProductId':product[1],'ProductName':product[2],
                'ProductType':product[3],'ProductWarranty':product[4],
                'ProductSpecification':product[5],
                'ProductPrice':product[6],'ProductImageAddress':product[7],
                'ProductImageAddress1':product[8],'ProductType1':product[9],
                'ProductBrand':product[10],'addeddate':product[11],
                'DiscountRate':product[12],'DiscountPrice':product[13]})
    dic={"Info":product_list1}
    return jsonify(dic)

@app.route('/remove_product',methods=['GET','POST'])
def remove_product():
    if request.method == 'POST':

        postData = request.form['pid']
        #print("sdjbkjdk>",postData)
        partner=database_interaction.RemoveProduct(postData)
        if partner == '1':
            flash('Product Successfully Removed.')
            return redirect(url_for('RemoveProduct'))
        else:
            return redirect(url_for('exception'))


@app.route('/get_details_of_product',methods=['GET','POST'])
def get_Details_of_Product():
    if request.method == 'POST':

        postData = request.form['pid']
        #print("sdjbkjdk111111111111",postData)
        product=database_interaction.ProductDetails(postData)
        #print(product)
        product={'ProductId':product[1],'ProductName':product[2],
                'ProductType':product[3],'ProductWarranty':product[4],
                'ProductSpecification':product[5],
                'ProductPrise':product[6],'ProductImageAddress':product[7],
                'ProductImageAddress1':product[8],'ProductType1':product[9],
                'ProductBrand':product[10],'addeddate':product[11],
                'DiscountRate':product[12],'DiscountPrise':product[13]}
        dic={"Info":product}
        return jsonify(dic)

@app.route('/update_price',methods=['GET','POST'])
def update_price():
    if request.method == 'POST':
        hiddenpid=request.form['pid']
        ud=request.form['updateddetails']
        dprice=request.form['dprice']
        result=database_interaction.update_product_price(hiddenpid,ud,dprice)
        if result == 'success':
            dic={'Info':"1"}
            return jsonify(dic)
    return redirect(url_for("exception"))

@app.route('/update_name',methods=['GET','POST'])
def update_name():
    if request.method == 'POST':
        hiddenpid=request.form['pid']
        ud=request.form['updateddetails']
        result=database_interaction.update_product_name(hiddenpid,ud)
        if result == 'success':
            dic={'Info':"1"}
            return jsonify(dic)

@app.route('/update_type',methods=['GET','POST'])
def update_type():
    if request.method == 'POST':
        hiddenpid=request.form['pid']
        ud=request.form['updateddetails']
        print(ud)
        result=database_interaction.update_product_type(hiddenpid,ud)
        if result == 'success':
            dic={'Info':"1"}
            return jsonify(dic)


@app.route('/update_type1',methods=['GET','POST'])
def update_type1():
    if request.method == 'POST':
        hiddenpid=request.form['pid']
        ud=request.form['updateddetails']
        result=database_interaction.update_product_type1(hiddenpid,ud)
        if result == 'success':
            dic={'Info':"1"}
            return jsonify(dic)


@app.route('/update_brand',methods=['GET','POST'])
def update_brand():
    if request.method == 'POST':
        hiddenpid=request.form['pid']
        ud=request.form['updateddetails']
        result=database_interaction.update_product_brand(hiddenpid,ud)
        if result == 'success':
            dic={'Info':"1"}
            return jsonify(dic)

@app.route('/update_warranty',methods=['GET','POST'])
def update_warranty():
    if request.method == 'POST':
        hiddenpid=request.form['pid']
        ud=request.form['updateddetails']
        result=database_interaction.update_product_warranty(hiddenpid,ud)
        if result == 'success':
            dic={'Info':"1"}
            return jsonify(dic)

@app.route('/update_description',methods=['GET','POST'])
def update_description():
    if request.method == 'POST':
        hiddenpid=request.form['pid']
        ud=request.form['updateddetails']
        result=database_interaction.update_product_description(hiddenpid,ud)
        if result == 'success':
            dic={'Info':"1"}
            return jsonify(dic)

@app.route('/update_image1',methods=['GET','POST'])
def update_image1():
    if request.method == 'POST':
        if 'file' in request.files and "pid" in request.form:
            hiddenpid=request.form['pid']
            print(request.form)
            print(request.files)
            ProductImage=request.files['file']
            filename = secure_filename(ProductImage.filename)
            ProductImageAddress="static/images/lights/"+filename;

            result=database_interaction.update_product_image1(hiddenpid,ProductImageAddress)
            if result == 'success':
                ProductImage.save(os.path.join(app.config['UPLOAD_FOLDER'], filename));
                dic={'Info':"1"}
                return jsonify(dic)

        dic={'Info':"0"}
        return jsonify(dic)

@app.route('/update_image2',methods=['GET','POST'])
def update_image2():
    if request.method == 'POST':
    	#print(request.form)
        if 'file1' in request.files and "pid" in request.form:
            hiddenpid=request.form['pid']
            #print(request.form)
            #print(request.files)
            ProductImage=request.files['file1']
            filename = secure_filename(ProductImage.filename)
            ProductImageAddress="static/images/lights/"+filename;

            result=database_interaction.update_product_image2(hiddenpid,ProductImageAddress)
            if result == 'success':
                ProductImage.save(os.path.join(app.config['UPLOAD_FOLDER'], filename));
                dic={'Info':"1"}
                return jsonify(dic)

        dic={'Info':"0"}
        return jsonify(dic)
'''******************************ADMIN CANCEL ORDER PAGE*********************************************'''
@app.route('/cancel_order_page',methods=['GET','POST'])
@alogin_required
def cancel_order_page():
    result=database_interaction.cancel_order_page()
    return render_template('admin/admincancelorders.html',result=result)
'''******************************ADMIN COMPLTED ORDER PAGE*********************************************'''
@app.route('/admin_complete_orders_page',methods=['GET','POST'])
@alogin_required
def admin_complete_orders_page():
	result=database_interaction.admin_completed_order()
	return render_template('admin/admincompleteorder.html',result=result)

'''******************************ADMIN ORDERS*********************************************'''
@app.route('/admin_orders',methods=['GET','POST'])
@alogin_required
def admin_orders():
	return render_template('admin/orders.html')

@app.route('/admin_customer_orders',methods=['GET','POST'])
@alogin_required
def admin_customer_orders():
    if request.method == 'POST':
        orderlist=[]
        result=database_interaction.admin_customer_orders()
        for order in result:
            orderlist.append({"username":order[1],"OrderID":order[2],"OrderConfirmation":order[3]
                ,"OrderPack":order[4],"OrderDispatch":order[5],
                "OrderDeliverd":order[6],"OrderDate":order[7]})
        dic={"Info":orderlist}
        return jsonify(dic)
    return redirect(url_for('exception'))

@app.route('/aIndivial_order_details_completed',methods=['GET','POST'])
@alogin_required
def aIndivial_order_details_completed():
    if request.method == 'POST':
        OrderID =request.form['OrderID']
        result,personal_info=database_interaction.aIndividual_order_details_completed(OrderID)
        return jsonify({"Info":result,"personal_info":personal_info})
    else:
        return redirect(url_for('exception'))

@app.route('/aIndividual_order_details_canceled',methods=['GET','POST'])
@alogin_required
def aIndividual_order_details_canceled():
    if request.method == 'POST':
        OrderID =request.form['OrderID']
        result,personal_info=database_interaction.aIndividual_order_details_canceled(OrderID)
        return jsonify({"Info":result,"personal_info":personal_info})
    else:
        return redirect(url_for('exception'))

@app.route('/aIndivial_order_details',methods=['GET','POST'])
@alogin_required
def aIndivial_order_details():
    if request.method == 'POST':
        OrderID =request.form['OrderID']
        result,personal_info=database_interaction.aIndividual_order_details(OrderID)
        return jsonify({"Info":result,"personal_info":personal_info})
    else:
        return redirect(url_for('exception'))


@app.route('/update_customer_order_status',methods=['GET','POST'])
@alogin_required
def update_customer_order_status():
	if request.method == 'POST':
		OrderID =request.form['OrderID']
		status=request.form['status']
		result,customer_email=database_interaction.update_customer_order_status(OrderID,status)
		#username=database_interaction.get_email_for_mail(OrderID)
		if result ==1:
			if status == "OrderConfirmed":
				msg=call_message.statusmailbyadminOC(customer_email,status,OrderID)
				mail.send(msg)
			if status == "OrderPack":
				msg=call_message.statusmailbyadminOP(customer_email,status,OrderID)
				mail.send(msg)
			if status == "OrderDispatch":
				msg=call_message.statusmailbyadminOD(customer_email,status,OrderID)
				mail.send(msg)
			if status == "OrderDeliverd":
				msg=call_message.statusmailbyadminODI(customer_email,status,OrderID)
				mail.send(msg)


			return jsonify({"Info":1})
		else:
			return redirect(url_for('exception'))

	else:
		return redirect(url_for('exception'))

@app.route('/admin_cancel_order',methods=['GET','POST'])
@alogin_required
def admin_cancel_order():
    if request.method == 'POST':
        username=request.form['username']
        OrderID=request.form['OrderID']
        result=database_interaction.admin_cancel_order(username,OrderID)
        if result ==1:
            flash("LightHUb Has "+OrderID+" Been Successfully Cancelled.")
            return redirect(url_for('admin_orders'))
        else:
            flash("Your Request for Cancellation Failed.")
            return redirect(url_for('admin_orders'))
    else:
        return redirect(url_for('exception'))

@app.route('/OrderFullfilled',methods=['GET','POST'])
@alogin_required
def OrderFullfilled():
	if request.method == 'POST':
		orderid=request.form['orderid']
		result=database_interaction.OrderFullfilled(orderid)
		if result==1:
			flash("Order Id "+orderid+" Sucessfully Completed")
			return redirect(url_for('admin_orders'))
	else:
		return redirect(url_for('exception'))
"""**************************************************ADMIN COUNTER PAGE*************************************************************************************"""
@app.route('/get_counter_data',methods=['GET','POST'])
@alogin_required
def get_counter_data():
    if request.method == 'POST':
        result=database_interaction.get_counter_data()
        return jsonify({'Info':result})
    else:
        return redirect(url_for('exception'))

'''*****************************ADMIN CUTOMIZED ORDER PAGE******************************************'''
@app.route('/a_customizeorder',methods=['GET','POST'])
@alogin_required
def a_customizeorder():
    result=database_interaction.a_customizeorder()
    if request.method =='POST':
        deleteorder=request.form['deleteorder']
        result=database_interaction.delete_customized_product_query(deleteorder)
        if result==1:
            flash('Query Related to Custom Product Removed.')
            return redirect(url_for('a_customizeorder'))
    return render_template('admin/acustomizeorder.html',requests=result)

@app.route('/infoofIndividualcostomizedquery',methods=['GET','POST'])
@alogin_required
def infoofIndividualcostomizedquery():
    if request.method == 'POST':
        queryid=request.form['queryid']
        result=database_interaction.fetctIndividualCustomizedquery(queryid)
        return jsonify({"Info":result})
    else:
        return redirect(url_for('exception'))
@app.route('/reply_done',methods=['GET','POST'])
@alogin_required
def reply_done():
    if request.method == 'POST':
        queryid=request.form['queryid']
        result=database_interaction.reply_done(queryid)
        if result ==1:
            flash("Query Replied")
            return redirect(url_for('a_customizeorder'))
    else:
        return redirect(url_for('exception'))

@app.route('/individual_order_by_search',methods=['GET','POST'])
@alogin_required
def individual_order_by_search():
	result={}
	if request.method == 'POST':
		orderid=request.form['OrderID']
		result=database_interaction.bill_genaration("VLH1591975942139")
		'''
		customer_info=result['customer_info']
		Type=result['type']
		customer_info=result['customer_info']
		OrderInfo=result['OrderInfo']
		Orders=result['Orders']
		'''
		result=database_interaction.bill_genaration(orderid)
		return render_template('admin/individual_order_by_search.html',flag=1,response=result)
	
	return render_template('admin/individual_order_by_search.html',flag=0,response=result)
	

if __name__ == '__main__':
	app.run(debug=True)

