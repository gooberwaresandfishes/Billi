import pygame
import random
from game import Game
import globalAccess
import states

# abstract base class (unneccessary in python but i want to do it like this because im used to java)
class Entity():
    
    def __init__(self):        
        self.init()
    
    def init(self):
        pass
    
    def update(self):
        pass
    
    def render(self):
        pass
        
    def checkEvents(self, event):
        pass
        
class Image(Entity):
    
    def __init__(self, x, y, isHidden, width, height, imagePath):
        
        self.x = x
        self.y = y
        self.isHidden = isHidden
        self.width = width
        self.height = height
        self.imagePath = imagePath
        
        super().__init__()
        
    def init(self):
        self.image = pygame.image.load(self.imagePath)
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        
        self.xMove = 0
        self.yMove = 0
    
    def update(self):
        
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        
        self.x += self.xMove
        self.y += self.yMove
    
    def render(self):
        if self.isHidden:
            return
            
        Game.instance.screen.blit(self.image, (self.x, self.y))

class ClickableImage(Image):
    
    def init(self):
        super().init()
        
        self.isHovered = False
        self.isClicked = False
        self.isUnclicked = False
        self.isHeld = False
        
        self.rectangle = pygame.Rect(self.x, self.y, self.width, self.height)
        
    def update(self):
        super().update()
        
        if self.isUnclicked:
            self.isClicked = False
            self.isUnclicked = False
            
        if self.isClicked:

            self.isUnclicked = True
            
        self.rectangle = pygame.Rect(self.x, self.y, self.width, self.height)

    
    def render(self):
        super().render()
        # to draw hitboxes
        #pygame.draw.rect(Game.instance.screen, (255, 0, 0), self.rectangle, 2)
    
    def checkEvents(self, event):
        
        # make this better later
        if event.type == pygame.MOUSEMOTION:
            self.isHovered = self.rectangle.collidepoint(*pygame.mouse.get_pos())
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

            self.isHeld = self.isHovered
            self.isClicked = self.isHovered
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.isHeld = False           

class Tip(ClickableImage):
    
    hasOccured = []
    
    def __init__(self, name, text, occursOnce):
        
        self.name = name
        self.text = text.split('\n')
        self.occursOnce = occursOnce
        
        super().__init__(0, 0, False, 1000, 600, "resources/tip.png")
        
    def init(self):
        super().init()
        
        
        
        Tip.hasOccured.append(self.name)
        
        pygame.font.init()
        
        self.tipTexts = globalAccess.renderMultilineFont(self.text, pygame.font.Font("resources/Cascadia Code.ttf", 17))
        
    def update(self):
        super().update()
        
        # if it has occured and can only occur once delete
        if self.name in self.hasOccured and self.occursOnce:
            Game.instance.currentState.entities.remove(self)
            try:
                Game.instance.currentState.tips.remove(self)
            except:
                pass
            return
        
        if self.isClicked:
            Game.instance.currentState.entities.remove(self)
            try:
                Game.instance.currentState.tips.remove(self)
            except:
                pass
            return
            
    def checkEvents(self, event):
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

            self.isClicked = True 
    
    def render(self):
        super().render()
        
        if Game.instance.currentState == states.Home.instance:
            globalAccess.blitMultilineFont(self.tipTexts, Game.instance.screen, 120, 160, 12)
        else:
            globalAccess.blitMultilineFont(self.tipTexts, Game.instance.screen, 240, 160, 12)

         
                  
