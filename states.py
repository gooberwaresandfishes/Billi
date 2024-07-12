import entities
import globalAccess
from game import Game
import pygame
import time
import json





# base class
class State():
    
    def __init__(self):
        
        self.init()
    
    def init(self):
        self.entities = []
    
    def update(self):
        for entity in self.entities:
            entity.update()
            
            if not(Game.instance.currentState == self):
                return
    
    def render(self):
        for entity in self.entities:
            entity.render()
        
    def checkEvents(self, event):
        for entity in self.entities:
            entity.checkEvents(event)
            
    def onSwitch(self):
        pass
    #health, happiness, hunger, hoariness, handsomeness, hardiness, headsmarts, sayings):
    def save(self):
        with open("data.save", "w") as save:
            cats = []
            for cat in Home.ownedCats:
                cats.append(
                [
                    cat.x,cat.y,cat.name,cat.imagePath,cat.health, cat.happiness, cat.hunger, cat.hoariness,
                    cat.handsomeness, cat.hardiness, cat.headsmarts, cat.sayings
                ]
                )
            
            globalAccess.saveDict["cats"] = cats
            
            items = []
            for item in Home.inventory:
                items.append(
                [
                    item.name, item.price, item.width, item.height, item.imagePath, item.health, item.happiness, item.hunger, item.hoariness,
                    item.handsomeness, item.hardiness, item.headsmarts
                ]
                )
            
            globalAccess.saveDict["items"] = items
            
            globalAccess.saveDict["buildings"]["gym"] = Building.gymTime
                
            globalAccess.saveDict["buildings"]["school"] = Building.schoolTime
                
            globalAccess.saveDict["buildings"]["barber"] = Building.barberTime
            
            globalAccess.saveDict["slept"] = int(time.time())
            globalAccess.saveDict["tips"] = []
            globalAccess.saveDict["money"] = int(globalAccess.money)
            
            json.dump(globalAccess.saveDict, save)
    
    def load(self,file):
        with open(file, "r") as save:
            globalAccess.saveDict = json.loads(save.read())
            if globalAccess.saveDict["slept"] == 0:
                globalAccess.saveDict["slept"] = time.time()

class Main(State):
    instance = None
    
    def init(self):
        super().init()
        self.entities = [
        entities.Image(0,0,False,1000,600, "resources/start.png"),
        entities.ClickableImage(400, 280, False, 200, 75, "resources/new.png"),
        entities.ClickableImage(400, 400, False, 200, 75, "resources/load.png")
        ]
    
    def update(self):
        super().update()
        
        if self.entities[1].isClicked:
            self.load("new.save")
            Game.instance.currentState = Home.instance
            Game.instance.currentState.onSwitch()
        elif self.entities[2].isClicked:
            self.load("data.save")
            Game.instance.currentState = Home.instance
            Game.instance.currentState.onSwitch()
        
    def checkEvents(self, event):
        for entity in self.entities:
            entity.checkEvents(event)
            
    def onSwitch(self):
        # music
        pygame.mixer.init()
        pygame.mixer.music.load("resources/mainmusic.mp3")
        pygame.mixer.music.play(-1,0.0)

     
