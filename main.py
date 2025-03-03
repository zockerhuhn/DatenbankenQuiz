import mysql.connector
import random

mydb = mysql.connector.connect(host="localhost", user= "eggbert",password="EggbertHatUser",database="testdb")
#mydb = mysql.connector.connect(host="10.0.41.8", user= "nutzer14",password="Eftg8xdx",database="Datenbank14")
mycursor = mydb.cursor()

answLimitNormal = 4
answLimitHard = 2
sql = None
fetchResult = None
score = 0
scoreMax = 0
highscore = None


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
  if (wrongChars <= 2 and correctChars >= 3) or (correctChars+wrongChars)/wrongChars <= 0.2:
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
      if is_similar(input(f"Von welchem Land ist {fetchResult[questionNr][0]} die Hauptstadt?\n"), fetchResult[questionNr][1]):
        return True
      else:
        print(f"Inkorrekt, die Antwort war: {fetchResult[questionNr][1]}")
    case 1:
      sql = "SELECT sprache.Name, land.Name, gesprochen.Anteil FROM ((gesprochen INNER JOIN land ON gesprochen.LNR = land.LNR) INNER JOIN sprache ON gesprochen.SNR = sprache.SNR) WHERE gesprochen.Anteil IS NOT NULL AND gesprochen.Anteil > 50"
      mycursor.execute(sql)
      fetchResult = mycursor.fetchall()
      questionNr = random.randint(0, len(fetchResult)-1)
      if is_similar(input(f"Welche Sprache wird zu {fetchResult[questionNr][2]}% in {fetchResult[questionNr][1]} gesprochen?\n"), fetchResult[questionNr][0]):
        return True
      else:
        print(f"Inkorrekt, die Antwort war: {fetchResult[questionNr][0]}")
    case 2:
      sql = "SELECT fluss.Name, fluss.Meer FROM fluss WHERE fluss.Meer IS NOT NULL"
      mycursor.execute(sql)
      fetchResult = mycursor.fetchall()
      questionNr = random.randint(0, len(fetchResult)-1)
      if is_similar(input(f"In welchem Meer mündet der Fluss {fetchResult[questionNr][0]}?\n"), fetchResult[questionNr][1]):
        print("korrekt")
        return True
      else:
        print(f"Inkorrekt, die Antwort war: {fetchResult[questionNr][1]}")
    


if __name__ == "__main__":
  name = input("Was ist dein Name?\n")
  sql = "SELECT COUNT(*) FROM user WHERE user.Name = %s"
  val = [name]
  mycursor.execute(sql, val)
  fetchResult = mycursor.fetchone()
  if fetchResult[0] == 0:
    input(f"(Der Name {name} wurde bisher noch nicht benutzt, falls du nicht neu hier bist überprüfe die Rechtschreibung des Namens)(ENTER um fortzufahren)")
    sql = "INSERT INTO user (Name) VALUES (%s)"
    mycursor.execute(sql, val)
  else:
    sql = "SELECT user.Highscore_normal, user.Highscore_hard FROM user WHERE user.Name = %s"
    mycursor.execute(sql, val)
    fetchResult = mycursor.fetchone()
    sql = "SELECT COUNT(*) FROM user WHERE user.Highscore_normal >= %s"
    mycursor.execute(sql, [fetchResult[0]])
    placement_normal = mycursor.fetchone()[0]
    sql = "SELECT COUNT(*) FROM user WHERE user.Highscore_hard >= %s"
    mycursor.execute(sql, [fetchResult[1]])
    placement_hard = mycursor.fetchone()[0]
    print(f"Willkommen zurück {name}, dein highscore in normal ist {fetchResult[0]} (Top {placement_normal}), dein highscore in hard ist {fetchResult[1]} (Top {placement_hard})")
  userInput = input("Welchen modi möchtest du spielen? (training/normal/hard)")
  if userInput == "training":
    anzahlFragen = input("Wie viele Fragen willst du bekommen?\n")
    for i in range(0, int(anzahlFragen)):
      questionType = random.randint(0, 2)
      if ask_question(questionType):
        score += 1
      scoreMax += 1
      print(f"{score}/{scoreMax} korrekt")
      exit()
  elif userInput == "normal":
    print(f"starte normal, nach {answLimitNormal} falschen Antworten endet das Quiz")
    highscore = fetchResult[0]
    while scoreMax-score < answLimitNormal:
      questionType = random.randint(0, 1)
      if ask_question(questionType):
        score +=1
      scoreMax+=1
      print(f"{score} korrekt, {scoreMax-score} inkorrekt")
    if score > highscore:
      print(f"neuer highscore von {score}")
      sql = "UPDATE user SET Highscore_normal = %s WHERE user.name = %s"
      val = (score, name)
      mycursor.execute(sql, val)
  elif userInput == "hard":
    print(f"starte hard, nach {answLimitHard} falschen Antworten endet das Quiz")
    highscore = fetchResult[1]
    while scoreMax-score < answLimitHard:
      questionType = random.randint(2, 2)
      if ask_question(questionType):
        score +=1
      scoreMax+=1
      print(f"{score} korrekt, {scoreMax-score} inkorrekt")
    if score > highscore:
      print(f"neuer highscore von {score}")
      sql = "UPDATE user SET Highscore_hard = %s WHERE user.name = %s"
      val = (score, name)
      mycursor.execute(sql, val)
  mydb.commit()