import mysql.connector
import random

mydb = mysql.connector.connect(host="10.0.41.8", user= "nutzer14",password="Eftg8xdx",database="Datenbank14")
mycursor = mydb.cursor()

anzahlFragen = input("Wie viele Fragen willst du bekommen?")
score = 0
scoreMax = 0

for i in range(1, anzahlFragen):
  questionType = random.randint(0, 3)
  
func 
  match questionType:
    case 0:
      sql = "SELECT ort.Name, land.Name FROM ort INNER JOIN land ON ort.ONR = land.StadtONR"
      mycursor.execute(sql)
      fetchResult = mycursor.fetchall()
      questionNr = random.randint(0, len(fetchResult)-1)
      
 
sql = "SELECT Name FROM land"
mycursor.execute(sql)
result = mycursor.fetchall()
print(result)
