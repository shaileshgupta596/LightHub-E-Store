from db import dbconnect
import datetime

def login_authentication(username,password):
	response=0#this value will be used to give rwsponse in webapp
	sql="SELECT * FROM customers WHERE username=%s and password =%s"
	val=(username,password,)

	c,conn=dbconnect()
	c.execute(sql,val)
	if c.rowcount== 1:
		response= 1
	c.close()
	conn.close()
	return response

	
def registration_authentication(username,phone_number,password,cnf_password):
	response=""
	c,conn = dbconnect()
	sql="SELECT username FROM customers WHERE username=%s "
	val=(username,)
	c.execute(sql,val)
	#print(val)
	print(c.rowcount)
	if c.rowcount >0:
		response="Email Already Already Exist!"
		return response
	if c.rowcount == 0:
		if password !=cnf_password:
			response ="Password doest Not Match!"
			return response
		else:
			response=1
			return response
 
def insert_register_user(Customerid,username,password,phone_number):


	sql="INSERT INTO customers (CustomerId,username,password,PhoneNumber)  VALUES (%s,%s,%s,%s)"
	value=(Customerid,username,password,phone_number,)

	c,conn=dbconnect()
	c.execute(sql,value)
	conn.commit()
	c.close()
	conn.close()
	return 	"success"
	
def encryption(val):
	val=val.lower()
	val=val.strip()
	nval=''
	for i in val:
		if i!= " ":
			nval=nval+str(ord(i))
	return nval

def checkusername(username):
	c,conn = dbconnect()
	sql="SELECT username FROM customers WHERE username=%s "
	val=(username,)
	c.execute(sql,val)
	#print(val)
	print(c.rowcount)
	if c.rowcount ==0:
		response="Email Address is Not Present!Try Email Which is used for Registration!!"
		return response
	if c.rowcount == 1:
		return 1


#forgot password
def insert_new_password(username,password,cnf_password):
	if password!=cnf_password or len(password)<8 or len(cnf_password)<8:
		return "Password does not match ! OR Password Policy does not match!"
	
	
	c,conn=dbconnect()
	sql='''UPDATE customers SET password=%s where username=%s '''
	value=(password,username)
	c.execute(sql,value)
	conn.commit()
	c.close()
	conn.close()
	return 'success'

#chaning from panel
def insert_new_password_from_panel(username,old_password,password,cnf_password):
	if password!=cnf_password or len(password)<8 or len(cnf_password)<8:
		return "Password does not match ! OR Password Policy does not match!"
	
	c,conn=dbconnect()
	sql="""SELECT * FROM customers WHERE username=%s and password=%s"""
	value=(username,old_password)
	c.execute(sql,value)
	count=c.rowcount
	conn.commit()
	c.close()
	conn.close()
	if count ==1:
		c,conn=dbconnect()
		sql='''UPDATE customers SET password=%s where username=%s'''
		value=(password,username)
		c.execute(sql,value)
		conn.commit()
		c.close()
		conn.close()
		return 'success'
	return "Current Password Not Correct"

def address_update(username,address):
	sql='''UPDATE customers SET Address=%s where username=%s '''
	value=(address,username)

	c,conn=dbconnect()
	c.execute(sql,value)
	conn.commit()
	c.close()
	conn.close()
	return 	"success"

def fetch_individual_customer_detail(username):
	sql='''SELECT * FROM customers WHERE username=%s '''
	value=(username,)
	c,conn=dbconnect()
	c.execute(sql,value)
	data=c.fetchone()
	#print(data)
	conn.commit()
	c.close()
	conn.close()
	return 	data

def update_customer_name(username,customername):
	sql="""UPDATE customers SET CustomerId=%s WHERE username=%s """
	value=(customername,username)
	c,conn=dbconnect()
	c.execute(sql,value)
	conn.commit()
	c.close()
	conn.close()
	return 	"success"

def update_customer_phone(username,PhoneNumber):
	sql="""UPDATE customers SET PhoneNumber=%s WHERE username=%s """
	value=(PhoneNumber,username)
	c,conn=dbconnect()
	c.execute(sql,value)
	conn.commit()
	c.close()
	conn.close()
	return 	"success"
