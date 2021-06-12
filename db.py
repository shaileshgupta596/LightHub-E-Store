import mysql.connector

def dbconnect():
	conn= mysql.connector.connect(host="localhost",user="Lighthub",passwd="Lighthub",
	  database="lightproject")

	c= conn.cursor(buffered=True)
	#c.execute("CREATE TABLE customers (id INT AUTO_INCREMENT PRIMARY KEY,username VARCHAR(255), password VARCHAR(255))")
	return c,conn 
