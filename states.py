import pygame
import json
import time

from game import Game
import globalAccess
import entities

# base class for states
class State():
    
    # constructor
    def __init__(self):
        
        self.init()
    
    def init(self):
    
        # declare entities
        self.entities = []
    
    def update(self):
    
        # loop through and update all entities
        for entity in self.entities:
            entity.update()
            
            # dont update if you aren't the state anymore
            if not(Game.instance.currentState == self):
                return
    
    def render(self):
    
        # loop through and render all entities
        for entity in self.entities:
            entity.render()
        
    def checkEvents(self, event):
    
        # if F key is pressed, save
        if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
            self.save()
        
        # loop through and let entities handle events
        for entity in self.entities:
            entity.checkEvents(event)
    
    # abstract method for when current state is switched
    def onSwitch(self):
        pass
        
        
    # save certain values as a json
    def save(self):
    
        # if the file hasnt loaded yet, dont save
        if not globalAccess.saveDict:
            return
        
        # open the file
        with open("data.save", "w") as save:
        
            # loop through all cats and save their data to the key as a nested array
            
            globalAccess.saveDict["cats"] = [
                [
                    cat.x, cat.y, cat.name, cat.imagePath, cat.health, cat.happiness, cat.hunger, cat.hoariness,
                    cat.handsomeness, cat.hardiness, cat.headsmarts, cat.sayings
                ]
                for cat in Home.ownedCats
            ]
           
            # loop through all items and save their data to the key as a nested array
            
            globalAccess.saveDict["items"] = [
                [
                    item.name, item.price, item.width, item.height, item.imagePath, item.health, item.happiness,
                    item.hunger, item.hoariness, item.handsomeness, item.hardiness, item.headsmarts
                ]
                for item in Home.inventory
            ]

            # save building times
            globalAccess.saveDict["buildings"]["gym"] = Building.gymTime
            globalAccess.saveDict["buildings"]["school"] = Building.schoolTime
            globalAccess.saveDict["buildings"]["barber"] = Building.barberTime
            
            # save the time the cat went to sleep (last time game was closed)
            globalAccess.saveDict["slept"] = int(time.time())
            
            # save the money
            globalAccess.saveDict["money"] = int(globalAccess.money)
            
            # dump the json
            json.dump(globalAccess.saveDict, save)
    
    # load the json
    def load(self, file):
        
        # open the file
        with open(file, "r") as save:
            
            # save to the dictionary
            globalAccess.saveDict = json.loads(save.read())
            
# main menu
class Main(State):

    # singleton so one instance
    instance = None
    
    def init(self):     
        
        # declare entities
        self.entities = [
            entities.Image(0,0,False,1000,600, "resources/start.png"),
            entities.ClickableImage(400, 280, False, 200, 75, "resources/new.png"),
            entities.ClickableImage(400, 400, False, 200, 75, "resources/load.png")
        ]
    
    def update(self):
        super().update()
        
        # if new was clicked start the new save
        if self.entities[1].isClicked:
            self.load("new.save")
        
        # if load was clicked start the current save
        elif self.entities[2].isClicked:
            self.load("data.save")
            
        # if nothing was clicked return so we dont switch the state
        else:
            return
        
        # if it didn't return, a button was clicked so switch the state and start the game
        Game.instance.currentState = Home.instance
        Game.instance.currentState.onSwitch()
            
    def onSwitch(self):
        # music
        pygame.mixer.init()
        pygame.mixer.music.load("resources/mainmusic.mp3")
        pygame.mixer.music.play(-1,0.0)

