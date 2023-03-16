import pygame as pg
from math import atan2, sin, cos, pi


class DropDown():
    def __init__(self, color_menu, color_option, x, y, w, h, font, main, options):
        self.color_menu = color_menu
        self.color_option = color_option
        self.rect = pg.Rect(x, y, w, h)
        self.font = font
        self.main = main
        self.options = options
        self.draw_menu = False
        self.menu_active = False
        self.active_option = -1

    def draw(self, surf):
        pg.draw.rect(surf, self.color_menu[self.menu_active], self.rect, 0)
        msg = self.font.render(self.main, 1, (0, 0, 0))
        surf.blit(msg, msg.get_rect(center = self.rect.center))
        if self.draw_menu:
            for i, text in enumerate(self.options):
                rect = self.rect.copy()
                rect.y += (i+1) * self.rect.height
                pg.draw.rect(surf, self.color_option[1 if i == self.active_option else 0], rect, 0)
                msg = self.font.render(text, 1, (0, 0, 0))
                surf.blit(msg, msg.get_rect(center = rect.center))

    def update(self, event):
        mpos = pg.mouse.get_pos()
        self.menu_active = self.rect.collidepoint(mpos)
        self.active_option = -1
        for i in range(len(self.options)):
            rect = self.rect.copy()
            rect.y += (i+1) * self.rect.height
            if rect.collidepoint(mpos):
                self.active_option = i
                break
        if not self.menu_active and self.active_option == -1:
            self.draw_menu = False
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if self.menu_active:
                self.draw_menu = not self.draw_menu
            elif self.draw_menu and self.active_option >= 0:
                self.draw_menu = False
                return self.active_option
        return -1


class Arrow():
    # base and point are (x,y) locations
    def __init__(self, base:tuple):
        self.base = base
        self.point = base
        self.end = base
        self.theta = 0
        self.p1 = base
        self.p2 = base
        self.a = 35 # triangle height
        self.b = 15 # half triangle base

    def draw(self, surf):
        pg.draw.line(surf, (0,0,0), self.base, self.end, width=10)
        pg.draw.polygon(surf, (0,0,0), [self.point, self.p1, self.p2])

    def update(self):
        self.point = pg.mouse.get_pos()
        self.theta = atan2(self.point[1]-self.base[1], self.point[0]-self.base[0])
        self.p1 = (self.point[0]-self.a*cos(self.theta)+self.b*cos(self.theta-pi/2), self.point[1]-self.a*sin(self.theta)+self.b*sin(self.theta-pi/2))
        self.p2 = (self.point[0]-self.a*cos(self.theta)-self.b*cos(self.theta-pi/2), self.point[1]-self.a*sin(self.theta)-self.b*sin(self.theta-pi/2))
        self.end = (self.point[0]-self.a/2*cos(self.theta), self.point[1]-self.a/2*sin(self.theta))






# what happens when one team hits other team
# only returns defender value
def doAttackLogic(attackerVal, defenderVal, gamemode):
    total = attackerVal + defenderVal
    if total < 5:
        defenderVal = total
    elif gamemode == 'Rollover' and total >= 5:
        defenderVal = total - 5
    elif gamemode == 'Cutoff' and total >= 5:
        defenderVal = 0
    return defenderVal


# what happends when one team hits a teammate
def doTransferLogic(donatorVal, receiverVal):
    pass