class Home(State):
    inventory = []
    ownedCats = []
    tips = []
    instance = None
    currentFlag = False
    
    def init(self):
        super().init()
        
        
        
        self.OGentities = [
            entities.Image(0,0, False, 1000, 600, "resources/background.png"),
            entities.ClickableImage(-20, 97, False, 180, 300, "resources/door.png")
            
            
        ]
        
        self.tips = [
            entities.Tip("Welcome",
            '''
            Welcome to billi!
            '''
            ,
            True),
            entities.Tip("Sleep",
            '''
            HOW TO PLAY:\n
            Your job is to look after your cat(s)\n
            to do this you must feed them items\n
            to feed them items you need money\n
            to get money you need to work\n
            '''
            ,
            True),
            entities.Tip("Cats",
            '''
            CATS:\n
            You currently own 1 cat, there are 2\n
            other cats scattered around the map\n
            your cats stats go down over time\n
            when you leave the game they go to sleep\n
            when they are asleep they lose stats slower\n
            for every stat that reaches its lowest\n
            your cat starts taking health damage\n
            if your cat is asleep it wont take damage\n
            click on your cat to see its condition\n
            '''
            ,
            True),
            entities.Tip("Items",
            '''
            ITEMS:\n
            items increase your cats stats\n
            to feed a cat an item just drag
            it onto him\n
            '''
            ,
            True),
            entities.Tip("Shops",
            '''
            SHOPS:\n
            there are 3 shops in the map\n
            (one is in the alley)\n
            you can buy items from shops\n
            just walk into one\n
            '''
            ,
            True),
            entities.Tip("Work",
            '''
            WORK:\n
            there are 3 other buildings in the map\n
            when you enter them you can work or use\n
            using gives you a skill upgrade\n
            working gives you money based on your\n
            current skill (handsomeness for barber etc)\n
            you can use or work once a day\n
            '''
            ,
            True),
            entities.Tip("World",
            '''
            WORLD:\n
            you can leave the house by clicking the door\n
            when you leave you can take 1 cat with you\n
            click on the cat you want to take before\n
            you leave\n
            when in the world walk with WASD controls\n
            and explore, walk into the black door to\n
            enter buildings
            '''
            ,
            True),
            entities.Tip("Save",
            '''
            SAVE:\n
            press the F button to save, and have fun!
            '''
            ,
            True)
        ]
        
        self.entities = self.OGentities + self.ownedCats + self.inventory + ([] if len(self.tips) == 0 else [self.tips[0]])
        
        
    def update(self):
        super().update()
        
        
        try:
            if not self.currentFlag:
                globalAccess.money = int(globalAccess.saveDict["money"])
                for cat in globalAccess.saveDict["cats"]:
                    self.ownedCats.append(entities.Cat(*cat))
                
                for item in globalAccess.saveDict["items"]:
                    self.inventory.append(entities.Item(*item)) 
                
                for cat in self.ownedCats:
                    slept = (time.time() - globalAccess.saveDict["slept"]) //3600
                    
                    cat.changeStats(0, -2*slept, -2*slept, slept, -slept, -slept, -slept)
                
                entities.Tip.hasOccured = globalAccess.saveDict["tips"]
                
                Building.gymTime = int(time.time()) - globalAccess.saveDict["slept"] +\
                globalAccess.saveDict["buildings"]["gym"]
                
                Building.schoolTime = int(time.time()) - globalAccess.saveDict["slept"] +\
                globalAccess.saveDict["buildings"]["school"]
                
                Building.barberTime = int(time.time()) - globalAccess.saveDict["slept"] +\
                globalAccess.saveDict["buildings"]["barber"]
                
                self.currentFlag = True
        except Exception as e:
            #print(e)
            pass
            
         
        
        self.entities = self.OGentities + self.ownedCats + self.inventory + ([] if len(self.tips) == 0 else [self.tips[0]])
        
        if self.entities[1].isClicked:
            Game.instance.currentState = Outside.instance
            # run state 
            Game.instance.currentState.onSwitch()
    
    def onSwitch(self):
        # music
        pygame.mixer.init()
        pygame.mixer.music.load("resources/background1.mp3")
        pygame.mixer.music.play(-1,0.0)
        
        
        
        
        

class Outside(State):
    
    instance = None
    player = None
    
    def init(self):
        super().init()
        
        self.player = entities.Player(300,725)

        self.entities = [
            
            entities.RoamImage(0,0, False, 1900, 1200, "resources/background2.png"),
            self.player,
            entities.Barrier(100, 100, 500, 300),
            entities.Barrier(700, 100, 500, 300),
            entities.Barrier(1300, 100, 500, 300),
            entities.Barrier(100, 800, 500, 300),
            entities.Barrier(700, 800, 500, 300),
            entities.Barrier(1300, 800, 500, 300),
            entities.Door(300, 800, 100, 75, Home.instance),
            entities.Door(300, 325, 100, 75, Shop.commonInstance),
            entities.Door(600, 180, 100, 75, Shop.blackInstance),
            entities.Door(900, 325, 100, 75, Shop.vetInstance),
            entities.Door(1500, 325, 100, 75, Building.gymInstance),
            entities.Door(1500, 800, 100, 75, Building.schoolInstance),
            entities.Door(900, 800, 100, 75, Building.barberInstance),
            entities.Collectible(620, 835, globalAccess.cats[1]),
            entities.Collectible(1200, 1110, globalAccess.cats[2])
        ]
        
    
    def render(self):
        Game.instance.screen.fill((0,0,0))
        
        offsetX = self.player.x - Game.instance.SCREEN_WIDTH // 2 + self.player.width // 2
        offsetY = self.player.y - Game.instance.SCREEN_HEIGHT // 2 + self.player.height // 2
        
        
        for entity in self.entities:
            if entity == self.player:
                entity.render()
                continue
            try:    
                entity.render(offsetX, offsetY)
            except:
                entity.render()
        
    def update(self):
        super().update()
        
    def onSwitch(self):
        # music
        pygame.mixer.init()
        pygame.mixer.music.load("resources/background2.mp3")
        pygame.mixer.music.play(-1,0.0)   
        self.player.image = pygame.image.load(self.player.imagePath)
       

