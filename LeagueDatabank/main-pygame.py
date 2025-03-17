import mysql.connector
import pygame
import pygame_menu as pm
import random

pygame.init() 

# Screen 
WIDTH, HEIGHT = 750, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT)) 

# Standard RGB colors 
RED = (255, 0, 0) 
GREEN = (0, 255, 0) 
BLUE = (0, 0, 255) 
CYAN = (0, 100, 100) 
BLACK = (0, 0, 0) 
WHITE = (255, 255, 255) 


def GUI():
    
    def start():
        input()
        
    settings = pm.Menu(title="Settings", 
                    width=WIDTH, 
                    height=HEIGHT, 
                    theme=pm.themes.THEME_GREEN) 
    
    settings._theme.widget_font_size = 25
    settings._theme.widget_font_color = BLACK 
    settings._theme.widget_alignment = pm.locals.ALIGN_CENTER
    
    settings.add.text_input(title="Name: ", textinput_id="username")
    settings.add.toggle_switch(
        title="Disable Voiceline Questiones", default=False, toggleswitch_id="disableVoice"
    )
    settings.add.toggle_switch(
        title="Disable Winrate Questiones", default=False, toggleswitch_id="disableWinrate"
    )
    settings.add.button(title="Restore Defaults", action=settings.reset_value, 
                        font_color=WHITE, background_color=RED) 
    settings.add.button(title="Return To Main Menu", 
                        action=pm.events.BACK, align=pm.locals.ALIGN_CENTER) 
    
    mainMenu = pm.Menu(title="Main Menu", 
                    width=WIDTH, 
                    height=HEIGHT, 
                    theme=pm.themes.THEME_GREEN) 
    mainMenu._theme.widget_alignment = pm.locals.ALIGN_CENTER 
    
    pygame.display.set_caption("test")
    
    mainMenu.add.button(title="Settings", action=settings, 
                        font_color=WHITE, background_color=GREEN)
    mainMenu.add.button(title="Start", action=start, 
                        font_color=WHITE, background_color=RED) 
    mainMenu.mainloop(screen) 
    

if __name__ == "__main__": 
    GUI()
    input()