# class for home (and the start of the actual game part thats why theres so much setup)
class Home(State):

    # initalise class level variables
    inventory = []
    ownedCats = []
    tips = []
    
    # singleton so instance
    instance = None
    
    # whether the save is initialised
    saveInitialised = False
    
    def init(self):
        super().init()
        
        # original entities
        self.OGentities = [
            entities.Image(0,0, False, 1000, 600, "resources/background.png"),
            entities.ClickableImage(-20, 97, False, 180, 300, "resources/door.png"),
            entities.ClickableImage(10, 480, False, 135, 50, "resources/exit.png"),
            entities.ClickableImage(10, 540, False, 135, 50, "resources/save.png")
        ]
        
        # tips to show at the start
        self.tips = globalAccess.tips
        
        # combined entities
        self.entities = (
            self.OGentities +
            self.ownedCats +
            self.inventory +
            [self.tips[0]] # the first tip
        )
        
    def update(self):
        super().update()
        
        # if the save is not initialised but has loaded, initialise
        if not self.saveInitialised and globalAccess.saveDict:
            self.initialiseSave()
        
        # update entities
        self.entities = self.OGentities + self.ownedCats + self.inventory + ([] if not self.tips else [self.tips[0]])
        
        # if the door is clicked, go outside
        if self.entities[1].isClicked:
            
            # change state to outside
            Game.instance.currentState = Outside.instance
            Game.instance.currentState.onSwitch()
        
        # when exit is clicked, stop running
        elif self.entities[2].isClicked:
            
            Game.instance.running = False
        
        # when save is clicked, save
        elif self.entities[3].isClicked:
            
            self.save()
    
    def onSwitch(self):
        # music
        pygame.mixer.init()
        pygame.mixer.music.load("resources/background1.mp3")
        pygame.mixer.music.play(-1,0.0)
        
    def initialiseSave(self):
        
        # if slept is 0, it must be a new save so set it to the time now
        if globalAccess.saveDict["slept"] == 0:
            globalAccess.saveDict["slept"] = time.time()
        
        # set money
        globalAccess.money = int(globalAccess.saveDict["money"])
        
        # get cats
        for cat in globalAccess.saveDict["cats"]:
            self.ownedCats.append(entities.Cat(*cat))
        
        # get items
        for item in globalAccess.saveDict["items"]:
            self.inventory.append(entities.Item(*item)) 
        
        # change the cat's stats based on how long they were away for
        for cat in self.ownedCats:
        
            # time slept in hours
            slept = (time.time() - globalAccess.saveDict["slept"]) //7200
            
            # reduce stats
            cat.changeStats(0, -2*slept, -2*slept, slept, -slept, -slept, -slept)

        # increase time by how long they've been away for
        Building.gymTime = int(time.time()) - globalAccess.saveDict["slept"] + globalAccess.saveDict["buildings"]["gym"]
                        
        Building.schoolTime = int(time.time()) - globalAccess.saveDict["slept"] + globalAccess.saveDict["buildings"]["school"]
                        
        Building.barberTime = int(time.time()) - globalAccess.saveDict["slept"] + globalAccess.saveDict["buildings"]["barber"]
        
        # save is now initialised
        self.saveInitialised = True
        
# walkable map
class Outside(State):
    
    # singleton so instance
    instance = None
    
    # player needs to be accessible
    player = None
    
    def init(self):
        super().init()
        
        # initialise player
        self.player = entities.Player(300,725)
        
        # initialise entities
        self.entities = [
            
            entities.RoamImage(0,0, False, 1900, 1200, "resources/background2.png"),
            self.player,
            
            # houses
            entities.Barrier(100, 100, 500, 300),
            entities.Barrier(700, 100, 500, 300),
            entities.Barrier(1300, 100, 500, 300),
            entities.Barrier(100, 800, 500, 300),
            entities.Barrier(700, 800, 500, 300),
            entities.Barrier(1300, 800, 500, 300),
            
            # doors
            entities.Door(300, 800, 100, 75, Home.instance),
            entities.Door(300, 325, 100, 75, Shop.commonInstance),
            entities.Door(600, 180, 100, 75, Shop.blackInstance),
            entities.Door(900, 325, 100, 75, Shop.vetInstance),
            entities.Door(1500, 325, 100, 75, Building.gymInstance),
            entities.Door(1500, 800, 100, 75, Building.schoolInstance),
            entities.Door(900, 800, 100, 75, Building.barberInstance),
            
            # cats to collect
            entities.Collectible(1780, 560, globalAccess.cats[0]),
            entities.Collectible(620, 835, globalAccess.cats[1]),
            entities.Collectible(1200, 1110, globalAccess.cats[2])
        ]
        
    
    def render(self):
        # make sure the back of the screen is black
        Game.instance.screen.fill((0,0,0))
        
        # get offset for camera stuff
        offsetX = self.player.x - Game.instance.SCREEN_WIDTH // 2 + self.player.width // 2
        offsetY = self.player.y - Game.instance.SCREEN_HEIGHT // 2 + self.player.height // 2
        
        # render entities but pass in offset for those that require it
        for entity in self.entities:
            try:    
                entity.render(offsetX, offsetY)
            except:
                entity.render()
        
    def onSwitch(self):
        # music
        pygame.mixer.init()
        pygame.mixer.music.load("resources/background2.mp3")
        pygame.mixer.music.play(-1,0.0)   
        self.player.image = pygame.image.load(self.player.imagePath)
        
        # add entities as they might be back
        
        # if there is a tip get it and remove it temporarily to handle the entities
        tempTip = None
        if isinstance(self.entities[-1], entities.Tip):
            tempTip = self.entities[-1]
            self.entities.pop()
        
        # add the collectibles
        self.entities = self.entities[: 15]
        self.entities += [
            entities.Collectible(1780, 560, globalAccess.cats[0]),
            entities.Collectible(620, 835, globalAccess.cats[1]),
            entities.Collectible(1200, 1110, globalAccess.cats[2])
        ]
        
        # add the tip back
        if tempTip:
            self.entities.append(tempTip)
       

