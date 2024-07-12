import pygame
import time
import json

class Game():
    
    instance = None
    
    # constructor
    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT, CAPTION, ICON_PATH, currentState):
        
        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT
        self.CAPTION = CAPTION
        self.ICON_PATH = ICON_PATH
        self.currentState = currentState
        self.running = True
        
        
        # initialise pygame settings
        self.init()
        
    def init(self):   
        # run state 
        self.currentState.onSwitch()

        # initalise pygame
        pygame.init()

        # set window dimensions
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        # set window title and icon
        pygame.display.set_caption(self.CAPTION)
        pygame.display.set_icon(pygame.image.load(self.ICON_PATH))
        
              
    
                
    def mainLoop(self):
        clock = pygame.time.Clock()
        FPS = 60
       
        
        while self.running:

                
            
            
            clock.tick(60)
            self.checkEvents()
            
            # game loop
            
            self.currentState.update()
            self.currentState.render()

            # render
            pygame.display.update()
        
        # when the game is finished quit
        pygame.quit()

    def checkEvents(self):
        # check for events
        for event in pygame.event.get():
        
            # if x button is pressed stop running
            if event.type == pygame.QUIT:
                self.running = False
            # if x key is pressed
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    self.currentState.save()
                
            self.currentState.checkEvents(event)