# i was gonna split this into a giant hierarchy of entities but then i realised i should take advantage of python being
# dynamic, otherwise i might aswell have used java
class Cat(ClickableImage):
    
    def __init__(self, x, y, name, imagePath,
    health, happiness, hunger, hoariness, handsomeness, hardiness, headsmarts, sayings):
        
       
        
        # name
        self.name = name

        # physical stats
        self.health = health
        self.happiness = happiness
        self.hunger = hunger
        self.hoariness = hoariness # age
        
        # skill stats
        self.handsomeness = handsomeness # charaisma
        self.hardiness = hardiness # athleticism
        self.headsmarts = headsmarts # intelligence
        
        self.sayings = sayings
       
        
        super().__init__(x, y, False, 200, 300, imagePath)
    
    def init(self):
        super().init()
        pygame.font.init()

        self.statsFont = pygame.font.Font("resources/Cascadia Code.ttf", 15)
        self.nameText = pygame.font.Font("resources/Cascadia Code.ttf", 27).render(self.name, True, (0, 0, 0))
        self.timePassed = 0
        
        self.statsTexts = globalAccess.renderMultilineFont((
            f"HEALTH: {self.health}",
            f"HAPPINESS: {self.happiness}",
            f"HUNGER: {self.hunger}",
            f"HOARINESS: {self.hoariness}",
            f"HANDSOMENESS: {self.handsomeness}",
            f"HARDINESS: {self.hardiness}",
            f"HEADSMARTS: {self.headsmarts}"

        ), self.statsFont)
        
        self.sayingText = self.statsFont.render(self.getCurrentSaying(), True,(0, 0, 0))

        
        self.bubbleTime = 0

    
    def render(self):
        super().render()
        
        Game.instance.screen.blit(self.nameText, (self.x + 50 - len(self.name), self.y - 30))
        globalAccess.blitMultilineFont(self.statsTexts, Game.instance.screen, self.x + 30, self.y + 300, 17)
        
        if self.bubbleTime > 0:
            resizedImage = pygame.transform.scale(globalAccess.bubbleImage, (80 + 9*len(self.currentSaying), 100) )
            
            Game.instance.screen.blit(resizedImage, (self.x + 200, self.y - 30))
            
            Game.instance.screen.blit(self.sayingText, (self.x + 250, self.y) )
       
    def update(self):
        super().update()
        
        if self.health <= 0:
            states.Home.instance.entities.remove(self)
            states.Home.instance.ownedCats.remove(self)
        
        self.timePassed += 1
        
        if self.timePassed > 36000:
            self.changeStats(0, -2, -2, 0, -1, -1, -1)
            
            for key, value in self.getAttributeDict().items():
                if not(key == "health") and value < 1:
                    self.changeStats(-1, 0, 0, 0, 0, 0, 0 )
            
            
            self.timePassed = 0
        
        if self.bubbleTime > 200:
            self.bubbleTime = 0
        elif self.bubbleTime > 0:
            self.bubbleTime += 1
        
        if self.isClicked:
            states.Outside.instance.player.imagePath = self.imagePath
            self.sayingText = self.statsFont.render(self.getCurrentSaying(), True,(0, 0, 0))
            self.bubbleTime = 1
            
            globalAccess.meow.play()
            
        self.statsTexts = globalAccess.renderMultilineFont((
            f"HEALTH: {self.health}",
            f"HAPPINESS: {self.happiness}",
            f"HUNGER: {self.hunger}",
            f"HOARINESS: {self.hoariness}",
            f"HANDSOMENESS: {self.handsomeness}",
            f"HARDINESS: {self.hardiness}",
            f"HEADSMARTS: {self.headsmarts}"

        ), self.statsFont)
     
    def getAttributeDict(self):
        # return a dictionary of attributes
        return {
            "health": self.health,
            "happiness": self.happiness,
            "hunger": self.hunger,
            "hoariness": self.hoariness,
            "handsomeness": self.handsomeness,
            "hardiness": self.hardiness,
            'headsmarts': self.headsmarts
        }

    def getCurrentSaying(self):
        attributes = self.getAttributeDict()
        sayings = self.sayings
        results = []
        for key, value in attributes.items():
            if key in sayings:
                if value <= 25:
                    results.append(sayings[key][1])
                elif value >= 75:
                    results.append(sayings[key][0])
        
        # if there are no results return average saying
        self.currentSaying = "im doing good" if not results else random.choice(results)
        return self.currentSaying
    
    def changeStats(self, health, happiness, hunger, hoariness, handsomeness, hardiness, headsmarts):
        # physical stats
        self.health = int(self.health + health if self.health + health > 0 else 0)
        self.happiness = int(self.happiness + happiness if self.happiness + happiness > 0 else 0)
        self.hunger = int(self.hunger + hunger  if self.hunger + hunger > 0 else 0)
        self.hoariness = int(self.hoariness + hoariness if self.hoariness + hoariness > 0 else 0) # age
                    
        # skill stats
        self.handsomeness = int(self.handsomeness + handsomeness if self.handsomeness + handsomeness > 0 else 0) # charaisma
        self.hardiness = int(self.hardiness + hardiness if self.hardiness + hardiness > 0 else 0) # athleticism
        self.headsmarts = int(self.headsmarts + headsmarts if self.headsmarts + headsmarts > 0 else 0) # intelligence
        
        

