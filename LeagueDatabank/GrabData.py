from selenium import webdriver
from selenium.webdriver import ActionChains, FirefoxProfile
from selenium.webdriver.common.by import By
import mysql.connector

import json


def start_browser():
  """
  Starts a new Firefox window with League of Graphs opened. Returns Webdriver of that Window.
  """
  global LoG
  options = webdriver.FirefoxOptions()
  #options.profile = FirefoxProfile("LeagueDatabank\\ttyzbxgh.default-release")
  LoG = webdriver.Firefox(options)
  LoG.get("https://www.leagueofgraphs.com/champions/builds/by-champion-name")

def get_championInfo():
    global LoG
    dictList = []
    champsList = LoG.find_elements(by=By.XPATH, value="//div[@class ='txt']/span[@class ='name']|//div[@class ='txt']/i|//progressbar[@data-color='wggreen']/div/div[@class='progressBarTxt']") #/div/div[@class='progressBarTxt'] is just /div[@class='progressBarTxt'] on non school computers because of outdated firefox
    for i in range(int(len(champsList)/3)):
      name = champsList[i*3].text
      identifier = champsList[i*3].text.lower().replace(" ", "").replace("'", "").replace(".", "").replace("&willump", "").replace("glasc", "").replace("wukong", "monkeyking")
      roles = champsList[(i*3)+1].text.lower().replace("jungler", "jungle").replace("mid", "middle").replace("ad carry", "adc").replace(" ", "")
      generalWinrate = float(champsList[(i*3)+2].text.lower().replace('%',''))
      champ = {
        "identifier": identifier,
        "name": name,
        "roles": roles,
        "winrate": generalWinrate
      }
      dictList.append(champ)
    with open('LeagueDatabank\\champion-info.json', 'w') as champsFile:
      json_obj = json.dumps(dictList, indent=2)
      champsFile.write(json_obj)

def get_winrates(): #reference: https://www.leagueofgraphs.com/champions/builds/aatrox/top
  global LoG
  winrates = []
  with open('LeagueDatabank\\champion-info.json', 'r') as champsFile:
    jsonList = json.load(champsFile) 
    for champ in jsonList:
      if ',' in champ['roles']:
        roles = champ['roles'].split(',')
      else:
        roles = [champ['roles']]
      winrateDict = {
        "identifier": champ['identifier'],
        "top": None,
        "jungle": None,
        "mid": None,
        "bot": None,
        "support": None
      }
      for role in roles:
        role
        LoG.get(f"https://www.leagueofgraphs.com/champions/builds/{champ['identifier']}/{role}")
        winrateDict[role] = float(LoG.find_element(by=By.ID, value='graphDD2').text.replace('%',''))
      winrates.append(winrateDict)
  with open('LeagueDatabank\\winrates.json', 'w') as winratesFile:
    json_obj = json.dumps(winrates, indent=2)
    winratesFile.write(json_obj)

def insert_champions():
  #mydb = mysql.connector.connect(host="localhost", user= "eggbert",password="EggbertHatUser",database="testdb")
  mydb = mysql.connector.connect(host="10.0.41.8", user= "nutzer14",password="Eftg8xdx",database="Datenbank14")
  mycursor = mydb.cursor()
  with open("LeagueDatabank\\winrates.json", 'r') as winratesFile:
    with open("LeagueDatabank\\champion-info.json") as champsFile:
      winrates = json.load(winratesFile)
      champs = json.load(champsFile)
      sql = f"INSERT INTO champion (identifier, name, winrate, winrate_top, winrate_jgl, winrate_mid, winrate_bot, winrate_sup) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
      val = []
      for i in range(len(winrates)):
        val.append((champs[i]['identifier'], champs[i]['name'], champs[i]['winrate'], winrates[i]['top'], winrates[i]['jungle'], winrates[i]['mid'], winrates[i]['bot'], winrates[i]['support']))
  mycursor.executemany(sql, val)
  print(mycursor.rowcount)
  mydb.commit()
#start_browser()
#get_championInfo()
#get_winrates()
#LoG.close()
insert_champions()
#input()