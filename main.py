# Load the previous gaming session if this game was played before.
disk = ""
with open("blackjackDisk.txt", mode ="r", encoding ="utf-8") as ls:
    disk = ls.read()

import pygame, random, sys

# Menu logic, splashes, and button input/detection/sounds by Parker Davison
# Blackjack core logic and incorporation to pygame by Sahir Samnani
# Background graphics in user interface and assets by Elias Mohamadi
# Music, card textures, notes, and saving/loading by Rori Lidell

allCards = ["ace of hearts", "king of hearts", "queen of hearts", "jack of hearts", "2 of hearts", "3 of hearts", "4 of hearts", "5 of hearts", "6 of hearts", "7 of hearts", "8 of hearts", "9 of hearts", "10 of hearts", "ace of clubs", "king of clubs", "queen of clubs", "jack of clubs", "2 of clubs", "3 of clubs", "4 of clubs", "5 of clubs", "6 of clubs", "7 of clubs", "8 of clubs", "9 of clubs", "10 of clubs", "ace of diamonds", "king of diamonds", "queen of diamonds", "jack of diamonds", "2 of diamonds", "3 of diamonds", "4 of diamonds", "5 of diamonds", "6 of diamonds", "7 of diamonds", "8 of diamonds", "9 of diamonds", "10 of diamonds", "ace of spades", "king of spades", "queen of spades", "jack of spades", "2 of spades", "3 of spades", "4 of spades", "5 of spades", "6 of spades", "7 of spades", "8 of spades", "9 of spades", "10 of spades"]
def cardValue(value):
    if value[0] == "a":
        return 11
    elif value[0] == "j" or value[0] == "q" or value[0] == "k":
        return 10
    elif value[0] == "1":
        return 10
    else:
        return int(value[0])

# Get Splash Text
lines = ""
with open("splashes.txt", mode="r", encoding="utf-8") as f:
    lines = [line.rstrip() for line in f] # stack overflow the goat
splashNumber = random.randint(0, len(lines) - 1)

'''
GAMESTATE = 0 (MENU)
GAMESTATE = 1 (HELP)
GAMESTATE = 2 (CREDITS)
GAMESTATE = 3 (INPUT INVESTMENT)
GAMESTATE = 4 (GAME)
GAMESTATE = 5 (GAME OVER (CANNOT MEET MINIMUM INVESTMENT REQUIREMENT))
'''

GAMESTATE = 0

# Money variables
if disk == "":
    gameMoney = 200.00
else:
    gameMoney = float(disk)
bidAmount = 0.00
minimumBid = 100.00

# Graphical representations
MENU_MONEY = "Bank Balance: $" + str(gameMoney) + "0"
BID_MONEY = "$" + str(bidAmount) + "0"

# Initialize pygame
pygame.init()
clock = pygame.time.Clock()

# Sounds
buttonSound = pygame.mixer.Sound("buttonSound.mp3")
buttonFailure = pygame.mixer.Sound("buttonFailure.mp3")

# Music
pygame.mixer.music.load("blackjackmusic.mp3")
pygame.mixer.music.play(-1)

# Screen dimensions
sizex = 1280
sizey = 720
importSurf = pygame.image.load("aceofhearts.png")
icon = pygame.transform.scale(importSurf, (120, 120))
screen = pygame.display.set_mode((sizex, sizey))

pygame.display.set_caption("Blackjack")
pygame.display.set_icon(icon)

# Establish game as running (default color for unassigned GAMESTATE)
running = True
screen.fill((70, 44, 20))

backHelpButton = pygame.image.load("backHelpButtonIdle.png").convert()
backHelpButtonRect = backHelpButton.get_rect(topleft = (500, 580))
backHelpButtonRect = backHelpButtonRect.move(-5000, 0)

plusButton = pygame.image.load("plusButtonIdle.png")
plusButtonRect = plusButton.get_rect(topleft = (380, 445))

minusButton = pygame.image.load("minusButtonIdle.png")
minusButtonRect = minusButton.get_rect(topleft = (810, 445))

gambleButton = pygame.image.load("gambleButtonIdle.png")
gambleButtonRect = gambleButton.get_rect(topleft = (500, 440))

hitButton = pygame.image.load("hitButtonIdle.png")
hitButtonRect = hitButton.get_rect(topleft = (810, 342))

standButton = pygame.image.load("standButtonIdle.png")
standButtonRect = standButton.get_rect(topleft = (160, 342))

maxButton = pygame.image.load("maxButtonIdle.png")
maxButtonRect = maxButton.get_rect(topleft = (180, 450))

minButton = pygame.image.load("minButtonIdle.png")
minButtonRect = minButton.get_rect(topleft = (920, 450))

backgroundImageImport = pygame.image.load("betterblackJackBG.png")
backgroundImage = pygame.transform.scale(backgroundImageImport, (1280, 720))
backgroundImageImportClone = pygame.image.load("betterblackJackBG.png").convert_alpha()
backgroundImageClone = pygame.transform.scale(backgroundImageImportClone, (1280, 720))

loseScreenImport = pygame.image.load("ambition.png")
loseScreen = pygame.transform.scale(loseScreenImport, (1280, 720))

playScreenImport = pygame.image.load("playScreen.png")
playScreen = pygame.transform.scale(playScreenImport, (1280, 720))

splashFont = pygame.font.Font(None, 40)
splashText = splashFont.render(str(lines[splashNumber]), True, (255, 255, 0))

balanceFont = pygame.font.Font(None, 69)
balanceText = balanceFont.render(str(MENU_MONEY), True, (255, 255, 255))

# Variables created to make the game function
firstTime = 1
hit = 0
hitCount = 2
stand = 0
dealerPlay = 0
hitOrStand = ""
reveal = 0
dealerHitCount = 2
addMinimum = 1
transportBack = 0
y = 1
x = 4