class Item(ClickableImage):
    
    def __init__(self, name, price, width, height, imagePath,
    health, happiness, hunger, hoariness, handsomeness, hardiness, headsmarts):
        super().__init__(random.randint(800, 1000-width), random.randint(100, 550-height), False, width, height, imagePath)
        
        self.name = name
        self.price = price
        
        # physical stats
        self.health = health
        self.happiness = happiness
        self.hunger = hunger
        self.hoariness = hoariness # age
        
        # skill stats
        self.handsomeness = handsomeness # charaisma
        self.hardiness = hardiness # athleticism
        self.headsmarts = headsmarts # intelligence
        
    
    def update(self):
        super().update()
        
        if self.isHeld:
            # able to drag item
            self.x, self.y = pygame.mouse.get_pos()[0] - 20, pygame.mouse.get_pos()[1] - 20
        else:
            for entity in Game.instance.currentState.entities:
            
                # if item collides with a cat
                if isinstance(entity, Cat) and self.rectangle.colliderect(entity.rectangle):
                
                    entity.changeStats(self.health, self.happiness, self.hunger, self. hoariness, self.handsomeness,
                        self.hardiness, self.headsmarts)
                    
                    globalAccess.nom.play()
                    
                    # remove the item
                    Game.instance.currentState.entities.remove(self)
                    Game.instance.currentState.inventory.remove(self)
                    return
            
            self.yMove = 3 if self.y < 500 and self.x < 720 else 0
            
            
        if self.x < 0:
            self.x = 0
        elif self.x > 1000-self.width:
            self.x = 1000-self.width
        
        if self.y < 0:
            self.y = 0
        elif self.y > 600-self.height:
            self.y = 600-self.height
        
class Player(Image):
    
    def __init__(self, x, y):
        
        super().__init__(x, y, False, 50,70, "resources/cat1.png")
        
    def init(self):
        super().init()
        
        self.rectangle = pygame.Rect(self.x, self.y, self.width, self.height)
    
    def update(self):
        super().update()
        self.rectangle = pygame.Rect(self.x, self.y, self.width, self.height)
        
        if self.x < 0:
            self.x = 0
        elif self.x > 1900-self.width:
            self.x =  1900-self.width
        
        if self.y < 0:
            self.y = 0
        elif self.y >  1200-self.height:
            self.y = 1200-self.height
           
        self.handleCollisions()
            
    def handleCollisions(self):
        for entity in Game.instance.currentState.entities:
            if isinstance(entity, Barrier):
                
                if pygame.Rect(self.x, self.y - self.yMove, self.width, self.height).colliderect(entity.rectangle):
                    if self.xMove > 0:  # moving right
                        self.x = entity.rectangle.left - self.width
                    elif self.xMove < 0:  # moving left
                        self.x = entity.rectangle.right
                
                if pygame.Rect(self.x - self.xMove, self.y, self.width, self.height).colliderect(entity.rectangle):                
                    if self.yMove > 0:  # moving down
                        self.y = entity.rectangle.top - self.height
                    elif self.yMove < 0:  # moving up
                        self.y = entity.rectangle.bottom
    
    def checkEvents(self, event):
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                self.yMove = -3
            elif event.key == pygame.K_s:
                self.yMove = 3
            elif event.key == pygame.K_a:
                self.xMove = -3
            elif event.key == pygame.K_d:
                self.xMove = 3
        
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w and self.yMove < 0:
                self.yMove = 0
            elif event.key == pygame.K_s and self.yMove > 0:
                self.yMove = 0
            elif event.key == pygame.K_a and self.xMove < 0:
                self.xMove = 0
            elif event.key == pygame.K_d and self.xMove > 0:
                self.xMove = 0
    
    def render(self):
        if self.isHidden:
            return
            
        Game.instance.screen.blit(self.image, (500-self.width/2, 300-self.height/2))
        