def main():
    ### Initialize pygame
    pg.init()
    screenWidth = 640; screenHeight = 480
    screen = pg.display.set_mode((screenWidth,screenHeight))
    clock = pg.time.Clock()
    if not pg.font:
        print("Warning, fonts disabled")
    if not pg.mixer:
        print("Warning, sound disabled")


    ### Initialize GUI elements and other things
    playerRight = []
    playerRight.append(pg.image.load("images/playerRight0.jpg").convert())
    playerRight.append(pg.image.load("images/playerRight1.jpg").convert())
    playerRight.append(pg.image.load("images/playerRight2.jpg").convert())
    playerRight.append(pg.image.load("images/playerRight3.jpg").convert())
    playerRight.append(pg.image.load("images/playerRight4.jpg").convert())
    playerRight.append(pg.image.load("images/playerRight5.jpg").convert())
    playerLeft = []; botRight = []; botLeft = []
    for img in playerRight:
        playerLeft.append(pg.transform.flip(img, True, False))
        botRight.append(pg.transform.flip(img, True, True))
        botLeft.append(pg.transform.flip(img, False, True))
    
    logo = pg.image.load("images/logo2.jpg").convert()

    medFont = pg.font.SysFont('Corbel',30)
    bigFont = pg.font.SysFont('Corbel',50)
    hugeFont = pg.font.SysFont('Corbel',60)

    welcomeStartButtonText = bigFont.render('Start Game' , True , (0,0,0))
    welcomeLabel = hugeFont.render('Chopsticks' , True , (0,0,0))
    optionsLabel = bigFont.render('Options', True, (0,0,0))
    gamemodeList = DropDown([(255,255,255), (245,245,245)], [(255,255,255), (245,245,245)],
    50, 150, 250, 50, medFont, "Select Gamemode", ["Rollover", "Cutoff"])
    whoStartsList = DropDown([(255,255,255), (245,245,245)], [(255,255,255), (245,245,245)],
    50, 300, 250, 50, medFont, "Select Who Starts", ["Player", "Computer"])
    optionsPlayButtonText = bigFont.render('Play' , True , (0,0,0))

    botRightRect = pg.Rect(154,96,112,105)
    botLeftRect = pg.Rect(374,96,112,105)
    playerLeftRect = pg.Rect(154,296,112,105)
    playerRightRect = pg.Rect(374,296,112,105)


    running = True
    screenState = 'welcome'
    turn = ''; gamemode = ''
    playerVal1 = 5; playerVal2 = 2
    botVal1 = 3; botVal2 = 4
    playerLeftAlive = True; playerRightAlive = True
    botRightAlive = True; botLeftAlive = True
    arrowActive = False; splitActive = False
    handSelected = 'none'; target = 'none'

    ### Game loop
    while running:
        ### Handle user input and update states
        # screenState = welcome -> intro screen
        # screenState = options -> new game / load game screen
        # screenState = playing -> playing the game
        # screenState = paused -> inside pause menu
        # screenState = finished -> win / lose / restart
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                raise SystemExit
            mouse = pg.mouse.get_pos() # stores (x,y) mouse position as a tuple
            #if event.type == pg.MOUSEBUTTONUP:
                #print(mouse) # for finding positions and debugging
            ## On welcome screen
            if screenState == "welcome":
                if event.type == pg.MOUSEBUTTONUP and 50 <= mouse[0] <= 50+232 and 380 <= mouse[1] <= 380+45:
                    screenState = "options"
            ## On options screen
            if screenState == "options":
                selectedOption = gamemodeList.update(event)
                selectedWhoStarts = whoStartsList.update(event)
                if event.type == pg.MOUSEBUTTONUP and 495 <= mouse[0] <= 495+95 and 395 <= mouse[1] <= 395+55:
                    screenState = "playing"
                    turn = whoStartsList.main
                    gamemode = gamemodeList.main
            ## On gameplay screen, player's turn
            if screenState == "playing" and turn == 'Player':
                # player's first mouse down to create arrow
                if event.type == pg.MOUSEBUTTONDOWN and not arrowActive and not splitActive:
                    # left hand selected
                    if playerLeftRect.collidepoint(mouse):
                        arrow = Arrow(mouse)
                        arrowActive = True
                        handSelected = 'playerLeft'
                    # right hand selected
                    elif playerRightRect.collidepoint(mouse):
                        arrow = Arrow(mouse)
                        arrowActive = True
                        handSelected = 'playerRight'
                # player's second mouse down to place arrow
                elif event.type == pg.MOUSEBUTTONDOWN and arrowActive and not splitActive:
                    # left hand selected
                    if handSelected == 'playerLeft':
                        if playerLeftRect.collidepoint(mouse):
                            target = 'none'
                            handSelected = 'none'
                            arrowActive = False
                        if playerRightRect.collidepoint(mouse): 
                            target = 'playerRight'
                            arrowActive = False
                        if botRightRect.collidepoint(mouse): 
                            target = 'botRight'
                            arrowActive = False
                        if botLeftRect.collidepoint(mouse):
                            target = 'botLeft'
                            arrowActive = False
                    # right hand selected
                    elif handSelected == 'playerRight':
                        if playerLeftRect.collidepoint(mouse):
                            target = 'playerLeft'
                            arrowActive = False
                        if playerRightRect.collidepoint(mouse): 
                            target = 'none'
                            handSelected = 'none'
                            arrowActive = False
                        if botRightRect.collidepoint(mouse): 
                            target = 'botRight'
                            arrowActive = False
                        if botLeftRect.collidepoint(mouse):
                            target = 'botLeft'
                            arrowActive = False
                # player moves arrow
                if event.type == pg.MOUSEMOTION and arrowActive and not splitActive:
                    arrow.update()
            ## On gameplay screen, computer's turn
            if screenState == "playing" and turn == "Computer":
                print('Computer takes turn')
                turn = 'player'

                
                

                
                


        ### Update Graphics
        if screenState == "welcome":
            pg.Surface.fill(screen, (255,255,255))
            pg.Surface.blit(screen, logo, (0,0))
            pg.draw.rect(screen, (0,0,0), (50,380,232,45), width=3)
            screen.blit(welcomeStartButtonText, (52,380))
            screen.blit(welcomeLabel, (225,70))
        
        if screenState == "options":
            pg.Surface.fill(screen, (255,255,255))
            screen.blit(optionsLabel, (50,50))
            if selectedOption >= 0:
                gamemodeList.main = gamemodeList.options[selectedOption]
            gamemodeList.draw(screen)
            if selectedWhoStarts >= 0:
                whoStartsList.main = whoStartsList.options[selectedWhoStarts]
            whoStartsList.draw(screen)
            if gamemodeList.main != "Select Gamemode" and whoStartsList.main != "Select Who Starts":
                screen.blit(optionsPlayButtonText, (500,400))
                pg.draw.rect(screen, (0,0,0), (495,395,95,55), width=3)

        if screenState == "playing":
            pg.Surface.fill(screen, (255,255,255))
            pg.draw.rect(screen, (0,0,0), botRightRect, width=3)
            pg.draw.rect(screen, (0,0,0), playerLeftRect, width=3)
            pg.draw.rect(screen, (0,0,0), botLeftRect, width=3)
            pg.draw.rect(screen, (0,0,0), playerRightRect, width=3)
            screen.blit(playerLeft[playerVal1], playerLeft[playerVal1].get_rect(center = (158+104/2, 300+98/2)))
            screen.blit(playerRight[playerVal2], playerRight[playerVal2].get_rect(center = (378+104/2, 300+98/2)))
            screen.blit(botRight[botVal1], botRight[botVal1].get_rect(center = (158+104/2, 100+98/2)))
            screen.blit(botLeft[botVal2], botLeft[botVal2].get_rect(center = (378+104/2, 100+98/2)))
        if screenState == "playing" and turn == "Player":
            if arrowActive:
                arrow.draw(screen)


        pg.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    main()