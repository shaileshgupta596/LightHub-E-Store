from flask_mail import Message
from flask import render_template

def EmailVerification(username,otp):
	try:
		msg = Message(subject="Email Verification",
		  sender="lighthub4@gmail.com",
		  recipients=[username])
		msg.html=render_template('message/message.html',username=username,otp=otp)
		return msg
	except Exception as  e:
		return(str(e))

def ForgotMail(email,otp):
	try:
		msg = Message(subject="Forgot Password",
		  sender="lighthub4@gmail.com",
		  recipients=[email])
		msg.html=render_template('message/forgotpasswordotp.html',otp=otp)
		return msg
	except Exception as  e:
		return(str(e))

def SuccsessfullyRegister(email,cname):
	try:
		msg = Message(subject="Succsessfully Register",
		  sender="lighthub4@gmail.com",
		  recipients=[email])
		msg.html=render_template('message/sucessfullyregister.html',username=cname)
		return msg
	except Exception as  e:
		return(str(e))

def CustomerPlacedOrder(session,orderid):

	email=session['Customer_username_lighthub']
	try:
		msg = Message(subject="Order Placed",
		  sender="lighthub4@gmail.com",
		  recipients=[email])
		msg.html=render_template('message/sucessfullyplacedorderemail.html',session=session,orderid=orderid)
		return msg
	except Exception as  e:
		return(str(e))

def OrderCancelByUser(email,orderid):
	username="shailesh"
	try:
		msg = Message(subject="Order Cancel",
		  sender="lighthub4@gmail.com",
		  recipients=[email])
		msg.html=render_template('message/usercancelordermessage.html',email=email,orderid=orderid)
		return msg
	except Exception as  e:
		return(str(e))


def statusmailbyadminOC(email,status,orderid):
	try:
		msg = Message(subject="Order Confirmation",
		  sender="lighthub4@gmail.com",
		  recipients=[email])
		msg.html=render_template('message/statusemail.html',email=email,orderid=orderid,status=status)
		return msg
	except Exception as  e:
		return(str(e))

def statusmailbyadminOP(email,status,orderid):
	try:
		msg = Message(subject="Order Process",
		  sender="lighthub4@gmail.com",
		  recipients=[email])
		msg.html=render_template('message/statusemail.html',email=email,orderid=orderid,status=status)
		return msg
	except Exception as  e:
		return(str(e))

def statusmailbyadminOD(email,status,orderid):
	try:
		msg = Message(subject="Order Dispatch",
		  sender="lighthub4@gmail.com",
		  recipients=[email])
		msg.html=render_template('message/statusemail.html',email=email,orderid=orderid,status=status)
		return msg
	except Exception as  e:
		return(str(e))

def statusmailbyadminODI(email,status,orderid):
	try:
		msg = Message(subject="Order Delivered",
		  sender="lighthub4@gmail.com",
		  recipients=[email])
		msg.html=render_template('message/statusemail.html',email=email,orderid=orderid,status=status)
		return msg
	except Exception as  e:
		return(str(e))