class Building(State):

    gymInstance = None
    schoolInstance = None
    barberInstance = None
    
    gymTime = 0
    schoolTime = 0
    barberTime = 0
        
    def __init__(self, imagePath, musicPath, stat):
        
        self.imagePath = imagePath
        self.musicPath = musicPath
        self.stat = stat
        
        
        super().__init__()
    
    def init(self):
        super().init()
        
        self.scene = False
        self.time = 0
        self.isMoney = False
        
        self.entities = [
            entities.Image(0,0, False, 1000, 600, "resources/buildingfront.png"),
            entities.ClickableImage(200, 320, False, 135, 50, "resources/work.png"),
            entities.ClickableImage(665, 320, False, 135, 50, "resources/use.png")
        ]
        
        
    def render(self):
        super().render()

        
    def update(self):
        super().update()
        
        if (self.stat == "hardiness" and Building.gymTime < 86400) or (self.stat == "headsmarts" and Building.schoolTime < 86400) or\
            (self.stat == "handsomeness" and Building.barberTime < 86400):
            Game.instance.currentState = Outside.instance
            
            Game.instance.currentState.entities.append(entities.Tip("Again","try again tommorow", False))
            
           
            
            Game.instance.currentState.onSwitch()
        
        if self.scene:
            if not(self.time > 0) :
                pygame.mixer.init()
                pygame.mixer.music.load(self.musicPath)
                pygame.mixer.music.play(-1,0.0) 
                
                self.entities = [
                    entities.Image(0,0, False, 1000, 600, self.imagePath),
                    entities.Image(400,250, False, 200, 300, Outside.instance.player.imagePath)
                ]
                
                
            
            self.time += 1
            
            if self.time > 360:
                
                if self.stat == "hardiness":
                    Building.gymTime = 0
                elif self.stat == "handsomeness":
                    Building.barberTime = 0
                elif self.stat == "headsmarts":
                    Building.schoolTime = 0
                
                Game.instance.currentState = Outside.instance
                
                for cat in Home.instance.ownedCats:
                    if cat.imagePath == Outside.instance.player.imagePath:
                        Game.instance.currentState.entities.append(entities.Tip("Increase",
                            f"money increased by {cat.getAttributeDict()[self.stat] * 3}\n" if self.isMoney else\
                            f"{self.stat} increased by 20\n"
                        ,
                        False))
                # run state 
                Game.instance.currentState.onSwitch()
            
            return
                
                

            
        # if work is clicked
        if self.entities[1].isClicked:
            for cat in Home.instance.ownedCats:
                if cat.imagePath == Outside.instance.player.imagePath:
                    self.isMoney = True
                    
                
                    globalAccess.money += cat.getAttributeDict()[self.stat] * 3
                    globalAccess.money = int(globalAccess.money)
                    self.scene = True
                    
        elif self.entities[2].isClicked:
            for cat in Home.instance.ownedCats:
                if cat.imagePath == Outside.instance.player.imagePath:
                    if self.stat == "handsomeness":
                        
                        cat.handsomeness += 20
                    elif self.stat == "hardiness":
                        
                        cat.hardiness += 20
                    elif self.stat == "headsmarts":
                    
                        cat.headsmarts += 20
                    
                    self.scene = True
            
    def onSwitch(self):
        self.init()
        
        

Building.gymInstance = Building("resources/gym.png", "resources/gym.mp3", "hardiness")
Building.schoolInstance = Building("resources/school.png", "resources/school.mp3", "headsmarts")
Building.barberInstance = Building("resources/barber.png", "resources/barber.mp3", "handsomeness")

