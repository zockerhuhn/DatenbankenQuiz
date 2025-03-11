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
    namesList = LoG.find_elements(by=By.CLASS_NAME, value="txt")
    namesList.pop(0)
    with open('LeagueDatabank\\champion-info.json', 'w') as namesFile:
        for i in namesList:
            namesFile.write(i.text + '\n')
            print(i.text)

start_browser()
get_championInfo()
# input()