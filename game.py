import pygame
import time

# the main class that consists of mostly generic functionality
class Game():
    
    # singleton so one instance
    instance = None
    
    # constructor
    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT, CAPTION, ICON_PATH, currentState):
        
        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT
        self.CAPTION = CAPTION
        self.ICON_PATH = ICON_PATH
        self.currentState = currentState
        
        # initialise settings
        self.init()
    
    # to initalise settings
    def init(self):
        
        # set running to true
        self.running = True
        self.dt = 1
        
        # initalise pygame
        pygame.init()

        # set window dimensions
        
        info = pygame.display.Info()
        flags = pygame.SCALED | pygame.HWSURFACE | pygame.DOUBLEBUF
        
        # if it fails just make it fullscreen i dont care (probably android if it fails and we want it fullscreen)
        try:
            # if screen is too small to fit window, fullscreen it
            if info.current_w <= self.SCREEN_WIDTH and info.current_y <= self.SCREEN_HEIGHT:
                flags |= pygame.FULLSCREEN
        except:
            flags |= pygame.FULLSCREEN

        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), flags)
        
        # set window title and icon
        pygame.display.set_caption(self.CAPTION)
        pygame.display.set_icon(pygame.image.load(self.ICON_PATH))
        
        # switch to the current state
        self.currentState.onSwitch()
    
    # heart of the program
    def mainLoop(self):
        
        # setup FPS
        clock = pygame.time.Clock()
        FPS = 60
        prev_time = time.time()
        
        # loop while running
        while self.running:
            
            # if the game updated too fast, wait so it wont go over 60 FPS
            clock.tick(60)
            
            # delta time stuff
            
            

            now = time.time()
            self.dt = now - prev_time
            prev_time = now
            
            # state loop
            
            # check for player input
            self.checkEvents()
            
            self.currentState.update()
            self.currentState.render()

            # update the window
            pygame.display.update()
        
        # when the game is finished, quit
        pygame.quit()
    
    # check for player input
    def checkEvents(self):
    
        # iterate through each event
        for event in pygame.event.get():
        
            # if x is pressed stop running
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.running = False
            
            # let state handle events
            self.currentState.checkEvents(event)