class Shop(State):

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
        super().init()
              
        self.entities = [
            entities.Image(0,0, False, 1000, 600, self.imagePath),
            entities.ClickableImage(760, 400, False, 135, 50, "resources/buy.png"),
            entities.ClickableImage(760, 470, False, 135, 50, "resources/next.png"),
            entities.ClickableImage(760, 540, False, 135, 50, "resources/leave.png")
        ]
        
        self.currentSaying = self.entranceSay
        self.currentItem = 0
        
        pygame.font.init()
        
        self.statsFont = pygame.font.Font("resources/Cascadia Code.ttf", 15)
        self.talkFont = pygame.font.Font("resources/Cascadia Code.ttf", 20)
        self.nameFont = pygame.font.Font("resources/Cascadia Code.ttf", 27)
        
        
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
        Game.instance.screen.blit(self.moneyText, (850, 82))
        
        Game.instance.screen.blit(self.costText, (900, 190))
        
        Game.instance.screen.blit(self.nameText, (800 - 5*len(self.items[self.currentItem][0]), 135))

        globalAccess.blitMultilineFont(self.statsTexts, Game.instance.screen, 750, 270, 17)
        
        resizedImage = pygame.transform.scale(pygame.image.load(self.items[self.currentItem][4]),
        (self.items[self.currentItem][2], self.items[self.currentItem][3]) )
        
        Game.instance.screen.blit(resizedImage, (790, 180))
        
        Game.instance.screen.blit(self.sayingText, (230 - 4*len(self.currentSaying), 500))
        

        
    def update(self):
        super().update()
        
        
        if self.entities[3].isClicked:
            Game.instance.currentState = Outside.instance
            # run state 
            Game.instance.currentState.onSwitch()
        
        # if next item
        elif self.entities[2].isClicked:
        
            # go to next item or beggining
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
                
                globalAccess.money = int(globalAccess.money)
                
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
                
        self.sayingText = self.talkFont.render(self.currentSaying, True,(0, 0, 0))
        
    def onSwitch(self):
        # music
        pygame.mixer.init()
        pygame.mixer.music.load(self.musicPath)
        pygame.mixer.music.play(-1,0.0)   

        self.currentSaying = self.entranceSay
        self.currentItem = 0
        
        pygame.font.init()
        
        self.statsFont = pygame.font.Font("resources/Cascadia Code.ttf", 15)
        self.talkFont = pygame.font.Font("resources/Cascadia Code.ttf", 20)
        self.nameFont = pygame.font.Font("resources/Cascadia Code.ttf", 27)
        
        
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


#name, price, width, height, imagePath, health, happiness, hunger, hoariness, handsomeness, hardiness, headsmarts
    
Shop.commonInstance = Shop("Welcome! I'm John Carmack, please buy my wares.", "Thanks for purchasing, now i can make my engine!",
    (
        ("Apple", 20, 60, 75, "resources/apple.png", 0, 0, 10, 0, 0, 5, 0),
        ("hamburger", 30, 75, 50, "resources/hamburger.png", 0, 10, 15, 0, 0, -5, 0),
        ("Toy", 40, 75, 50, "resources/toy.png", 0, 20, 0, 0, 0, 0, 0),
        ("chess set", 30, 65, 65, "resources/chess set.png", 0, 10, 0, 0, 0, 0, 10),
        ("bowtie", 35, 75, 50, "resources/bowtie.png", 0, 5, 0, 0, 10, 0, 0),
        ("protein powder", 45, 50, 65, "resources/protein shake.png", 5, 0, 5, 0, 0, 10, 0, 0),
        ("dumbell", 30, 75, 50, "resources/dumbell.png", 0, 0, 0, 0, 0, 10, 0 , 0),
        ("homework", 25, 50, 60, "resources/homework.png", 0, -10, 0, 0, 0, 0, 10)
    ),
"resources/background3.png", "resources/background3.mp3"
)

Shop.blackInstance = Shop("H3LL0, 1 4M 4 L337 H4XX0R, BUY MY STUFF M8", "TYSM!!! :) :)",
    (
        ("health potion", 100, 60, 75, "resources/health potion.png", 50, 0, 0, 0, 0, 0, 0),
        ("anti-depressant", 90, 50, 75, "resources/anti depressants.png", 0, 50, 0, 0, 0, 0, 0),
        ("ULTRA HAMBURGER", 80, 50, 75, "resources/ULTRA HAMBURGER.png", 0, 0, 50, 0, 0, 0, 0),
        ("age reversing pill", 200, 60, 60, "resources/age reversing pill.png", 0, 0, 0, -20, 0, 0, 0),
        ("botox", 110, 60, 75, "resources/botox.png", 0,0,0,0,30,0,0),
        ("steroids", 120, 60, 60, "resources/steroids.png", 0, 0, 0,0,0,30, 0),
        ("fake degree", 115, 60, 60, "resources/fake degree.png", 0, 0, 0, 0, 0, 0, 30)
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

Home.instance = Home()
Outside.instance = Outside()
Main.instance = Main()

