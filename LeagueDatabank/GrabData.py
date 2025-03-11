from selenium import webdriver
from selenium.webdriver import ActionChains, FirefoxProfile
from selenium.webdriver.common.by import By

import json


def start_browser():
  """
  Starts a new Firefox window with League of Graphs opened. Returns Webdriver of that Window.
  """
  global LoG
  options = webdriver.FirefoxOptions()
  options.profile = FirefoxProfile("LeagueDatabank\\ttyzbxgh.default-release")
  LoG = webdriver.Firefox(options)
  LoG.get("https://www.leagueofgraphs.com/champions/builds/by-champion-name")

def get_championInfo():
    global LoG
    dictList = []
    champsList = LoG.find_elements(by=By.XPATH, value="//div[@class ='txt']/span[@class ='name']|//div[@class ='txt']/i|//progressbar[@data-color='wggreen']/div[@class='progressBarTxt']")
    for i in range(int(len(champsList)/3)):
      name = champsList[i*3].text.lower().replace(" ", "").replace("'", "").replace(".", "").replace("&willump", "").replace("glasc", "").replace("wukong", "monkeyking")
      roles = champsList[(i*3)+1].text.lower().replace("jungler", "jungle").replace("mid", "middle").replace("ad carry", "adc").replace(" ", "")
        
      generalWinrate = champsList[(i*3)+2].text.lower()
      champ = {
        "name": name,
        "roles": roles,
        "Winrate": generalWinrate
      }
      dictList.append(champ)
    with open('LeagueDatabank\\champion-info.json', 'w') as champsFile:
      json_obj = json.dumps(dictList, indent=2)
      champsFile.write(json_obj)

def get_winrates(): #https://www.leagueofgraphs.com/champions/builds/aatrox/top
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
        "top": None,
        "jungle": None,
        "mid": None,
        "bot": None,
        "support": None
      }
      for role in roles:
        role
        LoG.get(f"https://www.leagueofgraphs.com/champions/builds/{champ['name']}/{role}")
        winrateDict[role] = LoG.find_elements(by=By.ID, value='graphDD1')[1].text
      winrates.append(winrateDict)
  with open('LeagueDatabank\\winrates.json', 'w') as winratesFile:
    json_obj = json.dumps(winrates, indent=2)
    winratesFile.write(json_obj)

start_browser()
get_championInfo()
get_winrates()
input()