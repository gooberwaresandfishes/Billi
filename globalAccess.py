import pygame
import entities
import states

#  health, happiness, hunger, hoariness, handsomeness, hardiness, headsmarts, sayings):

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

bubbleImage = pygame.image.load("resources/bubble.png")

money=0
pygame.mixer.init()
meow = pygame.mixer.Sound("resources/meow.mp3")
kaching = pygame.mixer.Sound("resources/money.mp3")
nom = pygame.mixer.Sound("resources/nom.mp3")
womp = pygame.mixer.Sound("resources/womp.mp3")

saveDict = {}