while running:
    if gameMoney >= 10 ** x:
        y += 1
        x += 1
        minimumBid = minimumBid * 10.00
    # Menu
    if GAMESTATE == 0:
        backHelpButtonRect = backHelpButton.get_rect(topleft=(-5000, 580))
        screen.blit(backgroundImage, (0, 0))
        screen.blit(backgroundImageClone, (0, 0))
        balanceText = balanceFont.render(str(MENU_MONEY), True, (255, 255, 255))
        titleSurf = pygame.image.load("blackjacklogo.png").convert_alpha()
        playButton = pygame.image.load("playButtonIdle.png").convert()
        helpButton = pygame.image.load("helpButtonIdle.png").convert()
        creditButton = pygame.image.load("creditsButtonIdle.png").convert()
        playButtonRect = playButton.get_rect(topleft = (500, 300))
        helpButtonRect = helpButton.get_rect(topleft = (190, 305))
        creditButtonRect = creditButton.get_rect(topleft = (820, 305))
        screen.blit(splashText, (200, 210))
        screen.blit(playButton, (playButtonRect.x, playButtonRect.y))
        screen.blit(helpButton, (helpButtonRect.x, helpButtonRect.y))
        screen.blit(creditButton, (creditButtonRect.x, creditButtonRect.y))
        screen.blit(balanceText, (helpButtonRect.x, 600))
        screen.blit(titleSurf, (320, 10))
    # Help Menu
    if GAMESTATE == 1:
        backHelpButtonRect = backHelpButton.get_rect(topleft = (500, 580))
        screen.blit(backgroundImage, (0, 0))
        screen.blit(backgroundImageClone, (0, 0))
        helpHeaderFont = pygame.font.Font(None, 70)
        helpHeaderSurf = helpHeaderFont.render("How To Blackjack", True, (255, 255, 255))
        helpTextFont = pygame.font.Font(None, 21)
        helpTextSurf1 = helpTextFont.render("• Blackjack is an easy card game that's played between a player and a dealer.", True, (255, 255, 255))
        helpTextSurf2 = helpTextFont.render("• The player and the dealer start with two cards each. Each card has a value equal to its number.", True, (255, 255, 255))
        helpTextSurf3 = helpTextFont.render("• Face cards (,if Kings, Queens, or Jacks,) are worth 10 and Aces are worth either 1 or 11 (whichever makes the hand better).", True, (255, 255, 255))
        helpTextSurf4 = helpTextFont.render("• The player will build their hand by hitting to add cards to their hand or standing when their hand wants ot be kept.", True, (255, 255, 255))
        helpTextSurf5 = helpTextFont.render("• The goal of the player is to create a hand with a total value at or near 21.", True, (255, 255, 255))
        helpTextSurf6 = helpTextFont.render('• If the player has a hand that exceeds a value of 21, the player "busts" and automatically loses their bet, or "investment".', True, (255, 255, 255))
        helpTextSurf7 = helpTextFont.render("• After the player stands, the dealer will add cards to their deck until their hand equals or ", True, (255, 255, 255))
        helpTextSurf8 = helpTextFont.render("      - exceeds a value of 17. If the dealer's hand is higher, then the dealer wins. (The dealer can also bust.)", True, (255, 255, 255))
        helpTextSurf9 = helpTextFont.render("• There is a minimum amount that the player must bet (or invest) before starting a game round. If they cannot meet the minimum, then the game will end.", True, (255, 255, 255))
        helpTextSurf10 = helpTextFont.render("Once a game round finishes, press the SPACE key to invest again!", True, (255, 0, 0))
        helpTextSurf11 = helpTextFont.render('• In this "Blackjack" game, the options to split, double down, and buy insurance have been removed for a beginner-friendly-investment experience.', True, (255, 255, 255))
        helpTextSurf12 = helpTextFont.render("If the minimum bet (investment) can't be met, then press the delete key to restore your bank balance and start over! (minimum bet can increase as bank balance increases)", True, (255, 0, 0))
        helpTextSurf13 = helpTextFont.render("Press the esc key to quit Blackjack...", True, (255, 0, 0))
        screen.blit(helpHeaderSurf, (80, 40))
        screen.blit(helpTextSurf1, (40, 100))
        screen.blit(helpTextSurf2, (40, 140))
        screen.blit(helpTextSurf3, (40, 180))
        screen.blit(helpTextSurf4, (40, 220))
        screen.blit(helpTextSurf5, (40, 260))
        screen.blit(helpTextSurf6, (40, 300))
        screen.blit(helpTextSurf7, (40, 340))
        screen.blit(helpTextSurf8, (40, 380))
        screen.blit(helpTextSurf9, (40, 420))
        screen.blit(helpTextSurf10, (40, 510))
        screen.blit(helpTextSurf11, (40, 460))
        screen.blit(helpTextSurf12, (40, 530))
        screen.blit(helpTextSurf13, (40, 550))
        screen.blit(backHelpButton, (backHelpButtonRect.x, backHelpButtonRect.y))
    # Credits
    if GAMESTATE == 2:
        backHelpButtonRect = backHelpButton.get_rect(topleft = (500, 580))
        screen.blit(backgroundImage, (0, 0))
        screen.blit(backgroundImageClone, (0, 0))
        creditFont = pygame.font.Font(None, 40)
        pCreditHeader = creditFont.render("Parker Davison: Menu Logic, Button Input/Detection/Sounds, Graphics, and Splashes", True, (255, 255, 255))
        rCreditHeader = creditFont.render("Rori Liddell: Card Textures, Music, Notes, and Saving/Loading", True, (255, 255, 255))
        eCreditHeader = creditFont.render("Elias Mohamadi: Background Graphics In User Interface and Assets", True, (255, 255, 255))
        sCreditHeader = creditFont.render("Sahir Samnani: All Game Logic, Multipliers, and Lore", True, (255, 255, 255))
        screen.blit(pCreditHeader, (50, 100))
        screen.blit(rCreditHeader, (50, 225))
        screen.blit(eCreditHeader, (50, 350))
        screen.blit(sCreditHeader, (50, 475))
    # Money Input Screen
    if GAMESTATE == 3:
        backHelpButtonRect = backHelpButton.get_rect(topleft = (500, 580))
        screen.blit(backgroundImage, (0, 0))
        moneyFont = pygame.font.Font(None, 87)
        bidText = moneyFont.render("Enter Amount To Invest (MIN $" + str(minimumBid) + "0)", True, (255, 255, 255))
        moneyText = moneyFont.render(str(BID_MONEY), True, (255, 255, 255))
        moneyWidth = moneyText.get_width()
        moneyHeight = moneyText.get_height()
        screen.blit(bidText, (110, 60))
        screen.blit(moneyText, (((sizex / 2) - (moneyWidth / 2)), ((sizey / 2) - (moneyHeight / 2)) + 25))
        screen.blit(backHelpButton, (backHelpButtonRect.x, backHelpButtonRect.y))
        screen.blit(plusButton, (plusButtonRect.x, plusButtonRect.y))
        screen.blit(minusButton, (minusButtonRect.x, minusButtonRect.y))
        screen.blit(gambleButton, (gambleButtonRect.x, gambleButtonRect.y))
        screen.blit(maxButton, (maxButtonRect.x, maxButtonRect.y))
        screen.blit(minButton, (minButtonRect.x, minButtonRect.y))
        dealerDialogue1 = pygame.Surface((1137, 200))
        dealerDialogue1.fill(color = (0, 0, 0))
        backgroundImage.blit(dealerDialogue1, (75, 137))
        dealerFont = pygame.font.Font(None, 26)
        dealerText1 = dealerFont.render("Your starting bank balance is $" + str(gameMoney) + "0.", True, (0, 255, 0))
        backgroundImage.blit(dealerText1, (85, 175))
        dealerText2 = dealerFont.render("Hello! Are you ready to start your investing journey in Blackjack?", True, (0, 255, 0))
        backgroundImage.blit(dealerText2, (85, 200))
        dealerText3 = dealerFont.render("Great! You're about to embark on a journey toward exceeding financial abundance.", True,(0, 255, 0))
        backgroundImage.blit(dealerText3, (85, 225))
        dealerText4 = dealerFont.render("My name is Robbert, and I am the dealer here.", True, (0, 255, 0))
        backgroundImage.blit(dealerText4, (85, 250))
        dealerText5 = dealerFont.render("Let's start investing! The minimum deposit is $" + str(minimumBid) + "0. You have the potential to double your money plus receive a blackjack bonus!", True, (0, 255, 0))
        backgroundImage.blit(dealerText5, (85, 275))
        dealerText6 = dealerFont.render("Use the + and - buttons to set the value of your investment.", True, (0, 255, 0))
        backgroundImage.blit(dealerText6, (85, 300))
    # Actual game
    if GAMESTATE == 4:
        scoreBoardFont = pygame.font.Font(None, 50)
        dealerScore = scoreBoardFont.render("Dealer Value: ", True, (0, 0, 255))
        playerScore = scoreBoardFont.render("Player Value: ", True, (0, 0, 255))
        if firstTime:
            gameMoney -= bidAmount
        moneyFont = pygame.font.Font(None, 45)
        info1 = moneyFont.render("Bank Balance: $" + str(gameMoney) + "0", True, (255, 255, 255))
        info2 = moneyFont.render("Deposited: $" + str(bidAmount) + "0", True, (255, 255, 255))
        if firstTime:
            allCards = ["ace of hearts", "king of hearts", "queen of hearts", "jack of hearts", "2 of hearts", "3 of hearts", "4 of hearts", "5 of hearts", "6 of hearts", "7 of hearts", "8 of hearts", "9 of hearts", "10 of hearts", "ace of clubs", "king of clubs", "queen of clubs", "jack of clubs", "2 of clubs", "3 of clubs", "4 of clubs", "5 of clubs", "6 of clubs", "7 of clubs", "8 of clubs", "9 of clubs", "10 of clubs", "ace of diamonds", "king of diamonds", "queen of diamonds", "jack of diamonds", "2 of diamonds", "3 of diamonds", "4 of diamonds", "5 of diamonds", "6 of diamonds", "7 of diamonds", "8 of diamonds", "9 of diamonds", "10 of diamonds", "ace of spades", "king of spades", "queen of spades", "jack of spades", "2 of spades", "3 of spades", "4 of spades", "5 of spades", "6 of spades", "7 of spades", "8 of spades", "9 of spades", "10 of spades"]
            random.shuffle(allCards)
            dealerDraw = [allCards[0]]
            allCards.remove(dealerDraw[0])
            dealerDraw.append(allCards[0])
            allCards.remove(dealerDraw[1])
            playerDraw = [allCards[0]]
            allCards.remove(playerDraw[0])
            playerDraw.append(allCards[0])
            allCards.remove(playerDraw[1])
            dealerValueList = list(map(cardValue, dealerDraw))
            playerValueList = list(map(cardValue, playerDraw))
            dealerValue = sum(dealerValueList)
            if 11 in dealerValueList:
                if dealerValue > 21:
                    ace = dealerValueList.index(11)
                    dealerValueList.pop(ace)
                    dealerValueList.insert(ace, 1)
                    dealerValue = sum(dealerValueList)
            playerValue = sum(playerValueList)
            if 11 in playerValueList:
                if playerValue > 21:
                    ace = playerValueList.index(11)
                    playerValueList.pop(ace)
                    playerValueList.insert(ace, 1)
                    playerValue = sum(playerValueList)
            dealerBlackjack = 0
            playerBlackjack = 0
            dealerBust = 0
            playerBust = 0
        screen.blit(playScreen, (0,0))
        if not(stand):
            screen.blit(standButton, (standButtonRect.x, standButtonRect.y))
            screen.blit(hitButton, (hitButtonRect.x, hitButtonRect.y))
        else:
            standButtonRect = standButtonRect.move(-5000, 0)
            hitButtonRect = hitButtonRect.move(5000, 0)
            screen.blit(standButton, (standButtonRect.x, standButtonRect.y))
            screen.blit(hitButton, (hitButtonRect.x, hitButtonRect.y))
        dealerDialogue2 = pygame.Surface((795, 111))
        dealerDialogue2.fill(color=(0, 0, 0))
        screen.blit(dealerDialogue2, (380, 37))
        screen.blit(info1, (100, 630))
        screen.blit(info2, (100, 660))
        dealerFont = pygame.font.Font(None, 24)
        if not(stand):
            dealerText1 = dealerFont.render("I have drawn a card, which I will face down, and I have drawn " + dealerDraw[1] + ", which I will face up.", True, (0, 255, 0))
        screen.blit(dealerText1, (385, 40))
        if hitCount == 2:
            dealerText2 = dealerFont.render("For you, I have drawn " + playerDraw[0] + " and " + playerDraw[1] + ", both of which I will face up.", True, (0, 255, 0))
        screen.blit(dealerText2, (385, 60))
        if not(stand):
            dealerText3 = dealerFont.render("My current value is " + str(dealerValue - cardValue(dealerDraw[0])) + " plus the secret face down value.", True, (0, 255, 0))
        screen.blit(dealerText3, (385, 80))
        if hitCount == 2:
            dealerText4 = dealerFont.render("Your current value is " + str(playerValue) + ".", True, (0, 255, 0))
        screen.blit(dealerText4, (385, 100))
        if playerValue < 21 and not(dealerPlay) and not(reveal) and not(stand):
            dealerText5 = dealerFont.render("Do you want to hit or stand?", True, (0, 255, 0))
            screen.blit(dealerText5, (385, 120))
        elif playerValue == 21 and firstTime:
            playerBlackjack = 1
        if firstTime:
            dealerCardRect1 = pygame.Rect(-203, 175, 60, 150)
            dealerCardRect2 = pygame.Rect(-232, 175, 60, 150)
            playerCardRect1 = pygame.Rect(1399, 467, 60, 150)
            playerCardRect2 = pygame.Rect(1428, 467, 60, 150)
            dealerCard1 = pygame.image.load(str(dealerDraw[0]) + ".png").convert_alpha()
            pygame.transform.scale(dealerCard1, (60, 150))
            dealerCard2 = pygame.image.load(str(dealerDraw[1]) + ".png").convert_alpha()
            pygame.transform.scale(dealerCard2, (60, 150))
            playerCard2 = pygame.image.load(str(playerDraw[1]) + ".png").convert_alpha()
            pygame.transform.scale(playerCard2, (60, 150))
            firstTime = 0
        screen.blit(dealerCard1, dealerCardRect1.topleft)
        dealerCard1cover = pygame.image.load("backofcards.png").convert_alpha()
        pygame.transform.scale(dealerCard1cover, (60, 150))
        if not(reveal):
            screen.blit(dealerCard1cover, dealerCardRect1.topleft)
        playerCard1 = pygame.image.load(str(playerDraw[0]) + ".png").convert_alpha()
        pygame.transform.scale(playerCard1, (60, 150))
        screen.blit(playerCard1, playerCardRect1.topleft)
        if not(dealerCardRect1.collidepoint((1114, 175))) and not(reveal):
            dealerCardRect1 = dealerCardRect1.move(37, 0)
            screen.blit(dealerCard1, dealerCardRect1.topleft)
            screen.blit(dealerCard1cover, dealerCardRect1.topleft)
        elif not(dealerCardRect2.collidepoint((1011, 175))):
            dealerCardRect2 = dealerCardRect2.move(37, 0)
            screen.blit(dealerCard2, dealerCardRect2.topleft)
        if not(playerCardRect1.collidepoint((104, 467))):
            playerCardRect1 = playerCardRect1.move(-37, 0)
            screen.blit(playerCard1, playerCardRect1.topleft)
        elif not(playerCardRect2.collidepoint((207, 467))):
            playerCardRect2 = playerCardRect2.move(-37, 0)
            screen.blit(playerCard2, playerCardRect2.topleft)
        screen.blit(dealerCard2, dealerCardRect2.topleft)
        screen.blit(playerCard2, playerCardRect2.topleft)
        if hit:
            dealerText2 = dealerFont.render("You have drawn " + playerDraw[len(playerDraw) - 1] + ".", True, (0, 255, 0))
            dealerText4 = dealerFont.render("Your current value is " + str(playerValue) + ".", True, (0, 255, 0))
            if not(stand):
                hitCount += 1
                if hitCount == 3:
                    playerCardRect3 = pygame.Rect(1428, 467, 60, 150)
                    playerCard3 = pygame.image.load(str(playerDraw[len(playerDraw) - 1]) + ".png").convert_alpha()
                    pygame.transform.scale(playerCard3, (60, 150))
                elif hitCount == 4:
                    playerCardRect4 = pygame.Rect(1428, 467, 60, 150)
                    playerCard4 = pygame.image.load(str(playerDraw[len(playerDraw) - 1]) + ".png").convert_alpha()
                    pygame.transform.scale(playerCard4, (60, 150))
                elif hitCount == 5:
                    playerCardRect5 = pygame.Rect(1428, 467, 60, 150)
                    playerCard5 = pygame.image.load(str(playerDraw[len(playerDraw) - 1]) + ".png").convert_alpha()
                    pygame.transform.scale(playerCard5, (60, 150))
                elif hitCount == 6:
                    playerCardRect6 = pygame.Rect(1428, 467, 60, 150)
                    playerCard6 = pygame.image.load(str(playerDraw[len(playerDraw) - 1]) + ".png").convert_alpha()
                    pygame.transform.scale(playerCard6, (60, 150))
                elif hitCount == 7:
                    playerCardRect7 = pygame.Rect(1428, 467, 60, 150)
                    playerCard7 = pygame.image.load(str(playerDraw[len(playerDraw) - 1]) + ".png").convert_alpha()
                    pygame.transform.scale(playerCard7, (60, 150))
                elif hitCount == 8:
                    playerCardRect8 = pygame.Rect(1428, 467, 60, 150)
                    playerCard8 = pygame.image.load(str(playerDraw[len(playerDraw) - 1]) + ".png").convert_alpha()
                    pygame.transform.scale(playerCard8, (60, 150))
                elif hitCount == 9:
                    playerCardRect9 = pygame.Rect(1428, 467, 60, 150)
                    playerCard9 = pygame.image.load(str(playerDraw[len(playerDraw) - 1]) + ".png").convert_alpha()
                    pygame.transform.scale(playerCard9, (60, 150))
                elif hitCount == 10:
                    playerCardRect10 = pygame.Rect(1428, 467, 60, 150)
                    playerCard10 = pygame.image.load(str(playerDraw[len(playerDraw) - 1]) + ".png").convert_alpha()
                    pygame.transform.scale(playerCard10, (60, 150))
                elif hitCount == 11:
                    playerCardRect11 = pygame.Rect(1428, 467, 60, 150)
                    playerCard11 = pygame.image.load(str(playerDraw[len(playerDraw) - 1]) + ".png").convert_alpha()
                    pygame.transform.scale(playerCard11, (60, 150))
            if playerValue >= 21:
                stand = 1
            hit = 0
        if hitCount >= 3:
            screen.blit(playerCard3, playerCardRect3.topleft)
            if not(playerCardRect3.collidepoint((333, 467))):
                playerCardRect3 = playerCardRect3.move(-11, 0)
                screen.blit(playerCard3, playerCardRect3.topleft)
        if hitCount >= 4:
            screen.blit(playerCard4, playerCardRect4.topleft)
            if not(playerCardRect4.collidepoint((433, 467))):
                playerCardRect4 = playerCardRect4.move(-11, 0)
                screen.blit(playerCard4, playerCardRect4.topleft)
        if hitCount >= 5:
            screen.blit(playerCard5, playerCardRect5.topleft)
            if not(playerCardRect5.collidepoint((533, 467))):
                playerCardRect5 = playerCardRect5.move(-11, 0)
                screen.blit(playerCard5, playerCardRect5.topleft)
        if hitCount >= 6:
            screen.blit(playerCard6, playerCardRect6.topleft)
            if not(playerCardRect6.collidepoint((633, 467))):
                playerCardRect6 = playerCardRect6.move(-11, 0)
                screen.blit(playerCard6, playerCardRect6.topleft)
        if hitCount >= 7:
            screen.blit(playerCard7, playerCardRect7.topleft)
            if not(playerCardRect7.collidepoint((733, 467))):
                playerCardRect7 = playerCardRect7.move(-11, 0)
                screen.blit(playerCard7, playerCardRect7.topleft)
        if hitCount >= 8:
            screen.blit(playerCard8, playerCardRect8.topleft)
            if not(playerCardRect8.collidepoint((833, 467))):
                playerCardRect8 = playerCardRect8.move(-11, 0)
                screen.blit(playerCard8, playerCardRect8.topleft)
        if hitCount >= 9:
            screen.blit(playerCard9, playerCardRect9.topleft)
            if not(playerCardRect9.collidepoint((923, 467))):
                playerCardRect9 = playerCardRect9.move(-11, 0)
                screen.blit(playerCard9, playerCardRect9.topleft)
        if hitCount >= 10:
            screen.blit(playerCard10, playerCardRect10.topleft)
            if not(playerCardRect10.collidepoint((1023, 467))):
                playerCardRect10 = playerCardRect10.move(-11, 0)
                screen.blit(playerCard10, playerCardRect10.topleft)
        if hitCount >= 11:
            screen.blit(playerCard11, playerCardRect11.topleft)
            if not(playerCardRect11.collidepoint((1123, 467))):
                playerCardRect11 = playerCardRect11.move(-11, 0)
                screen.blit(playerCard11, playerCardRect11.topleft)
        if playerValue > 21:
            playerBust = 1
            bidAmount = 0.00
            stand = 1
            dealerText5 = dealerFont.render("Oops, you have busted. So, your hand is essentially worth nothing.", True, (0, 255, 0))
            screen.blit(dealerText5, (385, 120))
        if stand:
            if not(playerBust):
                dealerText5 = dealerFont.render("Your hand is worth " + str(playerValue) + ".", True, (0, 255, 0))
            screen.blit(dealerText5, (385, 120))
            if not(dealerPlay) and not(reveal):
                dealerText1 = dealerFont.render("Now, the card I had faced down is " + dealerDraw[0] + ".", True, (0, 255, 0))
                dealerText3 = dealerFont.render("So, my current value is " + str(dealerValue) + ".", True, (0, 255, 0))
                if not(dealerCardRect1.collidepoint((1500, 175))):
                    dealerCardRect1 = dealerCardRect1.move(10, 0)
                    screen.blit(dealerCard1, dealerCardRect1.topleft)
                    screen.blit(dealerCard1cover, dealerCardRect1.topleft)
                    if dealerCardRect1.collidepoint((1500, 175)):
                        reveal = 1
            if reveal:
                if not(dealerCardRect1.collidepoint((1055, 175))):
                    dealerCardRect1 = dealerCardRect1.move(-10, 0)
                    screen.blit(dealerCard1, dealerCardRect1.topleft)
                    if dealerCardRect1.collidepoint((1055, 175)):
                        dealerPlay = 1
        if dealerPlay:
            if dealerValue < 17:
                hitOrStand = "hit"
            elif dealerValue >= 17:
                if dealerValue == 21:
                    dealerBlackjack = 1
                dealerPlay = 0
                hitOrStand = "stand"
        if hitOrStand == "hit":
            dealerHitCount += 1
            dealerDraw.append(allCards[0])
            allCards.remove(dealerDraw[len(dealerDraw) - 1])
            dealerValueList.append(cardValue(dealerDraw[len(dealerDraw) - 1]))
            dealerValue = sum(dealerValueList)
            if 11 in dealerValueList:
                if dealerValue > 21:
                    ace = dealerValueList.index(11)
                    dealerValueList.pop(ace)
                    dealerValueList.insert(ace, 1)
                    dealerValue = sum(dealerValueList)
            dealerText1 = dealerFont.render("I have drawn " + dealerDraw[len(dealerDraw) - 1] + ".", True, (0, 255, 0))
            dealerText3 = dealerFont.render("My current value is " + str(dealerValue) + ".", True, (0, 255, 0))
            if dealerHitCount == 3:
                dealerCardRect3 = pygame.Rect(-232, 175, 60, 150)
                dealerCard3 = pygame.image.load(str(dealerDraw[len(dealerDraw) - 1]) + ".png").convert_alpha()
                pygame.transform.scale(dealerCard3, (60, 150))
            elif dealerHitCount == 4:
                dealerCardRect4 = pygame.Rect(-232, 175, 60, 150)
                dealerCard4 = pygame.image.load(str(dealerDraw[len(dealerDraw) - 1]) + ".png").convert_alpha()
                pygame.transform.scale(dealerCard4, (60, 150))
            elif dealerHitCount == 5:
                dealerCardRect5 = pygame.Rect(-232, 175, 60, 150)
                dealerCard5 = pygame.image.load(str(dealerDraw[len(dealerDraw) - 1]) + ".png").convert_alpha()
                pygame.transform.scale(dealerCard5, (60, 150))
            elif dealerHitCount == 6:
                dealerCardRect6 = pygame.Rect(-232, 175, 60, 150)
                dealerCard6 = pygame.image.load(str(dealerDraw[len(dealerDraw) - 1]) + ".png").convert_alpha()
                pygame.transform.scale(dealerCard6, (60, 150))
            elif dealerHitCount == 7:
                dealerCardRect7 = pygame.Rect(-232, 175, 60, 150)
                dealerCard7 = pygame.image.load(str(dealerDraw[len(dealerDraw) - 1]) + ".png").convert_alpha()
                pygame.transform.scale(dealerCard7, (60, 150))
            elif dealerHitCount == 8:
                dealerCardRect8 = pygame.Rect(-232, 175, 60, 150)
                dealerCard8 = pygame.image.load(str(dealerDraw[len(dealerDraw) - 1]) + ".png").convert_alpha()
                pygame.transform.scale(dealerCard8, (60, 150))
            elif dealerHitCount == 9:
                dealerCardRect9 = pygame.Rect(-232, 175, 60, 150)
                dealerCard9 = pygame.image.load(str(dealerDraw[len(dealerDraw) - 1]) + ".png").convert_alpha()
                pygame.transform.scale(dealerCard9, (60, 150))
            elif dealerHitCount == 10:
                dealerCardRect10 = pygame.Rect(-232, 175, 60, 150)
                dealerCard10 = pygame.image.load(str(dealerDraw[len(dealerDraw) - 1]) + ".png").convert_alpha()
                pygame.transform.scale(dealerCard10, (60, 150))
            if dealerValue >= 17:
                hitOrStand = "stand"
        if dealerHitCount >= 3:
            screen.blit(dealerCard3, dealerCardRect3.topleft)
            if not(dealerCardRect3.collidepoint((888, 175))):
                dealerCardRect3 = dealerCardRect3.move(11, 0)
                screen.blit(dealerCard3, dealerCardRect3.topleft)
        if dealerHitCount >= 4:
            screen.blit(dealerCard4, dealerCardRect4.topleft)
            if not(dealerCardRect4.collidepoint((788, 175))):
                dealerCardRect4 = dealerCardRect4.move(11, 0)
                screen.blit(dealerCard4, dealerCardRect4.topleft)
        if dealerHitCount >= 5:
            screen.blit(dealerCard5, dealerCardRect5.topleft)
            if not(dealerCardRect5.collidepoint((688, 175))):
                dealerCardRect5 = dealerCardRect5.move(11, 0)
                screen.blit(dealerCard5, dealerCardRect5.topleft)
        if dealerHitCount >= 6:
            screen.blit(dealerCard6, dealerCardRect6.topleft)
            if not(dealerCardRect6.collidepoint((588, 175))):
                dealerCardRect6 = dealerCardRect6.move(11, 0)
                screen.blit(dealerCard6, dealerCardRect6.topleft)
        if dealerHitCount >= 7:
            screen.blit(dealerCard7, dealerCardRect7.topleft)
            if not(dealerCardRect7.collidepoint((488, 175))):
                dealerCardRect7 = dealerCardRect7.move(11, 0)
                screen.blit(dealerCard7, dealerCardRect7.topleft)
        if dealerHitCount >= 8:
            screen.blit(dealerCard8, dealerCardRect8.topleft)
            if not(dealerCardRect8.collidepoint((388, 175))):
                dealerCardRect8 = dealerCardRect8.move(11, 0)
                screen.blit(dealerCard8, dealerCardRect8.topleft)
        if dealerHitCount >= 9:
            screen.blit(dealerCard9, dealerCardRect9.topleft)
            if not(dealerCardRect9.collidepoint((288, 175))):
                dealerCardRect9 = dealerCardRect9.move(11, 0)
                screen.blit(dealerCard9, dealerCardRect9.topleft)
        if dealerHitCount >= 10:
            screen.blit(dealerCard10, dealerCardRect10.topleft)
            if not(dealerCardRect10.collidepoint((188, 175))):
                dealerCardRect10 = dealerCardRect10.move(11, 0)
                screen.blit(dealerCard10, dealerCardRect10.topleft)
        if dealerValue > 21:
            dealerBust = 1
            hitOrStand = "stand"
            dealerText6 = dealerFont.render("Oops, I have busted. So, my hand is essentially worth nothing.", True, (0, 255, 0))
            screen.blit(dealerText6, (615, 80))
        elif hitOrStand == "stand":
            dealerText6 = dealerFont.render("My hand is worth " + str(dealerValue) + ".", True, (0, 255, 0))
            screen.blit(dealerText6, (615, 80))
        if not(dealerPlay) and hitOrStand == "stand":
            dealerDialogue3 = pygame.Surface((1025, 100))
            dealerDialogue3.fill(color=(0, 0, 0))
            screen.blit(dealerDialogue3, (117, 345))
            if playerBust:
                dealerText7 = dealerFont.render("Since you have busted, your deposit will go to void.", True, (0, 255, 0))
                screen.blit(dealerText7, (125, 355))
                dealerText8 = dealerFont.render("Your current bank balance is $" + str(gameMoney) + "0.", True, (0, 255, 0))
                screen.blit(dealerText8, (125, 385))
            else:
                if playerValue > dealerValue or dealerBust:
                    if playerBlackjack:
                        gameMoney += bidAmount * 2.5
                        bidAmount = 0.00
                        dealerText7 = dealerFont.render("Since your hand is worth more than my hand, and you got a blackjack, your deposit will multiply by 2.5.", True, (0, 255, 0))
                        screen.blit(dealerText7, (125, 355))
                        dealerText8 = dealerFont.render("Your current bank balance is $" + str(gameMoney) + "0.", True, (0, 255, 0))
                        screen.blit(dealerText8, (125, 385))
                    else:
                        gameMoney += bidAmount * 2.0
                        bidAmount = 0.00
                        dealerText7 = dealerFont.render("Since your hand is worth more than my hand, your deposit will double.", True, (0, 255, 0))
                        screen.blit(dealerText7, (125, 355))
                        dealerText8 = dealerFont.render("Your current bank balance is $" + str(gameMoney) + "0.", True, (0, 255, 0))
                        screen.blit(dealerText8, (125, 385))
                elif playerValue < dealerValue:
                    bidAmount = 0.00
                    dealerText7 = dealerFont.render("Since your hand is worth less than my hand, your deposit will go to void.", True, (0, 255, 0))
                    screen.blit(dealerText7, (125, 355))
                    dealerText8 = dealerFont.render("Your current bank balance is $" + str(gameMoney) + "0.", True, (0, 255, 0))
                    screen.blit(dealerText8, (125, 385))
                elif playerValue == dealerValue:
                    gameMoney += bidAmount
                    bidAmount = 0.00
                    dealerText7 = dealerFont.render("Since your hand is worth the same as my hand, your deposit will stay the same.", True, (0, 255, 0))
                    screen.blit(dealerText7, (125, 355))
                    dealerText8 = dealerFont.render("Your current bank balance is $" + str(gameMoney) + "0.", True, (0, 255, 0))
                    screen.blit(dealerText8, (125, 385))
            dealerText9 = dealerFont.render("Would you like to invest in Blackjack again? You definitely should. Think about all the potential benefits! Press the SPACE key to ", True, (255, 0, 0))
            dealerText10 = dealerFont.render("do so, or press the esc key to quit Blackjack...", True, (255, 0, 0))
            screen.blit(dealerText9, (125, 409))
            screen.blit(dealerText10, (125, 426))
        if transportBack:
            standButtonRect = standButton.get_rect(topleft = (160, 342))
            hitButtonRect = hitButton.get_rect(topleft = (810, 342))
            transportBack = 0
        screen.blit(standButton, (standButtonRect.x, standButtonRect.y))
        screen.blit(hitButton, (hitButtonRect.x, hitButtonRect.y))
        if stand:
            dealerScore = scoreBoardFont.render("Dealer Value: " + str(dealerValue), True, (255, 255, 255))
        else:
            dealerScore = scoreBoardFont.render("Dealer Value: " + str(dealerValue - cardValue(dealerDraw[0])) + "+", True, (255, 255, 255))
        playerScore = scoreBoardFont.render("Player Value: " + str(playerValue), True, (255, 255, 255))
        screen.blit(dealerScore, (69, 60))
        screen.blit(playerScore, (69, 100))
    # Screen of undiscovered ambition
    if GAMESTATE == 5:
        backHelpButtonRect = backHelpButton.get_rect(topleft=(-5000, 580))
        if gameMoney < minimumBid:
            loseFont = pygame.font.Font(None, 28)
            loseText = loseFont.render("(At the moment, you currently need more investing power. So, go bring more money.)", True, (255, 255, 255))
            encouragementFont = pygame.font.Font(None, 25)
            encouragementText = encouragementFont.render("Press the delete key to reset the game!", True, (255, 255, 255))
            discouragementFont = pygame.font.Font(None, 27)
            discouragementText = discouragementFont.render("Press the esc key to give up (coward)", True, (0, 0, 0))
            screen.blit(loseScreen, (0, 0))
            screen.blit(loseText, (245, 10))
            screen.blit(encouragementText, (570, 160))
            screen.blit(discouragementText, (330, 500))
    # Event Handler
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("Your current bank balance is $" + str(gameMoney) + "0.")
            # Save the current gaming session if this game is exited.
            save = str(gameMoney)
            with open("blackjackDisk.txt", mode ="w", encoding ="utf-8") as sl:
                sl.write(save)
            pygame.quit()
            sys.exit(0)
            running = False
        if keys[pygame.K_ESCAPE]:
            print("Your current bank balance is $" + str(gameMoney) + "0.")
            # Save the current gaming session if this game is exited.
            save = str(gameMoney)
            with open("blackjackDisk.txt", mode ="w", encoding ="utf-8") as sl:
                sl.write(save)
            pygame.quit()
            sys.exit(0)
            running = False
        if keys[pygame.K_SPACE] and GAMESTATE == 4:
            MENU_MONEY = "Bank Balance: $" + str(gameMoney) + "0"
            bidAmount = 0.00
            minimumBid = 100.00
            GAMESTATE = 0
            firstTime = 1
            hit = 0
            hitCount = 2
            stand = 0
            dealerPlay = 0
            hitOrStand = ""
            reveal = 0
            dealerHitCount = 2
            addMinimum = 1
            transportBack = 1
            y = 1
            x = 4
        if keys[pygame.K_DELETE] and GAMESTATE == 5:
            gameMoney = 200.00
            MENU_MONEY = "Bank Balance: $" + str(gameMoney) + "0"
            bidAmount = 0.00
            minimumBid = 100.00
            GAMESTATE = 0
            firstTime = 1
            hit = 0
            hitCount = 2
            stand = 0
            dealerPlay = 0
            hitOrStand = ""
            reveal = 0
            dealerHitCount = 2
            addMinimum = 1
            transportBack = 1
            y = 1
            x = 4
        # Check if button is clicked
        if event.type == pygame.MOUSEBUTTONDOWN:
            if playButtonRect.collidepoint(event.pos) and GAMESTATE != 5:
                buttonSound.play(0)
                if gameMoney >= minimumBid:
                    GAMESTATE = 3
                    playButtonRect = playButtonRect.move(-5000, 0)
                    helpButtonRect = helpButtonRect.move(-5000, 0)
                    creditButtonRect = creditButtonRect.move(-5000, 0)
                    backHelpButtonRect = backHelpButtonRect.move(5000, 0)
                    if addMinimum:
                        bidAmount += minimumBid
                        addMinimum = 0
                    BID_MONEY = "$" + str(bidAmount) + "0"
                else:
                    buttonFailure.play(0)
                    GAMESTATE = 5
            if helpButtonRect.collidepoint(event.pos) and GAMESTATE != 5:
                buttonSound.play(0)
                GAMESTATE = 1
                playButtonRect = playButtonRect.move(-5000,0)
                helpButtonRect = helpButtonRect.move(-5000, 0)
                creditButtonRect = creditButtonRect.move(-5000, 0)
                backHelpButtonRect = backHelpButtonRect.move(5000, 0)
            if creditButtonRect.collidepoint(event.pos) and GAMESTATE != 5:
                buttonSound.play(0)
                GAMESTATE = 2
                playButtonRect = playButtonRect.move(-5000, 0)
                helpButtonRect = helpButtonRect.move(-5000, 0)
                creditButtonRect = creditButtonRect.move(-5000, 0)
                backHelpButtonRect = backHelpButtonRect.move(5000, 0)
            if backHelpButtonRect.collidepoint(event.pos) and GAMESTATE != 4:
                buttonSound.play(0)
                GAMESTATE = 0
                backHelpButtonRect = backHelpButtonRect.move(-5000, 0)
                playButtonRect = playButtonRect.move(5000, 0)
                helpButtonRect = helpButtonRect.move(5000, 0)
                creditButtonRect = creditButtonRect.move(5000, 0)
            # WIP (+/- buttons)
            if plusButtonRect.collidepoint(event.pos):
                if GAMESTATE == 3:
                    if bidAmount < gameMoney:
                        buttonSound.play(0)
                        screen.blit(backgroundImage, (0, 0))
                        bidAmount += 10.00 ** y
                        BID_MONEY = "$" + str(bidAmount) + "0"
                        moneyText = moneyFont.render(str(BID_MONEY), True, (255, 255, 255))
                        screen.blit(bidText, (110, 60))
                        screen.blit(moneyText, (((sizex / 2) - (moneyWidth / 2)), ((sizey / 2) - (moneyHeight / 2)) + 25))
                        screen.blit(backHelpButton, (backHelpButtonRect.x, backHelpButtonRect.y))
                        screen.blit(plusButton, (plusButtonRect.x, plusButtonRect.y))
                        screen.blit(minusButton, (minusButtonRect.x, minusButtonRect.y))
                        screen.blit(gambleButton, (gambleButtonRect.x, gambleButtonRect.y))
                        screen.blit(maxButton, (maxButtonRect.x, maxButtonRect.y))
                        screen.blit(minButton, (minButtonRect.x, minButtonRect.y))
                    else:
                        buttonFailure.play(0)
            if minusButtonRect.collidepoint(event.pos):
                if GAMESTATE == 3:
                    if bidAmount > minimumBid:
                        buttonSound.play(0)
                        screen.blit(backgroundImage, (0, 0))
                        bidAmount -= 10.00 ** y
                        BID_MONEY = "$" + str(bidAmount) + "0"
                        moneyText = moneyFont.render(str(BID_MONEY), True, (255, 255, 255))
                        screen.blit(bidText, (110, 60))
                        screen.blit(moneyText, (((sizex / 2) - (moneyWidth / 2)), ((sizey / 2) - (moneyHeight / 2)) + 25))
                        screen.blit(backHelpButton, (backHelpButtonRect.x, backHelpButtonRect.y))
                        screen.blit(plusButton, (plusButtonRect.x, plusButtonRect.y))
                        screen.blit(minusButton, (minusButtonRect.x, minusButtonRect.y))
                        screen.blit(gambleButton, (gambleButtonRect.x, gambleButtonRect.y))
                        screen.blit(maxButton, (maxButtonRect.x, maxButtonRect.y))
                        screen.blit(minButton, (minButtonRect.x, minButtonRect.y))
                    else:
                        buttonFailure.play(0)
            if minButtonRect.collidepoint(event.pos):
                if GAMESTATE == 3:
                    if bidAmount > minimumBid:
                        buttonSound.play(0)
                        screen.blit(backgroundImage, (0, 0))
                        bidAmount = minimumBid
                        BID_MONEY = "$" + str(bidAmount) + "0"
                        moneyText = moneyFont.render(str(BID_MONEY), True, (255, 255, 255))
                        screen.blit(bidText, (110, 60))
                        screen.blit(moneyText, (((sizex / 2) - (moneyWidth / 2)), ((sizey / 2) - (moneyHeight / 2)) + 25))
                        screen.blit(backHelpButton, (backHelpButtonRect.x, backHelpButtonRect.y))
                        screen.blit(plusButton, (plusButtonRect.x, plusButtonRect.y))
                        screen.blit(minusButton, (minusButtonRect.x, minusButtonRect.y))
                        screen.blit(gambleButton, (gambleButtonRect.x, gambleButtonRect.y))
                        screen.blit(maxButton, (maxButtonRect.x, maxButtonRect.y))
                        screen.blit(minButton, (minButtonRect.x, minButtonRect.y))
                    else:
                        buttonFailure.play(0)
            if maxButtonRect.collidepoint(event.pos):
                if GAMESTATE == 3:
                    if bidAmount < gameMoney and bidAmount >= minimumBid:
                        buttonSound.play(0)
                        screen.blit(backgroundImage, (0, 0))
                        bidAmount = gameMoney
                        BID_MONEY = "$" + str(bidAmount) + "0"
                        moneyText = moneyFont.render(str(BID_MONEY), True, (255, 255, 255))
                        screen.blit(bidText, (110, 60))
                        screen.blit(moneyText, (((sizex / 2) - (moneyWidth / 2)), ((sizey / 2) - (moneyHeight / 2)) + 25))
                        screen.blit(backHelpButton, (backHelpButtonRect.x, backHelpButtonRect.y))
                        screen.blit(plusButton, (plusButtonRect.x, plusButtonRect.y))
                        screen.blit(minusButton, (minusButtonRect.x, minusButtonRect.y))
                        screen.blit(gambleButton, (gambleButtonRect.x, gambleButtonRect.y))
                        screen.blit(maxButton, (maxButtonRect.x, maxButtonRect.y))
                        screen.blit(minButton, (minButtonRect.x, minButtonRect.y))
                    else:
                        buttonFailure.play(0)
            if gambleButtonRect.collidepoint(event.pos):
                if GAMESTATE == 3:
                    if bidAmount >= minimumBid and bidAmount <= gameMoney:
                        buttonSound.play(0)
                        GAMESTATE = 4
                    else:
                        buttonFailure.play(0)
                        GAMESTATE = 3
            if hitButtonRect.collidepoint(event.pos):
                if GAMESTATE == 4:
                    if playerValue < 21:
                        hit = 1
                        playerDraw.append(allCards[0])
                        allCards.remove(playerDraw[len(playerDraw) - 1])
                        playerValueList.append(cardValue(playerDraw[len(playerDraw) - 1]))
                        playerValue = sum(playerValueList)
                        if 11 in playerValueList:
                            if playerValue > 21:
                                ace = playerValueList.index(11)
                                playerValueList.pop(ace)
                                playerValueList.insert(ace, 1)
                                playerValue = sum(playerValueList)
                        buttonSound.play(0)
                    else:
                        buttonFailure.play(0)
            if standButtonRect.collidepoint(event.pos):
                if GAMESTATE == 4:
                    stand = 1

    # Check for mouse over button (scuffed WIP)
    bx, by = pygame.mouse.get_pos()
    if GAMESTATE == 0:
        # PLAY button
        if playButtonRect.x <= bx <= playButtonRect.x + 300 and playButtonRect.y <= by <= playButtonRect.y + 120:
            playButton = pygame.image.load("playButtonSelected.png").convert()
            screen.blit(playButton, (500, 300))
        else:
            playButton = pygame.image.load("playButtonIdle.png").convert()
            screen.blit(playButton, (500, 300))
        # HELP button
        if helpButtonRect.x <= bx <= helpButtonRect.x + 290 and helpButtonRect.y <= by <= helpButtonRect.y + 110:
            helpButton = pygame.image.load("helpButtonSelected.png").convert()
            screen.blit(helpButton, (190, 305))
        else:
            helpButton = pygame.image.load("helpButtonIdle.png").convert()
            screen.blit(helpButton, (190, 305))
        # CREDIT button
        if creditButtonRect.x <= bx <= creditButtonRect.x + 290 and creditButtonRect.y <= by <= creditButtonRect.y + 110:
            creditButton = pygame.image.load("creditsButtonSelected.png").convert()
            screen.blit(creditButton, (820, 305))
        else:
            creditButton = pygame.image.load("creditsButtonIdle.png").convert()
            screen.blit(creditButton, (820, 305))
    # BACK button
    if GAMESTATE == 1 or GAMESTATE == 2 or GAMESTATE == 3:
        if backHelpButtonRect.x <= bx <= backHelpButtonRect.x + 290 and backHelpButtonRect.y <= by <= backHelpButtonRect.y + 110:
            backHelpButton = pygame.image.load("backHelpButtonSelected.png").convert()
            screen.blit(backHelpButton, (500, 580))
        else:
            backHelpButton = pygame.image.load("backHelpButtonIdle.png")
            screen.blit(backHelpButton, (500, 580))
    if GAMESTATE == 3:
        if plusButtonRect.x <= bx <= plusButtonRect.x + 100 and plusButtonRect.y <= by <= plusButtonRect.y + 100:
            plusButton = pygame.image.load("plusButtonSelected.png")
            screen.blit(plusButton, (380, 445))
        else:
            plusButton = pygame.image.load("plusButtonIdle.png")
            screen.blit(plusButton, (380, 445))
        if minusButtonRect.x <= bx <= minusButtonRect.x + 100 and minusButtonRect.y <= by <= minusButtonRect.y + 100:
            minusButton = pygame.image.load("minusButtonSelected.png")
            screen.blit(minusButton, (810, 445))
        else:
            minusButton = pygame.image.load("minusButtonIdle.png")
            screen.blit(minusButton, (810, 445))
        if minButtonRect.x <= bx <= minButtonRect.x + 188 and minButtonRect.y <= by <= minButtonRect.y + 90:
            minButton = pygame.image.load("minButtonSelected.png")
            screen.blit(minButton, (920, 450))
        else:
            minButton = pygame.image.load("minButtonIdle.png")
            screen.blit(minButton, (920, 450))
        if maxButtonRect.x <= bx <= maxButtonRect.x + 188 and maxButtonRect.y <= by <= maxButtonRect.y + 90:
            maxButton = pygame.image.load("maxButtonSelected.png")
            screen.blit(maxButton, (180, 450))
        else:
            maxButton = pygame.image.load("maxButtonIdle.png")
            screen.blit(maxButton, (180, 450))
        # INVEST button
        if gambleButtonRect.x <= bx <= gambleButtonRect.x + 290 and gambleButtonRect.y <= by <= gambleButtonRect.y + 110:
            gambleButton = pygame.image.load("gambleButtonSelected.png")
            screen.blit(gambleButton, (500, 440))
        else:
            gambleButton = pygame.image.load("gambleButtonIdle.png")
            screen.blit(gambleButton, (500, 440))
    if GAMESTATE == 4:
        if hitButtonRect.x <= bx <= hitButtonRect.x + 290 and hitButtonRect.y <= by <= hitButtonRect.y + 110:
            hitButton = pygame.image.load("hitButtonSelected.png")
            screen.blit(hitButton, (hitButtonRect.x, hitButtonRect.y))
        else:
            hitButton = pygame.image.load("hitButtonIdle.png")
            screen.blit(hitButton, (hitButtonRect.x, hitButtonRect.y))
        if standButtonRect.x <= bx <= standButtonRect.x + 290 and standButtonRect.y <= by <= standButtonRect.y + 110:
            standButton = pygame.image.load("standButtonSelected.png")
            screen.blit(standButton, (standButtonRect.x, standButtonRect.y))
        else:
            standButton = pygame.image.load("standButtonIdle.png")
            screen.blit(standButton, (standButtonRect.x, standButtonRect.y))
    # Update the display every frame
    pygame.display.flip()
    clock.tick(60)