# class for any particular building
class Building(State):
    
    # instances
    gymInstance = None
    schoolInstance = None
    barberInstance = None
    
    # times since last entered
    gymTime = 0
    schoolTime = 0
    barberTime = 0
        
    def __init__(self, imagePath, musicPath, stat):
        
        self.imagePath = imagePath
        self.musicPath = musicPath
        self.stat = stat
        
        super().__init__()
    
    def init(self):
    
        # scene begins unstarted and at 0 seconds
        self.scene = False
        self.time = 0
        
        # stat increase is not money by default
        self.isMoney = False
        
        # initalise entities
        self.entities = [
            entities.Image(0,0, False, 1000, 600, "resources/buildingfront.png"),
            
            # buttons
            entities.ClickableImage(200, 320, False, 135, 50, "resources/work.png"),
            entities.ClickableImage(665, 320, False, 135, 50, "resources/use.png"),
            entities.ClickableImage(432, 500, False, 135, 50, "resources/leave.png")
        ]
        
        
    def update(self):
        super().update()
        
        
        
        # if scene is now playing
        if self.scene:
        
            # if scene has just started
            if self.time == 0:
            
                # start music
                pygame.mixer.init()
                pygame.mixer.music.load(self.musicPath)
                pygame.mixer.music.play(-1,0.0) 
                
                # add entiities for scene
                self.entities = [
                    entities.Image(0,0, False, 1000, 600, self.imagePath),
                    entities.Image(400,250, False, 200, 300, Outside.instance.player.imagePath)
                ]
                
            # increase time
            self.time += 1
            
            # when scene reaches end
            if self.time > 360:
                
                # reset the corresponding time
                match self.stat:
                    case "hardiness":
                        Building.gymTime = 0
                    case "handsomeness":
                        Building.barberTime = 0
                    case "headsmarts":
                        Building.schoolTime = 0
                    case _:
                        pass
                
                # change the state
                Game.instance.currentState = Outside.instance   
                    
                # append with tip about skill or money increase
                Game.instance.currentState.entities.append(
                    entities.Tip(
                        f"money increased by {(self.cat.getAttributeDict()[self.stat] + 10) * 3}\nnew total: {globalAccess.money}"
                        if self.isMoney
                        else f"{self.stat} increased by 50\nnew total: {self.cat.getAttributeDict()[self.stat]}"
                    )
                )
                
                # run state 
                Game.instance.currentState.onSwitch()
            
            return
                
        # if work is clicked
        if self.entities[1].isClicked:
                    
            # increase money based on skills
            globalAccess.money += (self.cat.getAttributeDict()[self.stat] + 10) * 3
            
            # we are giving them money
            self.isMoney = True
            
            # start scene
            self.scene = True
        
        # if use is clicked
        elif self.entities[2].isClicked:
        
            # increase the corresponding stat
            match self.stat:
                case "handsomeness":
                    self.cat.handsomeness += 50
                case "hardiness":
                    self.cat.hardiness += 50
                case "headsmarts":
                    self.cat.headsmarts += 50
                case _:
                    pass 
                    
            # start scene
            self.scene = True
            
        # if leave is pressed, leave 
        elif self.entities[3].isClicked:
            
            # change state back to outside
            Game.instance.currentState = Outside.instance
            Game.instance.currentState.onSwitch()
            
    def onSwitch(self):
        if Outside.instance.player.imagePath == "resources/icon.png":
            # change state back to outside
            Game.instance.currentState = Outside.instance
            
            # add tip
            Game.instance.currentState.entities.append(entities.Tip("You have no cat equipped, you silly billi!!\nclick a cat in your house to equip it"))
            
            # switch now
            Game.instance.currentState.onSwitch()

        # initialise cat, get the cat that matches the player
        for cat in Home.instance.ownedCats:
            if cat.imagePath == Outside.instance.player.imagePath:
                self.cat = cat
        
        # if the time isnt right yet
        if (self.stat == "hardiness" and Building.gymTime < 86400) or\
            (self.stat == "headsmarts" and Building.schoolTime < 86400) or\
            (self.stat == "handsomeness" and Building.barberTime < 86400):
            
            # change state back to outside
            Game.instance.currentState = Outside.instance
            
            # add tip
            Game.instance.currentState.entities.append(entities.Tip("Not enough time has passed, try again later."))
            
            # switch now
            Game.instance.currentState.onSwitch()
        
        
        self.init()
        
