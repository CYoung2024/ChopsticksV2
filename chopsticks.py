import pygame as pg


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
    playerRight5 = pg.image.load("images/playerRight5.jpg").convert()
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



    ### Game loop
    running = True
    screenState = "welcome"
    turn = ""
    gamemode = ""
    playerVal1 = 1
    playerVal2 = 1
    botVal1 = 1
    botVal1 = 1
    while running:
        ### Handle user input and update states
        # screenState = welcome -> intro screen
        # screenState = options -> new game / load game screen
        # screenState = playing -> playing the game
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                raise SystemExit
            mouse = pg.mouse.get_pos() # stores (x,y) mouse position as a tuple
            if event.type == pg.MOUSEBUTTONUP:
                print(mouse) # for finding positions and debugging
            ## On welcome screen
            if screenState == "welcome":
                if event.type == pg.MOUSEBUTTONUP:
                    if 50 <= mouse[0] <= 50+232 and 380 <= mouse[1] <= 380+45:
                        screenState = "options"
            ## On options screen
            if screenState == "options":
                selectedOption = gamemodeList.update(event)
                selectedWhoStarts = whoStartsList.update(event)
                if event.type == pg.MOUSEBUTTONUP:
                    if 495 <= mouse[0] <= 495+95 and 395 <= mouse[1] <= 395+55:
                        screenState = "playing"
                        turn = whoStartsList.main
                        gamemode = gamemodeList.main

                  



        ### Update states and logic ???? maybe dont do it here
        # screenState = welcome -> intro screen
        # screenState = options -> new game / load game screen
        


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

            

        #pg.Surface.blit(screen, playerRight5, (100,100))

        pg.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    main()