import mysql.connector

mydb = mysql.connector.connect(host="10.0.41.8", user= "nutzer14",password="Eftg8xdx",database="Datenbank14")
mycursor = mydb.cursor()

anzahlFragen = input("Wie viele Fragen willst du bekommen?")

for i in range(1, anzahlFragen):
  fragenNr = randi()
  match 
sql = "SELECT Name FROM land"
mycursor.execute(sql)
result = mycursor.fetchall()
print(result)