# initalise instances
Building.gymInstance = Building("resources/gym.png", "resources/gym.mp3", "hardiness")
Building.schoolInstance = Building("resources/school.png", "resources/school.mp3", "headsmarts")
Building.barberInstance = Building("resources/barber.png", "resources/barber.mp3", "handsomeness")


# class for shops
class Shop(State):
    
    # instances
    commonInstance = None
    blackInstance = None
    vetInstance = None

    def __init__(self, entranceSay, purchaseSay, items, imagePath, musicPath):
        
        self.entranceSay = entranceSay
        self.purchaseSay = purchaseSay
        self.items = items
        self.imagePath = imagePath
        self.musicPath = musicPath
        
        super().__init__()
    
    def init(self):
        
        # entities
        self.entities = [
            entities.Image(0,0, False, 1000, 600, self.imagePath),
            
            # buttons
            entities.ClickableImage(760, 400, False, 135, 50, "resources/buy.png"),
            entities.ClickableImage(760, 470, False, 135, 50, "resources/next.png"),
            entities.ClickableImage(760, 540, False, 135, 50, "resources/leave.png")
        ]
        
        # set current saying
        self.currentSaying = self.entranceSay
        
        # set current item index
        self.currentItem = 0
        
        # FONT STUFF
        pygame.font.init()
        
        self.statsFont = pygame.font.Font("resources/Cascadia Code.ttf", 15)
        self.talkFont = pygame.font.Font("resources/Cascadia Code.ttf", 20)
        self.nameFont = pygame.font.Font("resources/Cascadia Code.ttf", 27)
        
        # make texts with the fonts
        
        self.moneyText = self.nameFont.render(str(int(globalAccess.money)), True, (0, 0, 0))
        
        self.costText = self.nameFont.render("$ " + str(self.items[self.currentItem][1]), True, (0, 0, 0))
        
        self.nameText = self.nameFont.render(self.items[self.currentItem][0], True, (0, 0, 0))
        
        self.statsTexts = globalAccess.renderMultilineFont((
            f"HEALTH: {self.items[self.currentItem][5]}",
            f"HAPPINESS: {self.items[self.currentItem][6]}",
            f"HUNGER: {self.items[self.currentItem][7]}",
            f"HOARINESS: {self.items[self.currentItem][8]}",
            f"HANDSOMENESS: {self.items[self.currentItem][9]}",
            f"HARDINESS: {self.items[self.currentItem][10]}",
            f"HEADSMARTS: {self.items[self.currentItem][11]}"

        ), self.statsFont)
        
        self.sayingText = self.talkFont.render(self.currentSaying, True,(0, 0, 0))
        
    def render(self):
        super().render()
        
        # render text
        
        # render saying
        Game.instance.screen.blit(self.sayingText, (230 - 4*len(self.currentSaying), 500))
        
        # render money
        Game.instance.screen.blit(self.moneyText, (850, 82))
        
        # render item stuff
        Game.instance.screen.blit(self.costText, (900, 190))
        
        Game.instance.screen.blit(self.nameText, (800 - 5*len(self.items[self.currentItem][0]), 135))

        globalAccess.blitMultilineFont(self.statsTexts, Game.instance.screen, 750, 270, 17)
        
        # load and transform image
        resizedImage = pygame.transform.scale(pygame.image.load(self.items[self.currentItem][4]),
        (self.items[self.currentItem][2], self.items[self.currentItem][3])) # width and height
        
        # render image
        Game.instance.screen.blit(resizedImage, (790, 180))
       
    def update(self):
        super().update()
        
        # if leave is clicked, go outside
        if self.entities[3].isClicked:
        
            # switch state
            Game.instance.currentState = Outside.instance
            Game.instance.currentState.onSwitch()
        
        # if next item is clicked, go to next item
        elif self.entities[2].isClicked:
        
            # go to next item or beginning
            self.currentItem = self.currentItem + 1 if self.currentItem + 1 < len(self.items) else 0
            
            # change displayed name and stats to current item
            self.costText = self.nameFont.render("$ " + str(self.items[self.currentItem][1]), True, (0, 0, 0))
            
            self.nameText = self.nameFont.render(self.items[self.currentItem][0], True, (0, 0, 0))
        
            self.statsTexts = globalAccess.renderMultilineFont((
                f"HEALTH: {self.items[self.currentItem][5]}",
                f"HAPPINESS: {self.items[self.currentItem][6]}",
                f"HUNGER: {self.items[self.currentItem][7]}",
                f"HOARINESS: {self.items[self.currentItem][8]}",
                f"HANDSOMENESS: {self.items[self.currentItem][9]}",
                f"HARDINESS: {self.items[self.currentItem][10]}",
                f"HEADSMARTS: {self.items[self.currentItem][11]}"

            ), self.statsFont)
        
        # if buy is clicked
        elif self.entities[1].isClicked:
        
            # if person has enough money
            if (globalAccess.money >= self.items[self.currentItem][1]):
            
                # take away money
                globalAccess.money -= self.items[self.currentItem][1]
                
                # add to inventory
                Home.inventory.append(entities.Item(*self.items[self.currentItem]))
                
                # update money
                self.moneyText = self.nameFont.render(str(int(globalAccess.money)), True, (0, 0, 0))
                
                # update saying
                self.currentSaying = self.purchaseSay
                
                globalAccess.kaching.play()
            else:
                self.currentSaying = "You dont have enough money buddy"
                globalAccess.womp.play()
        
        # update saying
        self.sayingText = self.talkFont.render(self.currentSaying, True,(0, 0, 0))
        
    def onSwitch(self):
        # music
        pygame.mixer.init()
        pygame.mixer.music.load(self.musicPath)
        pygame.mixer.music.play(-1,0.0)   

        self.init()


