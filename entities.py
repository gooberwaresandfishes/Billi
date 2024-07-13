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

# class to display images  
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
        # load and size image
        self.image = pygame.image.load(self.imagePath)
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        
        self.xMove = 0
        self.yMove = 0
    
    def update(self):
        # resize image if width and height changed
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        
        # increase coordinates by move
        self.x += self.xMove
        self.y += self.yMove
    
    def render(self):
        if self.isHidden:
            return
            
        Game.instance.screen.blit(self.image, (self.x, self.y))

class ClickableImage(Image):
    
    def init(self):
        super().init()
        
        # initialise booleans
        self.isHovered = False
        self.isClicked = False
        self.isUnclicked = False
        self.isHeld = False
        
        # initialise hitbox
        self.rectangle = pygame.Rect(self.x, self.y, self.width, self.height)
        
    def update(self):
        super().update()
        
        # make sure rectangle is right size and coords
        self.rectangle = pygame.Rect(self.x, self.y, self.width, self.height)
        
        self.isHovered = self.rectangle.collidepoint(*pygame.mouse.get_pos())
        
        # to sort of unclicking
        if self.isUnclicked:
            self.isClicked = False
            self.isUnclicked = False
            
        if self.isClicked:
            self.isUnclicked = True
    
    def checkEvents(self, event):  
        
        # if mouse is pressed update clicked if hovering
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.isHeld = self.isHovered
            self.isClicked = self.isHovered
        
        # if mouse is up it is not help
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.isHeld = False           

