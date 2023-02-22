import pygame as pg


def main():
    pg.init()
    screen = pg.display.set_mode((640,480))
    clock = pg.time.Clock()

    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                raise SystemExit

        # Logical Updates here

        # Render Graphics Here

        pg.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    main()
