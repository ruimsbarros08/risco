import pyodbc

# set up some constants
#MDB = '/Users/ruibarros/Desktop/datasources/gadm1_lev0.mdb'; DRV = '{Microsoft Access Driver (*.mdb)}'; PWD = 'pw'

# connect to db
con = pyodbc.connect('DRIVER={Microsoft Access Driver (*.mdb)};DBQ={/Users/ruibarros/Desktop/datasources/gadm1_lev0.mdb};')
cur = con.cursor()

# run a query and get the results 
SQL = 'SELECT *;' # your query goes here
rows = cur.execute(SQL).fetchall()
cur.close()
con.close()