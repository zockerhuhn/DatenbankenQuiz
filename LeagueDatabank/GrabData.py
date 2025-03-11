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
    champsList = LoG.find_elements(by=By.XPATH, value="//div/span[@class ='name']")
    champsList.pop(0)
    with open('LeagueDatabank\\champion-info.json', 'w') as namesFile:
        for i in champsList:
            name = i.find_element(by=By.ID, value='name')
            roles = i.find_element(by=By.NAME, value='i')
            champ = {
              "name": name,
              "roles": roles
            }
            print(champ)
             
            
start_browser()
get_championInfo()
# input()