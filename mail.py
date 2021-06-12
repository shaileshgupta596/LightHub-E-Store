import smtplib, ssl
import random

sender="############"

password="###########"

port = 465
def Email_verification(recieve,otp):

	recieve = recieve

	message = "Subject:Email verification\nTo:"+str(recieve)+"\n\nDear sir/madam,\nThank you for Registering with LightHub.com .\nOne Time Password(OTP):"+str(otp)+"\nWe are here to Enlight your Dream.\nThank you.\n\nPlease Do Not Reply, This mail will be System Generated "

	context = ssl.create_default_context()

	print("Starting to send")
	with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
	    server.login(sender, password)
	    server.sendmail(sender, recieve, message)

	print("sent email!")

def Send_Query_Mail(recieve,query):

	recieve = recieve

	message = "Subject:Customer Query\nTo:"+str(recieve)+"\n\nDear sir/madam,\nGreeting from  LightHub.com .\nYour Query Has been Send To our Customer Support:'"+str(query)+"'\n\n We will revert back to Your query with 24 hours of working day.\n\nWe are here to Enlight your Dream.\nThank you.\n\nPlease Do Not Reply, This mail will be System Generated "

	context = ssl.create_default_context()

	print("Starting to send")
	with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
	    server.login(sender, password)
	    server.sendmail(sender, recieve, message)

	print("sent email!")

Send_Query_Mail("shaileshgupta596@gmail.com","Hi")
