import mysql.connector

mydb = mysql.connector.connect(host="10.0.41.8", user= "nutzer14",password="Eftg8xdx",database="Datenbank14")
mycursor = mydb.cursor()

sql = "SELECT ort.Name, land.Name FROM ort INNER JOIN land ON ort.ONR = land.HauptONR WHERE land.KNR = 'EU'"
mycursor.execute(sql)

maxScore = 0
currentScore = 0
while 1:
    result = mycursor.fetchone()
    if input(f"In welchem Land liegt {result[0]}?") == result[1]:
        print("richtig")
        maxScore += 1
        currentScore += 1
    else:
        print("falsch")
        maxScore += 1
    print(f"Du hast {currentScore}/{maxScore} Fragen richtig beantwortet")
