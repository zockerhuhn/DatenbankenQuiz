import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
import random

inSchool = True #verbinden mit der Schuldatenbank statt eigener

root = tk.Tk()
root.title("login")
if inSchool:
    mydb = mysql.connector.connect(host="10.0.41.8", user= "nutzer14",password="Eftg8xdx",database="Datenbank14")
else:
    mydb = mysql.connector.connect(host="localhost", user= "eggbert",password="EggbertHatUser",database="datenbank14")
mycursor = mydb.cursor()

mode = None
answLimitNormal = 4
answLimitHard = 2
score = 0
scoreMax = 0
highscore = 0
valid = True
master = None

def reset():
    """Resets the Quiz for a retry
    """
    global score, scoreMax, highscore, master, root
    score = 0
    scoreMax = 0
    highscore = 0
    if master != None: #Quiz window schließen
        master.destroy()
        master = None
    if root != None: #Login window schließen falls es existiert damit es neu erstellt werden kann
        root.destroy()
        root = None
    root = tk.Tk()
    root.title("login")
    GUI()


class Question:
    question:str
    answers:list
    correctAnsw:int
    def __init__(self, hard:bool, questionType = -1):
        if questionType == -1: #um einfacher Fragen zu testen
            if hard: #type 2 trifft nur in hard auf
                questionType = random.randint(0, 2)
            else:
                questionType = random.randint(0, 1)
        self.answers = [None, None, None, None] #Die Antworten werden in einem Array gespeichert um einfacher nach doppelten Antworten zu prüfen
        self.correctAnsw = random.randint(0, 3)
        match questionType:
            case 0:
                sql = "SELECT ort.Name, land.Name FROM ort INNER JOIN land ON ort.ONR = land.HauptONR"
                mycursor.execute(sql)
                fetchResult = mycursor.fetchall()
                for i in range(len(self.answers)):
                    while True: #Verhindert dass keine doppelten Antwortmöglichkeiten auftreten
                        questionNr = random.randint(0, len(fetchResult)-1) #Eine zufällige Frage aus allen Fragen wählen
                        if fetchResult[questionNr][1] not in self.answers: break
                    self.answers[i] = fetchResult[questionNr][1]
                    if i == self.correctAnsw:
                        self.question = f"Von welchem Land ist {fetchResult[questionNr][0]} die Hauptstadt?"
            case 1:
                if hard: #Bei Modus hard werden statt Sprachen die über 50% gesprochen werden nur Sprachen die unter 50% gesprochen werden inkludiert
                    sql = "SELECT sprache.Name, land.Name, gesprochen.Anteil FROM ((gesprochen INNER JOIN land ON gesprochen.LNR = land.LNR) INNER JOIN sprache ON gesprochen.SNR = sprache.SNR) WHERE gesprochen.Anteil IS NOT NULL AND gesprochen.Anteil < 50"
                else:
                    sql = "SELECT sprache.Name, land.Name, gesprochen.Anteil FROM ((gesprochen INNER JOIN land ON gesprochen.LNR = land.LNR) INNER JOIN sprache ON gesprochen.SNR = sprache.SNR) WHERE gesprochen.Anteil IS NOT NULL AND gesprochen.Anteil > 50"
                mycursor.execute(sql)
                fetchResult = mycursor.fetchall()
                for i in range(len(self.answers)):
                    while True:
                        questionNr = random.randint(0, len(fetchResult)-1)
                        if fetchResult[questionNr][0] not in self.answers: break
                    self.answers[i] = fetchResult[questionNr][0]
                    if i == self.correctAnsw:
                        self.question = f"Welche Sprache wird zu {fetchResult[questionNr][2]}% in {fetchResult[questionNr][1]} gesprochen?\n"
            case 2:
                sql = "SELECT fluss.Name, fluss.Meer FROM fluss WHERE fluss.Meer IS NOT NULL"
                mycursor.execute(sql)
                fetchResult = mycursor.fetchall()
                for i in range(len(self.answers)):
                    while True:
                        questionNr = random.randint(0, len(fetchResult)-1)
                        if fetchResult[questionNr][1] not in self.answers: break
                    self.answers[i] = fetchResult[questionNr][1]
                    if i == self.correctAnsw:
                        self.question = f"In welchem Meer mündet der Fluss {fetchResult[questionNr][0]}?\n"

