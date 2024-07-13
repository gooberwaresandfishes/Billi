from game import Game
import states
import pygame

# main function
def main():
    # initialise before anything just to make sure
    pygame.init()
    
    # start new game
    Game.instance = Game(1000, 600, "Billi", "resources/icon.png", states.Main.instance)

    # start the main loop
    Game.instance.mainLoop()

# program entrance
if __name__ == "__main__":
    main()