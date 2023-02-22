import pygame as pg

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
    bigFont = pg.font.SysFont('Corbel',50)
    hugeFont = pg.font.SysFont('Corbel',60)
    welcomeStartButtonText = bigFont.render('Start Game' , True , (0,0,0))
    welcomeLabel = hugeFont.render('Chopsticks' , True , (0,0,0))



    ### Game loop
    running = True
    screenState = "welcome"
    turn = "player"
    playerVal1 = 1
    playerVal2 = 1
    botVal1 = 1
    botVal1 = 1
    while running:
        ### Handle user input and update states
        # screenState = welcome -> intro screen
        # screenState = options -> new game / load game screen
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
                    print(screenState)
        ## On options screen

        



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
            

        #pg.Surface.blit(screen, playerRight5, (100,100))

        pg.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    main()
    