'''*********************************MOST IMPORTANT******************************************'''
'''*********************************MOST IMPORTANT******************************************'''
'''*********************************MOST IMPORTANT******************************************'''
'''*********************************MOST IMPORTANT******************************************'''
'''*********************************MOST IMPORTANT******************************************'''
'''*********************************MOST IMPORTANT******************************************'''
'''*********************************MOST IMPORTANT******************************************'''
'''*********************************MOST IMPORTANT******************************************'''
'''*********************************MOST IMPORTANT******************************************'''
'''*********************************MOST IMPORTANT******************************************'''
'''*********************************MOST IMPORTANT******************************************'''
'''*********************************MOST IMPORTANT******************************************'''
'''*********************************MOST IMPORTANT******************************************'''
'''*********************************MOST IMPORTANT******************************************'''
'''*********************************MOST IMPORTANT******************************************'''
'''*********************************MOST IMPORTANT******************************************'''
'''*********************************MOST IMPORTANT******************************************'''
'''*********************************MOST IMPORTANT******************************************'''
'''*********************************MOST IMPORTANT******************************************'''
'''*********************************MOST IMPORTANT******************************************'''
'''*********************************MOST IMPORTANT******************************************'''
'''*********************************MOST IMPORTANT******************************************'''
'''*********************************MOST IMPORTANT******************************************'''
'''*********************************MOST IMPORTANT******************************************'''
'''*********************************MOST IMPORTANT******************************************'''
'''*********************************MOST IMPORTANT******************************************'''
'''*********************************MOST IMPORTANT******************************************'''
'''*********************************MOST IMPORTANT******************************************'''
'''*********************************MOST IMPORTANT******************************************'''
'''*********************************MOST IMPORTANT******************************************'''
def update_customer_email(username,emailaddress):
	response=checkusername(emailaddress)
	if response!=1:
		c,conn=dbconnect()
		sql="""UPDATE customers SET username=%s WHERE username=%s """
		value=(emailaddress,username)
		c.execute(sql,value)

		sql="""UPDATE orderinfotable SET username=%s WHERE username=%s """
		value=(emailaddress,username)
		c.execute(sql,value)

		sql="""UPDATE cancelordertable SET username=%s WHERE username=%s """
		value=(emailaddress,username)
		c.execute(sql,value)

		sql="""UPDATE completeordertable SET username=%s WHERE username=%s """
		value=(emailaddress,username)
		c.execute(sql,value)

		sql="""UPDATE watchlist SET username=%s WHERE username=%s """
		value=(emailaddress,username)
		c.execute(sql,value)
		conn.commit()
		c.close()
		conn.close()
		return 	"success"
	else:
		return response
'''*********************************MOST IMPORTANT******************************************'''
'''*********************************MOST IMPORTANT******************************************'''
'''*********************************MOST IMPORTANT******************************************'''
'''*********************************MOST IMPORTANT******************************************'''
'''*********************************MOST IMPORTANT******************************************'''
'''*********************************MOST IMPORTANT******************************************'''
'''*********************************MOST IMPORTANT******************************************'''
'''*********************************MOST IMPORTANT******************************************'''
'''*********************************MOST IMPORTANT******************************************'''
'''*********************************MOST IMPORTANT******************************************'''
'''*********************************MOST IMPORTANT******************************************'''
'''*********************************MOST IMPORTANT******************************************'''
'''*********************************MOST IMPORTANT******************************************'''
'''*********************************MOST IMPORTANT******************************************'''
'''*********************************MOST IMPORTANT******************************************'''
'''*********************************MOST IMPORTANT******************************************'''
'''*********************************MOST IMPORTANT******************************************'''
'''*********************************MOST IMPORTANT******************************************'''
'''*********************************MOST IMPORTANT******************************************'''
'''*********************************MOST IMPORTANT******************************************'''
'''*********************************MOST IMPORTANT******************************************'''
'''*********************************MOST IMPORTANT******************************************'''
'''*********************************MOST IMPORTANT******************************************'''
'''*********************************MOST IMPORTANT******************************************'''
'''*********************************MOST IMPORTANT******************************************'''
'''*********************************MOST IMPORTANT******************************************'''
'''*********************************MOST IMPORTANT******************************************'''
'''*********************************MOST IMPORTANT******************************************'''
'''*********************************MOST IMPORTANT******************************************'''
'''*********************************MOST IMPORTANT******************************************'''
'''***********************************NAVBAR PART*************************************'''
#username i.e customer name for showing 'hi customer' 
def get_cn(username):
	c,conn=dbconnect()
	sql="SELECT CustomerId FROM customers where username =%s "
	value=(username,)
	c.execute(sql,value)
	data=c.fetchone()
	#print(data)
	conn.commit()
	c.close()
	conn.close()
	return 	data

def add_into_watchlist(CustomerId,productId):
	c,conn=dbconnect()
	# Condition for limit Reached
	sql1='''SELECT count(username) from watchlist where username=%s'''
	value=(CustomerId,)
	c.execute(sql1,value)
	data=c.fetchone()
	#print(data)
	if data[0] > 4:
		print("Limit Reached")
		conn.commit()
		c.close()
		conn.close()
		return '3'

	#condition for avoiding Duplication or product in individual customer
	sql1='''SELECT * from watchlist where username=%s and ProductId=%s'''
	value=(CustomerId,productId)
	c.execute(sql1,value)
	if c.rowcount > 0:
		print("Already Present")
		conn.commit()
		c.close()
		conn.close()
		return '2'


	sql="INSERT INTO watchlist (username,ProductId)  VALUES (%s,%s)"
	value=(CustomerId,productId,)
	c.execute(sql,value)
	conn.commit()
	c.close()
	conn.close()
	return '1'