# tip class for popups
class Tip(ClickableImage):
    
    def __init__(self, text):
        
        # split the text into lines
        self.text = text.split('\n')
        
        super().__init__(0, 0, False, 1000, 600, "resources/tip.png")
        
    def init(self):
        super().init()
        
        
            
        for i in range(len(self.text)):      
            self.text[i] = self.text[i].strip()
        
        if not self.text[0]:
            self.text.pop(0)
        
        # initialise font stuff
        pygame.font.init()
        
        self.tipTexts = globalAccess.renderMultilineFont(self.text, pygame.font.Font("resources/Cascadia Code.ttf", 17))
        
    def update(self):
        super().update()
        
        # when clicked remove
        if self.isClicked:
            Game.instance.currentState.entities.remove(self)
            
            try:
                Game.instance.currentState.tips.remove(self)
            except:
                pass
                
            return
            
    def checkEvents(self, event):
        
        # click anywhere
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

            self.isClicked = True 
    
    def render(self):
        super().render()
        
        globalAccess.blitMultilineFont(self.tipTexts, Game.instance.screen, 240, 160, 20)

         
                  
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
        
        # initialise font stuff
        pygame.font.init()

        self.statsFont = pygame.font.Font("resources/Cascadia Code.ttf", 15)
        self.nameText = pygame.font.Font("resources/Cascadia Code.ttf", 27).render(self.name, True, (0, 0, 0))
        self.timePassed = 0
        
        # text stuff
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

        # time the bubble has stayed up for
        self.bubbleTime = 0

    
    def render(self):
        super().render()
        
        # render text
        Game.instance.screen.blit(self.nameText, (self.x + 50 - len(self.name), self.y - 30))
        globalAccess.blitMultilineFont(self.statsTexts, Game.instance.screen, self.x + 30, self.y + 300, 17)
        
        # if bubble is here, render bubble
        if self.bubbleTime > 0:
            resizedImage = pygame.transform.scale(globalAccess.bubbleImage, (80 + 9 * len(self.currentSaying), 100))
            
            Game.instance.screen.blit(resizedImage, (self.x, self.y - 110))
            
            Game.instance.screen.blit(self.sayingText, (self.x + 50, self.y - 80) )
       
    def update(self):
        super().update()
        
        # if theres no health you die
        if self.health <= 0:
            
            # tell the player the cat has died
            if Game.instance.currentState == states.Home.instance:
                Game.instance.currentState.tips.append(
                    Tip(f"{self.name} has died!\ndead cats respawn outside when you enter home.")
                )
                
            else:
                Game.instance.currentState.entities.append(
                    Tip(f"{self.name} has died!\ndead cats respawn outside when you enter home.")
                )

            # remove RIP
            states.Home.instance.entities.remove(self)
            states.Home.instance.ownedCats.remove(self)
            
            # select another cat as the player if this one dies and is selected
            if states.Outside.instance.player.imagePath == self.imagePath:
                
                # if there are cats left just switch to another cat
                if states.Home.instance.ownedCats:
                    
                    states.Outside.instance.player.imagePath = states.Home.instance.ownedCats[0].imagePath
                
                # if there are no cats left show secret easter egg billi!!! O:
                else:
                    
                    states.Outside.instance.player.imagePath = "resources/icon.png"
                    
                states.Outside.instance.player.image = pygame.image.load(states.Outside.instance.player.imagePath)
        
        # time passed increases
        self.timePassed += 1
        
        # if roughly 10 minutes has passed reduce stats
        if self.timePassed > 18000:
            
            self.changeStats(0, -2, -2, 0, -1, -1, -1)
            
            # for every non-health attribute at 0 reduce health by 1
            for key, value in self.getAttributeDict().items():
                if (not key == "health") and\
                ((not(key == "hoariness") and value < 1) or (key == "hoariness" and value > 100)):
                    
                    self.changeStats(-1, 0, 0, 0, 0, 0, 0 )
            
            # reset time passed
            self.timePassed = 0
        
        # increase or reset bubble time
        self.bubbleTime = 0 if self.bubbleTime > 200 else self.bubbleTime + 1 if self.bubbleTime > 0 else 0
        
        # if cat is clicked, say the condition
        if self.isClicked:
            
            # select this cat to go outside
            states.Outside.instance.player.imagePath = self.imagePath
            
            # text stuff
            self.sayingText = self.statsFont.render(self.getCurrentSaying(), True,(0, 0, 0))
            self.bubbleTime = 1
            
            globalAccess.meow.play()
            
        # update text
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
        
        # all possible replies
        results = [sayings[key][1] for key, value in attributes.items() if key in sayings and value <= 25]
        results.extend([sayings[key][0] for key, value in attributes.items() if key in sayings and value >= 75])

        # set default saying if no results found
        self.currentSaying = random.choice(results) if results else "I'm doing good"
        
        return self.currentSaying
    
    def changeStats(self, health, happiness, hunger, hoariness, handsomeness, hardiness, headsmarts):
    
        # increase stats by value until it reaches 0
        
        self.health = int(self.health + health if self.health + health > 0 else 0)
        self.happiness = int(self.happiness + happiness if self.happiness + happiness > 0 else 0)
        self.hunger = int(self.hunger + hunger  if self.hunger + hunger > 0 else 0)
        self.hoariness = int(self.hoariness + hoariness if self.hoariness + hoariness > 0 else 0) # age
        self.handsomeness = int(self.handsomeness + handsomeness if self.handsomeness + handsomeness > 0 else 0) # charaisma
        self.hardiness = int(self.hardiness + hardiness if self.hardiness + hardiness > 0 else 0) # athleticism
        self.headsmarts = int(self.headsmarts + headsmarts if self.headsmarts + headsmarts > 0 else 0) # intelligence    
        