# initialise shop instances: health, happiness, hunger, hoariness, handsomeness, hardiness, headsmarts
    
Shop.commonInstance = Shop("Welcome! I'm John Carmack, please buy my wares.", "Thanks for purchasing, now i can make my engine!",
    (
        ("Apple", 20, 60, 75, "resources/apple.png", 0, 0, 10, 0, 0, 5, 0),
        ("hamburger", 30, 75, 50, "resources/hamburger.png", 0, 10, 15, 0, 0, -5, 0),
        ("Toy", 40, 75, 50, "resources/toy.png", 0, 20, 0, 0, 0, 0, 0),
        ("chess set", 30, 65, 65, "resources/chess set.png", 0, 10, 0, 0, 0, 0, 5),
        ("bowtie", 35, 75, 50, "resources/bowtie.png", 0, 5, 0, 0, 10, 0, 0),
        ("protein powder", 45, 50, 65, "resources/protein shake.png", 5, 0, 5, 0, 0, 10, 0),
        ("dumbell", 30, 75, 50, "resources/dumbell.png", 0, 0, 0, 0, 0, 10, 0),
        ("homework", 25, 50, 60, "resources/homework.png", 0, -10, 0, 0, 0, 0, 10)
    ),
"resources/background3.png", "resources/background3.mp3"
)

Shop.blackInstance = Shop("H3LL0, 1 4M 4 L337 H4XX0R, BUY MY STUFF M8", "TYSM!!! :) :)",
    (
        ("health potion", 90, 60, 75, "resources/health potion.png", 50, 0, 0, 1, 0, 0, 0),
        ("anti-depressant", 80, 50, 75, "resources/anti depressants.png", -10, 50, 0, 0, 0, 0, 0),
        ("ULTRA HAMBURGER", 70, 50, 75, "resources/ULTRA HAMBURGER.png", -10, 0, 50, 0, 0, 0, 0),
        ("age reversing pill", 200, 60, 60, "resources/age reversing pill.png", -10, 0, 0, -20, 0, 0, 0),
        ("botox", 70, 60, 75, "resources/botox.png", -10,0,0,0,40,0,0),
        ("steroids", 80, 60, 60, "resources/steroids.png", -10, 0, 0,0,0,40, 0),
        ("fake degree", 75, 60, 60, "resources/fake degree.png", -10, 0, 0, 0, 0, 0, 40)
    ),
"resources/blackbackground.png", "resources/blackbackground.mp3"
)

Shop.vetInstance = Shop("You look sick may i suggest a lobotomy?", "thank you kindly.",
    (
        ("bandage", 50, 60, 60, "resources/bandage.png", 20, 0, 0, 0, 0, 0, 0),
        ("poison", 100, 50, 75, "resources/poison.png", -50, 0, 0, 0, 0, 0, 0)
    ),
"resources/vetbackground.png", "resources/vetbackground.mp3"
)

# initialise normal instances
Home.instance = Home()
Outside.instance = Outside()
Main.instance = Main()