'''********************************PRODUCT PAGE PARTS***********************************************'''
def ProductDetails1(pid):
	c,conn=dbconnect()
	sql="""SELECT * FROM lights where ProductId=%s"""
	value=(pid,)
	c.execute(sql,value)
	data=c.fetchone()
	#print(data)
	conn.commit()
	c.close()
	conn.close()
	return 	data 


'''********************************WATCH LIST PART*********************************************'''
def watchlist(username):
	
	c,conn=dbconnect()
	
	sql='''SELECT lights.id,lights.ProductId,lights.ProductName, lights.ProductType,lights.ProductWarranty,
	lights.ProductDescription,lights.ProductPrice,lights.ProductImageAddress,lights.ProductImageAddress1,
	lights.ProductType1,lights.ProductBrand,lights.Discount,lights.DiscountPrice
	 FROM watchlist  INNER JOIN lights
	  ON watchlist.ProductId=lights.ProductId
	   and watchlist.username=%s '''

	value=(username,)
	c.execute(sql,value)
	data=c.fetchall()
	#print(data)
	conn.commit()
	c.close()
	conn.close()
	return data


def delete_watchlist(username):
	c,conn=dbconnect()
	sql='''DELETE FROM watchlist where username=%s'''
	value=(username,)
	c.execute(sql,value)
	conn.commit()
	c.close()
	conn.close()
	return "1"


'''*********************************Customer Product Filter Related work*******************************************'''
def customerfilter_product_list(data):
	print("jbsifjbjb \nsdnfknoskdnknsdksndn\nskdjbfijbdjbfjsbdfkjbj\nsjbdfjbjsdfbkjsdb\naifisdifidfivfj\nakjbfibdfidi")
	sql="SELECT * FROM lights WHERE"
	ptype_checkbox=data['ptype']
	pbrand_checkbox=data['pbrand']
	pproduct_checkbox=data['pproduct']
	pprice_checkbox=data['pprice']
	pwarranty_checkbox =data['pwarranty']
	print(pwarranty_checkbox)
	sql1="SELECT * FROM lights"

	if ptype_checkbox =="All":
		sql=sql +"  1 "
	else:
		sql = sql+' ProductType= "'+ptype_checkbox+'"';


	if (len(pbrand_checkbox) ==1 and pbrand_checkbox[0] == "All") or len(pbrand_checkbox)==0:
		sql=sql + ' AND 1 '
	else:
		sql=sql+ ' AND ('
		for i in range(0,len(pbrand_checkbox)):
			if i== len(pbrand_checkbox)-1:
				break;
			sql = sql+' ProductBrand="'+pbrand_checkbox[i]+'"  OR';
		sql = sql+' ProductBrand="'+pbrand_checkbox[i]+'")';



	if (len(pproduct_checkbox) ==1 and pproduct_checkbox[0] == "All") or len(pproduct_checkbox)==0:
		sql=sql + " AND 1 "
	else:
		sql=sql+ ' AND ('
		for i in range(0,len(pproduct_checkbox)):
			if i == len(pproduct_checkbox)-1:
				break;
			sql = sql+' ProductType1="'+pproduct_checkbox[i]+'" OR';
		sql = sql+' ProductType1="'+pproduct_checkbox[i]+'")';


	if pprice_checkbox[0] == "All" and len(pprice_checkbox) ==1:
		sql=sql +" AND 1 "
	else:
		sql = sql+" AND ProductPrice Between "+pprice_checkbox[0]+" AND " +pprice_checkbox[1]



	if pwarranty_checkbox =="All":
		sql=sql +" AND  1 "
	elif pwarranty_checkbox == "0":
		sql = sql+' AND ProductWarranty=1';
	else:
		sql=sql+' AND ProductWarranty <> 1';


	print(sql)


	c,conn=dbconnect()
	c.execute(sql)
	data=c.fetchall()
	#print(data)
	conn.commit()
	c.close()
	conn.close()
	return 	data

'''**************************************************************************'''

