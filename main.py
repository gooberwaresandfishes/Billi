from game import Game
import states

def main():
    
    # start new game
    
    Game.instance = Game(1000, 600, "Billi", "resources/icon.png", states.Main.instance)

    # start the main loop
    Game.instance.mainLoop()

# entrance
if __name__ == "__main__":
    main()