question:Question
def quiz(name):
### USER HANDLING ###
    global answLimitHard, answLimitNormal, score, scoreMax ,highscore, question, valid, mode, master, root
    sql = "SELECT COUNT(*) FROM user WHERE user.Name = %s"
    val = [name]
    mycursor.execute(sql, val)
    fetchResult = mycursor.fetchone()
    if fetchResult[0] == 0: #Nutzer nicht wiedererkannt
        waitForUser = messagebox.askokcancel(message=f"Der Name {name} wurde bisher noch nicht benutzt, falls du nicht neu hier bist überprüfe die Rechtschreibung des Namens")
        if not waitForUser: #Auf ok warten von Nutzer, sonst Programm neustarten und Nutzer nicht in Datenbank aufnehmen
            reset()
            exit() #Theoretisch endet das Programm immer per exit() allerdings falls etwas übersehen wurde wird nach neustart exited
        sql = "INSERT INTO user (Name) VALUES (%s)"
        mycursor.execute(sql, val)
        fetchResult = [0, 0]
    else: #Nutzer wiedererkannt
        sql = "SELECT user.Highscore_normal, user.Highscore_hard FROM user WHERE user.Name = %s"
        mycursor.execute(sql, val)
        fetchResult = mycursor.fetchone()
        sql = "SELECT COUNT(*) FROM user WHERE user.Highscore_normal >= %s"
        mycursor.execute(sql, [fetchResult[0]])
        placement_normal = mycursor.fetchone()[0]
        sql = "SELECT COUNT(*) FROM user WHERE user.Highscore_hard >= %s"
        mycursor.execute(sql, [fetchResult[1]])
        placement_hard = mycursor.fetchone()[0]
        messagebox.showinfo(message=f"Willkommen zurück {name}, dein highscore in normal ist {fetchResult[0]} (Top {placement_normal}), dein highscore in hard ist {fetchResult[1]} (Top {placement_hard})")
        if mode == "hard":
            highscore = fetchResult[1]
        elif mode == "normal":
            highscore = fetchResult[0]
### ANSWER PROCESSING ###
    def answer(index):
        """Handles answers by setting score and updating with a new question

        Args:
            index (int): which answer (0-3) was given
        """
        global score, scoreMax, mode, question, sql, val, mycursor
        if index == question.correctAnsw:
            score += 1
        scoreMax += 1
        resultLabel1.config(text=f"Die Antwort war {question.answers[question.correctAnsw]}")
        resultLabel2.config(text=f"Score: {score}, Leben: {answLimit-(scoreMax-score)}")
        if valid and scoreMax - score >= answLimit:
            printstr = f"Score: {score}"
            if score > highscore:
                printstr += ", neuer highscore"
                sql = f"UPDATE user SET highscore_{mode} = %s WHERE name = %s"
                val = [score, name]
                mycursor.execute(sql, val)
            printstr += ", retry?"
            message = messagebox.askokcancel(message=printstr)
            mydb.commit()
            if message:
                reset()
            exit()
        if mode == "normal":
            question = Question(False)
        else:
            question = Question(True)
        answButton1.config(text=question.answers[0])
        answButton2.config(text=question.answers[1])
        answButton3.config(text=question.answers[2])
        answButton4.config(text=question.answers[3])
        questionLabel.config(text=question.question)
    def answer0(): #siehe Zeile 149
        answer(0)
    def answer1():
        answer(1)
    def answer2():
        answer(2)
    def answer3():
        answer(3)
### SETUP ###
    root.destroy()
    root = None
    master = tk.Tk()
    master.title("Quiz")
    match mode:
        case "normal":
            answLimit = answLimitNormal
            question = Question(False)
        case "hard":
            answLimit = answLimitHard
            question = Question(True)
        case "practice":
            answLimit = 9999
            valid = False
            question = Question(True)
        case _:
            messagebox.showerror(message="Invalid mode")
            reset()
      
### GUI ###
    questionLabel = tk.Label(master, text=question.question)
    answButton1 = tk.Button(master, text=question.answers[0], command=answer0) #bei command kann keine Funktion mit args angegeben werden da die Funktion sonst beim erstellen des buttons aufgerufen wird
    answButton2 = tk.Button(master, text=question.answers[1], command=answer1)
    answButton3 = tk.Button(master, text=question.answers[2], command=answer2)
    answButton4 = tk.Button(master, text=question.answers[3], command=answer3)
    resultLabel2 = tk.Label(master, text=f"Score: 0, Leben: {answLimit-(scoreMax-score)}")
    resultLabel1 = tk.Label(master, text="")
    questionLabel.pack()
    answButton1.pack(side='bottom', fill='both')
    answButton2.pack(side='bottom', fill='both')
    answButton3.pack(side='bottom', fill='both')
    answButton4.pack(side='bottom', fill='both')
    resultLabel2.pack(side='top')
    resultLabel1.pack(side='top')
    master.mainloop()



def GUI():
### LOGIN ###
    def updateMode(event):
        global mode
        mode = modeSelector.get()
    def start_quiz():
        quiz(nameEntry.get())
    nameLabel = tk.Label(root, text="Name:")
    nameEntry = tk.Entry(root)
    modeLabel = tk.Label(root, text="mode:")
    modeSelector = ttk.Combobox(root, values=["normal", "hard", "practice"]) #practice mode benutzt hard mode nur ohne tracking und fail condition
    continueButton = tk.Button(root, text="continue", command=start_quiz)
    nameLabel.grid(row=0, column=0)
    nameEntry.grid(row=0, column=1)
    modeLabel.grid(row=1, column=0)
    modeSelector.grid(row=1, column=1)
    continueButton.grid(row=2, column=1)
    modeSelector.bind("<<ComboboxSelected>>", updateMode)
    root.mainloop()
    
if __name__ == "__main__":
    GUI()