class RoamImage(Image):
    
    def render(self, x, y):
        if self.isHidden:
            return
            
        Game.instance.screen.blit(self.image, (self.x - x, self.y - y))

class Barrier(Entity):
    
    def __init__(self, x, y, width, height):
        
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
        super().__init__()
        
    def init(self):
        self.rectangle = pygame.Rect(self.x, self.y, self.width, self.height)
        self.xMove = 0
        self.yMove = 0
    
    def update(self):
        self.rectangle = pygame.Rect(self.x, self.y, self.width, self.height)
        self.x += self.xMove
        self.y += self.yMove
    
    def render(self, x, y):
        # to draw hitboxes
        #renderedRectangle = pygame.Rect(self.x-x, self.y-y, self.width, self.height)
        
        #pygame.draw.rect(Game.instance.screen, (0, 0, 255), renderedRectangle, 2)]
        pass


        
class Door(Entity):
    def __init__(self, x, y, width, height, state):
        
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.state = state
        
        super().__init__()
        
    def init(self):
        self.rectangle = pygame.Rect(self.x, self.y, self.width, self.height)
        self.xMove = 0
        self.yMove = 0
        
      
    
    def update(self):
        self.rectangle = pygame.Rect(self.x, self.y, self.width, self.height)
        self.x += self.xMove
        self.y += self.yMove
        
        if self.rectangle.colliderect(Game.instance.currentState.player.rectangle):
            Game.instance.currentState.player.y -= 8*Game.instance.currentState.player.yMove
            Game.instance.currentState.player.xMove = 0
            Game.instance.currentState.player.yMove = 0    
            
            Game.instance.currentState = self.state

            # run state 
            Game.instance.currentState.onSwitch()
    
    def render(self, x, y):
        # to draw hitboxes
        #renderedRectangle = pygame.Rect(self.x-x, self.y-y, self.width, self.height)
        
        #pygame.draw.rect(Game.instance.screen, (0, 0, 255), renderedRectangle, 2)]
        pass
        
class Collectible(RoamImage):
    def __init__(self, x, y, cat):
        self.cat = cat
        
        super().__init__(x, y, False, 60, 80, cat[1])
        
    def init(self):
        super().init()
        self.rectangle = pygame.Rect(self.x, self.y, self.width, self.height)
        self.xMove = 0
        self.yMove = 0
        
        for cat in states.Home.ownedCats:
            if self.cat[0] == cat.name:
                Game.instance.currentState.entities.remove(self)
    
    def update(self):
        super().update()
        
        self.rectangle = pygame.Rect(self.x, self.y, self.width, self.height)
        self.x += self.xMove
        self.y += self.yMove
        
        if self.rectangle.colliderect(Game.instance.currentState.player.rectangle):
        
            states.Home.instance.ownedCats.append(Cat(150 + 200*len(states.Home.instance.ownedCats), 175,*self.cat))
            Game.instance.currentState.entities.remove(self)
            