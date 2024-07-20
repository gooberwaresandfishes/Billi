import pygame
import entities
import states
import gif_pygame

# save
saveDict = {}

# money
money = 0

# cats stats
cats = [
("RICHARD", "resources/cat1.png", 50, 50, 50, 0, 10, 10, 10,
    {
        "health" : ("wow i feeel so helty!", "im boutta die bruh"),
        "happiness": ("im so exited", "i think im depressed"),
        "hunger": ("im so full!", "im so hungry i could eat a horse"),
        "hoariness": ("damn im old", "im so young!"),
        "handsomeness":("this bowtie lookin good", "i wish i had a bowtie to look more snazzy"),
        "hardiness":("im ready to run a marathon", "im quite unfit"),
        "headsmarts": ("my brian is so beeeg", "i failed my last test")
    }
),
("GERALD", "resources/cat2.png", 60, 40, 50, 5, 10, 20, 5,
    {
        "health" : ("oh, im very healthy", "oh, im about to die"),
        "happiness": ("oh, im so happy", "oh, im depressed"),
        "hunger": ("oh, im very full", "oh, im starving"),
        "hoariness": ("oh, im old", "oh, im young"),
        "handsomeness":("oh, im handsome", "oh, im not very handsome"),
        "hardiness":("oh, im strong", "oh, im weak"),
        "headsmarts": ("oh, im smart", "oh, im dumb")
    }
),
("TIMOTHY", "resources/cat3.png", 40, 60, 40, 0, 20, 10, 5,
    {
        "health" : ("wwwoowiie so health!", "i can see the light"),
        "happiness": ("yippeeee im so happy!", "im very sad today"),
        "hunger": ("i am not hungry anymore!", "is there a famine going on?"),
        "hoariness": ("im old somehow", "im just a kid!"),
        "handsomeness":("im lookin good :3", "damn im ugly"),
        "hardiness":("i am speedy", "i am frail"),
        "headsmarts": ("im so snart i kno everything", "i forgot maffs")
    }
)
]

# resources 
bubbleImage = pygame.image.load("resources/bubble.png")
seaImage = gif_pygame.load("resources/sea.gif")

# sounds
pygame.mixer.init()
meow = pygame.mixer.Sound("resources/meow.mp3")
kaching = pygame.mixer.Sound("resources/money.mp3")
nom = pygame.mixer.Sound("resources/nom.mp3")
womp = pygame.mixer.Sound("resources/womp.mp3")
crash = pygame.mixer.Sound("resources/car.mp3")

# useful functions
def renderMultilineFont(text, font):
    rendered = []
    for line in text:
        rendered.append(font.render(line, True, (0, 0, 0)))
    
    return rendered

def blitMultilineFont(rendered, screen, x, y, gap):
    distance = 0
    for text in rendered: 
        screen.blit(text, (x, y + distance))
        distance += gap
        
# tips
tips = [
    entities.Tip(
        '''
        Welcome to Billi!
        '''
    ),
    entities.Tip(
        '''
        HOW TO PLAY:
        - Your objective is to take care of your cats.
        - Feed them items to maintain their stats.
        - Buy items from shops using money.
        - Pick up collectibles around the map
        - Earn money by working in buildings.
        '''
    ),
    entities.Tip(
        '''
        CATS:
        - You start with 1 cat.
        - There are 2 more to find, scattered in the maze
        - Cat's stats decrease over time.
        - Hoariness means age and instead increases over time
        - When you exit or time travel, your cats sleep
        - When cats sleep they lose stats slower.
        - Low stats lead to health damage (or high hoariness)
        - Sleeping cats avoid health damage
        - If a cat reaches 0 health it dies
        - dead cats respawn outside or in the maze
        - Click a cat to check its condition.
        '''
    ),
    entities.Tip(
        '''
        ITEMS:
        - Items boost your cat's stats.
        - Drag items onto a cat to feed them.
        '''
    ),
    entities.Tip(
        '''
        SHOPS:
        - There are 4 shops in the map (2 in the alley).
        - Visit shops to purchase items.
        - Simply walk into a shop and buy.
        '''
    ),
    entities.Tip(
        '''
        WORK:
        - There are 3 buildings on the map.
        - Enter buildings to work or use services.
        - Using upgrades skills
        - Working earns money based on skills.
        - Any action is available once daily.
        '''
    ),
    entities.Tip(
        '''
        WORLD:
        - Click a door to exit the house.
        - Click a cat to accompany you before leaving.
        - Use WASD to move or press on sides of the screen.
        - Enter buildings through black doors.
        '''
    ),
    entities.Tip(
        '''
        PRACTICE:
        - Click the arrow button in the corner switch rooms.
        - The room next to you is the practice room
        - Here you can increase the stats of your cats.
        - You can click and upgrade to reduce clicks required.
        '''
    ),
    entities.Tip(
        '''
        MAZE:
        - A maze is located following the road to the right
        - It contains many items and collectibles such as...
        - Cats, clocks (to skip time forward), items
        - there is also a ghost that will chase and do damage
        '''
    ),
    entities.Tip(
        '''
        SAVE:
        - Press 'Esc' or EXIT at home to exit the game.
        - Press 'F' or SAVE at home save your progress.
        - Press LOAD in the main menu to load your save.
        '''
    ),
    entities.Tip(
        '''
        IMPORTANT:
        - MAKE SURE TO EXIT THE GAME OR STATS WILL DRAIN.
        - MAKE SURE TO SAVE BEFORE EXITING.
        - Have fun exploring Billi!
        '''
    )
]

from PIL import Image

def convert_image_to_2d_array(image_path):
    # Load the image
    image = Image.open(image_path)

    # Convert the image to grayscale
    image = image.convert('L')

    # Get image dimensions
    width, height = image.size

    # Convert to 1s and 0s
    binary_image = []
    for x in range(height):
        row = []
        for y in range(width):
            pixel = image.getpixel((x, y))
            # Assuming 0 is black and 255 is white
            row.append(1 if pixel == 0 else 0)
        binary_image.append(row)
        
    return binary_image