def upload_new_product(ProductId,ProductName,ProductType,ProductWarranty,ProductSpecification,ProductPrice,ProductImageAddress,ProductImageAddress1,ProductType1,ProductBrand,DiscountPrice):
	expression=100-((int(DiscountPrice)/int(ProductPrice))*100)
	DiscountRate=round(expression,2)
	sql1="SELECT ProductId FROM lights WHERE ProductId=%s "
	val1=(ProductId,)
	c,conn=dbconnect()
	c.execute(sql1,val1)
	if c.rowcount >0:
		return 'Product Already Present'

	sql="""INSERT INTO lights 
	(ProductId,ProductName, ProductType,ProductWarranty,
	ProductDescription,ProductPrice,ProductImageAddress,ProductImageAddress1,
	ProductType1,ProductBrand,Discount,DiscountPrice)
	  VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

	value=(ProductId,ProductName,ProductType,ProductWarranty,
		ProductSpecification,ProductPrice,ProductImageAddress,
		ProductImageAddress1,ProductType1,ProductBrand,DiscountRate,DiscountPrice)
	
	c.execute(sql,value)
	conn.commit()
	c.close()
	conn.close()
	return 'success'

def getoverall_product_list(sql):
	#sql="SELECT * FROM lights"

	c,conn=dbconnect()
	c.execute(sql)
	data=c.fetchall()
	#print(data)
	conn.commit()
	c.close()
	conn.close()
	return 	data

'''**********************************ORDER PLACED DB WORK*******************************************'''
def OrderPlaceDbWork(username,OrderID,cart):
	t=datetime.datetime.now()
	OrderID="VLH"+OrderID
	c,conn=dbconnect()
	sql = """INSERT INTO orderinfotable (username,OrderID,OrderConf,order_date) VALUES (%s,%s,%s,%s)"""
	value=(username,OrderID,"-",t)
	c.execute(sql,value)
	conn.commit()
	c.close()
	conn.close()


	c,conn=dbconnect()
	sql1='''INSERT INTO orderedproduct (OrderID,ProductId,pcount,ProductName,ProductSpecification,ProductImage,ProductPrice,Discount,DiscountPrice) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
	for productId ,value in cart.items():
		if productId !='tp':
			value1=(OrderID,productId,value['Count'],value['ProductName']
				,value['ProductSpecification'],value['ProductImageAddress'],value['ProductPrice'],value['DiscountRate'],value['DiscountPrice'])
			c.execute(sql1,value1)

	conn.commit()
	c.close()
	conn.close()
	return 1
'''**********************************Customer ORDERS LIST********************************************'''
def customer_orders(username):
	c,conn=dbconnect()
	sql="SELECT * FROM orderinfotable where username = %s "
	value=(username,)
	c.execute(sql,value)
	data=c.fetchall()
	print(data)
	conn.commit()
	c.close()
	conn.close()
	return 	data
'''*********************************CUSTOMER COMPLTED ORDER LIST****************************************'''
def customer_Completed_order(username):
	c,conn=dbconnect()
	sql="SELECT * FROM completeordertable where username =%s "
	value=(username,)
	c.execute(sql,value)
	data=c.fetchall()
	print(data)
	conn.commit()
	c.close()
	conn.close()
	return 	data

def Individual_order_details(OrderID):
	c,conn=dbconnect()
	sql ='''SELECT * from orderedproduct where OrderID=%s'''
	value=(OrderID,)
	c.execute(sql,value)
	data=c.fetchall()
	conn.commit()
	c.close()
	conn.close()
	main_list=[]
	
	for product in data: 
		main_list.append({'OrderID':product[1],"ProductId":product[2],'ProductName':product[4],
				"pcount":product[3],'ProductSpecification':product[5],
				'ProductPrice':product[7],'ProductImageAddress':product[6]
				,'DiscountRate':product[8],'DiscountPrice':product[9]})
	return main_list

	
def ucancel_order(username,OrderID):
	c,conn=dbconnect()
	# fecthing the values of deleted Order
	sql2="""SELECT * FROM orderinfotable where OrderID=%s"""
	value2=(OrderID,)
	c.execute(sql2,value2)
	info=c.fetchone()
	confirmation_time=info[8]
	print("HEKKOOO",confirmation_time)

	current_time=datetime.datetime.now()
	if confirmation_time == None:
		confirmation_time="None"
		dt=" -- "
	else:
		dt=str(current_time-confirmation_time)


	# Inserting Into Cancelordertable
	sql3='''INSERT INTO cancelordertable (username,OrderID,status,cancelby,cancel_date,confirmation_time,time_difference)
	 VALUES(%s,%s,%s,%s,%s,%s,%s)'''
	value3=(username,OrderID,info[3],"Cancel By Customer",current_time,confirmation_time,dt)
	c.execute(sql3,value3)




	# Deleting the Order from both table orderinfotable & orderedproduct table
	sql = '''DELETE FROM orderinfotable WHERE OrderID=%s'''
	value=(OrderID,)
	#sql1 = '''DELETE FROM orderedproduct WHERE OrderID=%s'''
	c.execute(sql,value)
	#c.execute(sql1,value)
	conn.commit()
	c.close()
	conn.close()
	return 1

'''**********************************CUSTOMIZE PRODUCT LIST*****************************************'''
def Send_Constomize_Infromation(customername,email,phone_number,ProductType,Description,ImageAddress):
	c,conn=dbconnect()
	t=datetime.datetime.now()
	sql='''INSERT INTO customizeordertable
	(customername,email,phone_number,ProductType,Description,ImageAddress,status,request_date)
	VALUES (%s,%s,%s,%s,%s,%s,%s,%s)'''
	value=(customername,email,phone_number,ProductType,Description,ImageAddress,"Reply Pending",t)
	c.execute(sql,value)
	conn.commit()
	c.close()
	conn.close()
	return "success"



'''**************************************ADMIN DB PART*****
**************************************************************
************************************************************
****************************************************************
****************************************************************
******************************************************************
*********************************************************************
***********************************************************************
***********************************************************************
**************************************************************************
*************************************************************************
***********************************************************************
***********************************************************************
*************************************************************************
***********************************************************************
*********************************************************************
**********************************************************************
********************************'''
def InsertPartner(EnterpriseName,OwnerName,Contact1,Contact2,Contact3,Address):
	c,conn=dbconnect()
	sql="""INSERT INTO AssociatePartner (EnterpriseName,OwnerName,Contact1,Contact2,Contact3,Address)
	VALUES (%s,%s,%s,%s,%s,%s)"""
	value=(EnterpriseName,OwnerName,Contact1,Contact2,Contact3,Address)
	c.execute(sql,value)
	conn.commit()
	c.close()
	conn.close()
	return 'success'

def LoadPartners():
	c,conn=dbconnect()
	sql="""SELECT * FROM AssociatePartner"""
	c.execute(sql)
	data=c.fetchall()
	#print(data)
	conn.commit()
	c.close()
	conn.close()
	return 	data

def LoadIndividualPartners(x):
	c,conn=dbconnect()
	sql="""SELECT * FROM AssociatePartner where id=%s"""
	value=(x,)
	c.execute(sql,value)
	data=c.fetchone()
	#print(data)
	conn.commit()
	c.close()
	conn.close()
	return 	data

def RemovePartner(pid):
	c,conn=dbconnect()
	sql="""DELETE FROM AssociatePartner where id=%s"""
	value=(pid,)
	c.execute(sql,value)
	conn.commit()
	c.close()
	conn.close()
	return '1'

def LoadProduct(option,option1):
	sql="SELECT * FROM lights WHERE"

	if option =="All":
		sql=sql +"  1 "
	else:
		sql = sql+' ProductType= "'+option+'"';

	if option1 =="All":
		sql=sql +" AND  1 "
	else:
		sql = sql+' AND ProductType1= "'+option1+'"';

	print(sql)
	c,conn=dbconnect()
	c.execute(sql)
	
	data=c.fetchall()
	#print(data)
	conn.commit()
	c.close()
	conn.close()
	return 	data



def RemoveProduct(pid):
	c,conn=dbconnect()
	sql="""DELETE FROM lights where id=%s"""
	value=(pid,)
	c.execute(sql,value)
	conn.commit()
	c.close()
	conn.close()
	return '1'

def ProductDetails(pid):
	c,conn=dbconnect()
	sql="""SELECT * FROM lights where id=%s"""
	value=(pid,)
	c.execute(sql,value)
	data=c.fetchone()
	#print(data)
	conn.commit()
	c.close()
	conn.close()
	return 	data

def update_product_price(pid,ProductPrice,DiscountPrice):
	expression=100-((int(DiscountPrice)/int(ProductPrice))*100)
	DiscountRate=round(expression,2)
	c,conn=dbconnect()
	sql='''UPDATE lights SET ProductPrice=%s , DiscountPrice=%s , Discount=%s  WHERE id=%s '''
	value=(ProductPrice,DiscountPrice,DiscountRate,pid)
	c.execute(sql,value)
	conn.commit()
	c.close()
	conn.close()
	return 'success'

def update_product_name(pid,ProductName):
	#print(ProductName)
	c,conn=dbconnect()
	sql='''UPDATE lights SET ProductName=%s WHERE id=%s '''
	value=(ProductName,pid)
	c.execute(sql,value)
	conn.commit()
	c.close()
	conn.close()
	return 'success'
#update_product_name(2,"philips868")

def update_product_type(pid,ProductType):
	c,conn=dbconnect()
	sql='''UPDATE lights SET ProductType=%s WHERE id=%s '''
	value=(ProductType,pid)
	c.execute(sql,value)
	conn.commit()
	c.close()
	conn.close()
	return 'success'

def update_product_type1(pid,ProductType1):
	c,conn=dbconnect()
	sql='''UPDATE lights SET ProductType1=%s WHERE id=%s '''
	value=(ProductType1,pid)
	c.execute(sql,value)
	conn.commit()
	c.close()
	conn.close()
	return 'success'


def update_product_brand(pid,ProductBrand):
	c,conn=dbconnect()
	sql='''UPDATE lights SET ProductBrand=%s WHERE id=%s '''
	value=(ProductBrand,pid)
	c.execute(sql,value)
	conn.commit()
	c.close()
	conn.close()
	return 'success'

def update_product_warranty(pid,ProductWarranty):
	c,conn=dbconnect()
	sql='''UPDATE lights SET ProductWarranty=%s WHERE id=%s '''
	value=(ProductWarranty,pid)
	c.execute(sql,value)
	conn.commit()
	c.close()
	conn.close()
	return 'success'

def update_product_description(pid,ProductDescription):
	c,conn=dbconnect()
	sql='''UPDATE lights SET ProductDescription=%s WHERE id=%s '''
	value=(ProductDescription,pid)
	c.execute(sql,value)
	conn.commit()
	c.close()
	conn.close()
	return 'success'

def update_product_image1(pid,ProductImageAddress):
	c,conn=dbconnect()
	sql='''UPDATE lights SET ProductImageAddress=%s WHERE id=%s '''
	value=(ProductImageAddress,pid)
	c.execute(sql,value)
	conn.commit()
	c.close()
	conn.close()
	return 'success'

def update_product_image2(pid,ProductImageAddress1):
	c,conn=dbconnect()
	sql='''UPDATE lights SET ProductImageAddress1=%s WHERE id=%s '''
	value=(ProductImageAddress1,pid)
	c.execute(sql,value)
	conn.commit()
	c.close()
	conn.close()
	return 'success'

'''********************************* Admin Order Work*************************************'''

def admin_customer_orders():
	c,conn=dbconnect()
	sql="SELECT * FROM orderinfotable"
	c.execute(sql)
	data=c.fetchall()
	#print(data)
	conn.commit()
	c.close()
	conn.close()
	return 	data

def aIndividual_order_details(OrderID):

	c,conn=dbconnect()
	sql ='''SELECT * from orderedproduct where OrderID=%s'''
	value=(OrderID,)
	c.execute(sql,value)
	data=c.fetchall()

	sql ='''SELECT username from orderinfotable where OrderID=%s'''
	value=(OrderID,)
	c.execute(sql,value)
	username=c.fetchone()

	sql ='''SELECT * from customers where username=%s'''
	value=(username[0],)
	c.execute(sql,value)
	personal_info=c.fetchone()
	#print(personal_info)

	conn.commit()
	c.close()
	conn.close()
	
	#personal Info
	address=personal_info[5].split('@');
	personal_info={"CustomerName":personal_info[1],"username":personal_info[2],
	"PhoneNumber":personal_info[4],"add1":address[0],"add2":address[1],"add3":address[2]
	,"add4":address[3],"add5":address[4]}

	# orderlist
	main_list=[]
	for product in data: 
		main_list.append({'OrderID':product[1],"ProductId":product[2],'ProductName':product[4],
				"pcount":product[3],'ProductSpecification':product[5],
				'ProductPrice':product[7],'ProductImageAddress':product[6],
				'DiscountRate':product[8],'DiscountPrice':product[9]
				})

	return main_list,personal_info

def aIndividual_order_details_completed(OrderID):

	c,conn=dbconnect()
	sql ='''SELECT * from orderedproduct where OrderID=%s'''
	value=(OrderID,)
	c.execute(sql,value)
	data=c.fetchall()

	sql ='''SELECT username from completeordertable where OrderID=%s'''
	value=(OrderID,)
	c.execute(sql,value)
	username=c.fetchone()

	sql ='''SELECT * from customers where username=%s'''
	value=(username[0],)
	c.execute(sql,value)
	personal_info=c.fetchone()
	#print(personal_info)

	conn.commit()
	c.close()
	conn.close()
	
	#personal Info
	address=personal_info[5].split('@');
	personal_info={"CustomerName":personal_info[1],"username":personal_info[2],
	"PhoneNumber":personal_info[4],"add1":address[0],"add2":address[1],"add3":address[2]
	,"add4":address[3],"add5":address[4]}

	# orderlist
	main_list=[]
	for product in data: 
		main_list.append({'OrderID':product[1],"ProductId":product[2],'ProductName':product[4],
				"pcount":product[3],'ProductSpecification':product[5],
				'ProductPrice':product[7],'ProductImageAddress':product[6],
				'DiscountRate':product[8],'DiscountPrice':product[9]
				})

	return main_list,personal_info

def aIndividual_order_details_canceled(OrderID):

	c,conn=dbconnect()
	sql ='''SELECT * from orderedproduct where OrderID=%s'''
	value=(OrderID,)
	c.execute(sql,value)
	data=c.fetchall()

	sql ='''SELECT username from cancelordertable where OrderID=%s'''
	value=(OrderID,)
	c.execute(sql,value)
	username=c.fetchone()

	sql ='''SELECT * from customers where username=%s'''
	value=(username[0],)
	c.execute(sql,value)
	personal_info=c.fetchone()
	#print(personal_info)

	conn.commit()
	c.close()
	conn.close()
	
	#personal Info
	address=personal_info[5].split('@');
	personal_info={"CustomerName":personal_info[1],"username":personal_info[2],
	"PhoneNumber":personal_info[4],"add1":address[0],"add2":address[1],"add3":address[2]
	,"add4":address[3],"add5":address[4]}

	# orderlist
	main_list=[]
	for product in data: 
		main_list.append({'OrderID':product[1],"ProductId":product[2],'ProductName':product[4],
				"pcount":product[3],'ProductSpecification':product[5],
				'ProductPrice':product[7],'ProductImageAddress':product[6],
				'DiscountRate':product[8],'DiscountPrice':product[9]
				})

	return main_list,personal_info

def update_customer_order_status(orderid,status):
	t=datetime.datetime.now()
	c,conn=dbconnect()
	sql2 ='''SELECT * FROM orderinfotable WHERE OrderID=%s'''
	value2=(orderid,)
	c.execute(sql2,value2)
	data=c.fetchone()
	customer_email=data[1]
	if status == "OrderConfirmed":
		sql='''UPDATE orderinfotable SET OrderConf=%s ,OrderConfirmationTime=%s WHERE OrderID=%s'''
		value=(status,t,orderid)
		c.execute(sql,value)
	else:
		sql='''UPDATE orderinfotable SET OrderConf=%s WHERE OrderID=%s'''
		value=(status,orderid)
		c.execute(sql,value)
	conn.commit()
	c.close()
	conn.close()
	return 1,customer_email


def admin_cancel_order(username,OrderID):
	c,conn=dbconnect()

	# fecthing the values of deleted Order
	sql2="""SELECT * FROM orderinfotable where OrderID=%s"""
	value2=(OrderID,)
	c.execute(sql2,value2)
	info=c.fetchone()
	t=datetime.datetime.now()
	# Inserting Into Cancelordertable
	sql3='''INSERT INTO cancelordertable (username,OrderID,status,cancelby,cancel_date,confirmation_time)
	 VALUES(%s,%s,%s,%s,%s,%s)'''
	value3=(username,OrderID,info[3],"Cancel By Lighthub",t,info[8])
	c.execute(sql3,value3)




	# Deleting the Order from both table orderinfotable & orderedproduct table
	sql = '''DELETE FROM orderinfotable WHERE OrderID=%s'''
	value=(OrderID,)
	#sql1 = '''DELETE FROM orderedproduct WHERE OrderID=%s'''
	c.execute(sql,value)
	#c.execute(sql1,value)
	conn.commit()
	c.close()
	conn.close()
	return 1


def OrderFullfilled(orderid):
	c,conn=dbconnect()
	#FETCHING INFOMATION FROM ORDER INFO TABLE
	sql="""SELECT * from orderinfotable where OrderID=%s """
	value=(orderid,)
	c.execute(sql,value)
	data=c.fetchone()
	username=data[1]
	OrderID=data[2]
	status="Completed"
	order_date=data[7]
	order_confirmation_time=data[8]
	print(order_confirmation_time)
	delivery_date=datetime.datetime.now()
	#INSERTING TO COMPLETE OREDER DATABASE
	sql='''INSERT INTO completeordertable (username,OrderID,status,order_date,delivery_date,confirmation_time)
	VALUES(%s,%s,%s,%s,%s,%s)'''
	value=(username,OrderID,status,order_date,delivery_date,order_confirmation_time)
	c.execute(sql,value)

	# DELETING COMPLETED ORDER FROM ORDER INFO TABLE
	sql='''DELETE FROM orderinfotable WHERE OrderID=%s'''
	value=(orderid,)
	c.execute(sql,value)


	conn.commit()
	c.close()
	conn.close()
	return 1
'''******************************ORDER CANCEL PAGE DB WORK********************************************'''
def cancel_order_page():
	c,conn=dbconnect()
	sql='''SELECT * FROM cancelordertable'''
	c.execute(sql)
	data=c.fetchall()
	conn.commit()
	c.close()
	conn.close()
	return data

'''******************************ORDER COMPLTED PAGE DB WORK********************************************'''
def admin_completed_order():
	c,conn=dbconnect()
	sql='''SELECT * FROM completeordertable'''
	c.execute(sql)
	data=c.fetchall()
	conn.commit()
	c.close()
	conn.close()
	return data
'''********************************ADMIN HOME PAGE COUNTER DATA**************************************'''
def get_counter_data():
	c,conn=dbconnect()

	sql='''SELECT * FROM orderinfotable WHERE OrderConf="-" '''
	c.execute(sql)
	NewOrder=c.rowcount

	sql='''SELECT * FROM orderinfotable  '''
	c.execute(sql)
	PendingOrder=c.rowcount

	sql='''SELECT * FROM completeordertable  '''
	c.execute(sql)
	CompletedOrder=c.rowcount

	sql='''SELECT * FROM cancelordertable '''
	c.execute(sql)
	CancelOrder=c.rowcount

	sql='''SELECT * FROM customizeordertable '''
	c.execute(sql)
	CustomizeQuery=c.rowcount

	conn.commit()
	c.close()
	conn.close()
	dictionary={'PendingOrder':PendingOrder,'CompletedOrder':CompletedOrder,'CancelOrder':CancelOrder,'NewOrder':NewOrder,'CustomizeQuery':CustomizeQuery}
	return dictionary

'''******************************** ADMIN CUSTOMIZE ORDER REQUEST PAGE****************************************'''
def a_customizeorder():
	c,conn=dbconnect()
	sql='''SELECT * FROM customizeordertable'''
	c.execute(sql)
	data=c.fetchall()
	conn.commit()
	c.close()
	conn.close()
	return data

def delete_customized_product_query(deleteorder):
	sql='''DELETE FROM customizeordertable WHERE id=%s'''
	value=(deleteorder,)
	c,conn=dbconnect()
	c.execute(sql,value)
	conn.commit()
	c.close()
	conn.close()
	return 1
def fetctIndividualCustomizedquery(queryid):
	sql = '''SELECT * FROM customizeordertable where id=%s'''
	value=(queryid,)
	c,conn=dbconnect()
	c.execute(sql,value)
	data=c.fetchone()
	conn.commit()
	c.close()
	conn.close()
	return data

def reply_done(queryid):
	sql = '''UPDATE customizeordertable SET status="Reply Done" WHERE id=%s '''
	value=(queryid,)
	c,conn=dbconnect()
	c.execute(sql,value)
	conn.commit()
	c.close()
	conn.close()
	return 1




def bill_genaration(OrderID):
	result={}
	found=0
	c,conn = dbconnect()

	sql='''SELECT * FROM orderinfotable Where OrderID=%s'''
	value=(OrderID,)
	c.execute(sql,value)
	if c.rowcount == 1:
		found=2

	sql='''SELECT * FROM completeordertable Where OrderID=%s'''
	value=(OrderID,)
	c.execute(sql,value)
	if c.rowcount == 1:
		found=3

	sql='''SELECT * FROM cancelordertable Where OrderID=%s'''
	value=(OrderID,)
	c.execute(sql,value)
	if c.rowcount == 1:
		found=4

	if found==0:
		return "Not Found"

	if found ==2:
		sql='''SELECT * FROM orderinfotable Where OrderID=%s'''
		value=(OrderID,)
		c.execute(sql,value)
		data=c.fetchone()
		result['type']="Pending"
		result['OrderInfo']={
		'OrderID':data[2],'OrderStatus':data[3],'OrderDate':data[7],
		'ConfirmationTime':data[8]
		}

	if found ==3:
		sql='''SELECT * FROM completeordertable Where OrderID=%s'''
		value=(OrderID,)
		c.execute(sql,value)
		data=c.fetchone()
		result['type']="Completed"
		result['OrderInfo']={
		'OrderID':data[2],'OrderStatus':data[3],'OrderDate':data[4],
		'DeliverDate':data[5],'ConfirmationTime':data[6]
		}

	if found ==4:
		sql='''SELECT * FROM cancelordertable Where OrderID=%s'''
		value=(OrderID,)
		c.execute(sql,value)
		data=c.fetchone()
		result['type']="Cancel"
		result['OrderInfo']={
		'OrderID':data[2],'OrderStatus':data[3],'CancelBy':data[4],
		'CancelDate':data[5],'ConfirmationTime':data[6],'time_difference':int(data[7][0])
		}


	#print(data)
	username=data[1]
	sql='''SELECT * FROM customers where username=%s'''
	value=(username,)
	c.execute(sql,value)
	customer_info=c.fetchone();
	#print(customer_info)

	result['customer_info']={"cname":customer_info[1],'email':customer_info[2],'phone_number':customer_info[4],
	'address':customer_info[5]}

	sql='''SELECT * FROM orderedproduct Where OrderID=%s'''
	value=(OrderID,)
	c.execute(sql,value)
	products=c.fetchall()
	c_products=[]
	total=0
	for product in products:
		c_products.append({
			'ProductId':product[2],'pcount':product[3],'ProductName':product[4],
			'ProductSpecification':product[5],'ProductPrice':product[7],'Discount':product[8],
			'DiscountPrice':product[9],
			})
		total=total+(product[3]*product[9])
	result['Orders']=c_products
	result['TotalPrice']=total
	return result


