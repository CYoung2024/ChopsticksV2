import pygame as pg

def updateState():
    pass

def handleUserInput():
    pass



def main():
    pg.init()
    screen = pg.display.set_mode((640,480))
    clock = pg.time.Clock()
    if not pg.font:
        print("Warning, fonts disabled")
    if not pg.mixer:
        print("Warning, sound disabled")

    ### Load Images
    playerRight5 = pg.image.load("images/playerRight5.jpg").convert()
    logo = pg.image.load("images/logo.jpg").convert()
    logo = pg.transform.scale(logo, (400,320))



    ### Game loop
    running = True
    screenState = "welcome"
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                raise SystemExit


        ### Update states and logic
        # screenState = welcome -> intro screen
        # screenState = options -> new game / load game screen
        updateState()


        ### Update Graphics
        if screenState == "welcome":
            pg.Surface.fill(screen, (255,255,255))
            pg.Surface.blit(screen, logo, (120,0))

        #pg.Surface.blit(screen, playerRight5, (100,100))

        pg.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    main()
    
