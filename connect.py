import mysql.connector





def connect():
	con = mysql.connector.connect(
		host='83.220.174.62',
		user='meo',
		password='yR2gE0xW5faM',
		database='sender')
	cursor = con.cursor(buffered=True)
	return con, cursor
