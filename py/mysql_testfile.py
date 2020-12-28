import mysql.connector
mydb = mysql.connector.connect(
  host="localhost",
  user="stock_scraper",
  password="quinnkump1",
  database="py_stock_scraper"
)
mycursor = mydb.cursor()

#pulls up all the tickers
mycursor.execute("select ticker, COUNT(appearence) from stock_testing group by ticker")
results = mycursor.fetchall()
for x in results:
    print(x)
print("")
print("done with tickers")

#testing script to insert values
ticker = "NIO"
mycursor.execute("insert into stock_testing values (default, '" + ticker + "', now())")
mydb.commit()
print("added new stock")
