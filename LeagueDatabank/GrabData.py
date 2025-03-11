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
  #options.profile = FirefoxProfile("LeagueDatabank\\ttyzbxgh.default-release")
  LoG = webdriver.Firefox(options)
  LoG.get("https://www.leagueofgraphs.com/champions/builds/by-champion-name")

def get_championInfo():
    global LoG
    dictList = []
    champsList = LoG.find_elements(by=By.XPATH, value="//div[@class ='txt']/span[@class ='name']|//div[@class ='txt']/i|//progressbar[@data-color='wggreen']/div/div[@class='progressBarTxt']")
    for i in range(int(len(champsList)/3)):
      name = champsList[i*3].text
      roles = champsList[(i*3)+1].text
      generalWinrate = champsList[(i*3)+2].text
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
  champsList = []
  with open('LeagueDatabank\\champion-info.json', 'r') as champsFile:
   jsonList 
    
            
start_browser()
get_championInfo()
# input()