# item in invetory
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
        
        # if its being held allow it to be dragged
        if self.isHeld:
            # able to drag item
            self.x, self.y = pygame.mouse.get_pos()[0] - 20, pygame.mouse.get_pos()[1] - 20
            
        else:
            for cat in Game.instance.currentState.ownedCats:
            
                # if this item collides with a cat
                if self.rectangle.colliderect(cat.rectangle):
                    
                    # change the stats by the given amount
                    cat.changeStats(self.health, self.happiness, self.hunger, self.hoariness, self.handsomeness,
                        self.hardiness, self.headsmarts)
                    
                    globalAccess.nom.play()
                    
                    # remove the item
                    Game.instance.currentState.entities.remove(self)
                    Game.instance.currentState.inventory.remove(self)
                    return
            
            # affected by gravity if not in inventory
            self.yMove = 3 if self.y < 500 and self.x < 720 else 0
            
        # make sure it doesent go out the border
        
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
        
        super().__init__(x, y, False, 50,70, "resources/icon.png")
        
    def init(self):
        super().init()
        
        self.rectangle = pygame.Rect(self.x, self.y, self.width, self.height)
    
    def update(self):
        super().update()
        self.rectangle = pygame.Rect(self.x, self.y, self.width, self.height)
        
        # do not allow player to get out the map
        if self.x < 0:
            self.x = 0
        elif self.x > 1900-self.width:
            self.x =  1900-self.width
        
        if self.y < 0:
            self.y = 0
        elif self.y >  1200-self.height:
            self.y = 1200-self.height
        
        # handle collisions with barriers
        self.handleCollisions()
            
    def handleCollisions(self):
    
        # do not allow player to pass barriers
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
        
        # keyboard movement
        
        if event.type == pygame.KEYDOWN:
            
            # move in the direction based on WASD
            
            if event.key == pygame.K_w:
                self.yMove = -3
            elif event.key == pygame.K_s:
                self.yMove = 3
                
            if event.key == pygame.K_a:
                self.xMove = -3
            elif event.key == pygame.K_d:
                self.xMove = 3
        
        # if key is unpressed, stop moving in that direction
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w and self.yMove < 0:
                self.yMove = 0
            elif event.key == pygame.K_s and self.yMove > 0:
                self.yMove = 0
                
            if event.key == pygame.K_a and self.xMove < 0:
                self.xMove = 0
            elif event.key == pygame.K_d and self.xMove > 0:
                self.xMove = 0
        
        # mouse movement
        
        elif (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
            
            # get mouse position
            position = pygame.mouse.get_pos()
            
            # if mouse is pressed on a far side of the screen it will go in that direction
            self.yMove = -3 if position[1] < 200 else 3 if position[1] > 400 else 0
            self.xMove = -3 if position[0] < 400 else 3 if position[0] > 600 else 0
        
        # if mouse is unpressed stop moving
        elif event.type == pygame.MOUSEBUTTONUP  and event.button == 1:
            self.xMove = 0
            self.yMove = 0      
    
    def render(self):
        if self.isHidden:
            return
        
        # always render in the middle of the screen
        Game.instance.screen.blit(self.image, (500-self.width/2, 300-self.height/2))

# image that moves with player   
class RoamImage(Image):
    
    def render(self, x, y):
        if self.isHidden:
            return
        
        # render with adjust for offset
        Game.instance.screen.blit(self.image, (self.x - x, self.y - y))

# barrier to stop player passing
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
        
        #  if colliding with player, transport player to the building
        if self.rectangle.colliderect(Game.instance.currentState.player.rectangle):
        
            # move player away from door
            Game.instance.currentState.player.y -= 8*Game.instance.currentState.player.yMove
            
            # make player still
            Game.instance.currentState.player.xMove = 0
            Game.instance.currentState.player.yMove = 0    
            
            # switch state
            Game.instance.currentState = self.state
            Game.instance.currentState.onSwitch()

# cat to be collected  
class Collectible(RoamImage):

    def __init__(self, x, y, cat):
        self.cat = cat
        
        super().__init__(x, y, False, 60, 80, cat[1])
        
    def init(self):
        super().init()
        
        self.rectangle = pygame.Rect(self.x, self.y, self.width, self.height)
        
        self.xMove = 0
        self.yMove = 0
    
    def update(self):
        super().update()
        
        # remove from map if player already owns cat
        for cat in states.Home.ownedCats:
            if self.cat[0] == cat.name:
                Game.instance.currentState.entities.remove(self)
                return
        
        
        # if somehow cats are full remove self
        
        if len(states.Home.instance.ownedCats) > 2:
            Game.instance.currentState.entities.remove(self)
            return
        
        self.rectangle = pygame.Rect(self.x, self.y, self.width, self.height)
        
        self.x += self.xMove
        self.y += self.yMove
        
        # if there is a collision add to inventory and remove from map
        if self.rectangle.colliderect(Game.instance.currentState.player.rectangle):
            
            # gett all possible positions and remove the taken ones
            catPositions = [150, 350, 550]
            
            for cat in states.Home.instance.ownedCats:
                catPositions.remove(cat.x)
                 
            states.Home.instance.ownedCats.append(Cat(random.choice(catPositions), 175,*self.cat))
            Game.instance.currentState.entities.remove(self)
            
            Game.instance.currentState.entities.append(
                Tip(f"you got {states.Home.instance.ownedCats[-1].name}!\n meet him at home!")
            )
            