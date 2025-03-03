import mysql.connector
import random

mydb = mysql.connector.connect(host="localhost", user= "eggbert",password="EggbertHatUser",database="testdb")
mycursor = mydb.cursor()

anzahlFragen = input("Wie viele Fragen willst du bekommen?")
score = 0
scoreMax = 0


def is_similar(userInput:str, answer:str):
  userInput = userInput.lower().replace('oe', 'ö').replace('ae', 'ä').replace('ue', 'ü')
  answer = answer.lower().replace('oe', 'ö').replace('ae', 'ä').replace('ue', 'ü')
  if userInput == answer: #redundant?
    return True
  correctChars = 0
  wrongChars = 0
  for i in range(min(len(userInput),len(answer))):
    if userInput[i] == answer[i]:
      correctChars += 1
    else:
      wrongChars += 1
  if wrongChars <= 2 or (correctChars+wrongChars)/wrongChars <= 0.2:
    return True
  else:
    return False

def ask_question(questionType):
  match questionType:
    case 0:
      sql = "SELECT ort.Name, land.Name FROM ort INNER JOIN land ON ort.ONR = land.HauptONR"
      mycursor.execute(sql)
      fetchResult = mycursor.fetchall()
      questionNr = random.randint(0, len(fetchResult)-1)
      return is_similar(input(f"Von welchem Land ist {fetchResult[questionNr][0]} die Hauptstadt?\n"), fetchResult[questionNr][1])
    case 1:
      sql = "SELECT fluss.Name, fluss.Meer FROM fluss WHERE fluss.Meer IS NOT NULL"
      mycursor.execute(sql)
      fetchResult = mycursor.fetchall()
      questionNr = random.randint(0, len(fetchResult)-1)
      return is_similar(input(f"In welchem Meer mündet der Fluss {fetchResult[questionNr][0]}?\n"), fetchResult[questionNr][1])

for i in range(0, int(anzahlFragen)):
  questionType = random.randint(0, 1)
  if ask_question(questionType):
    score += 1
  scoreMax += 1
  print(f"{score}/{scoreMax} correct")