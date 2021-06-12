import call_message 
from flask import Flask,render_template
from flask_mail import Mail, Message

app = Flask(__name__)

app.config.update(
	DEBUG=True,
	#EMAIL SETTINGS
	MAIL_SERVER='smtp.gmail.com',
	MAIL_PORT=465,
	MAIL_USE_SSL=True,
	MAIL_USERNAME = '***********',
	MAIL_PASSWORD = '***********'
	)
mail = Mail(app)
@app.route('/we')
def send_mail():
	username="shailesh"
	try:
		msg=call_message.EmailVerification()
		mail.send(msg)
		return "Mail"
	except Exception as  e:
		return(str(e))

@app.route('/')
def send_mai():
	otp=287384
	username="shailesh"
	return render_template('message/sucessfullyregister.html',username=username,otp=otp)

if __name__ == '__main__':
	app.run(debug=True)

