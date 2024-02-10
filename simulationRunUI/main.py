from menuUI import *
import pygame as pg

def main():
    pg.init()
    currentMenu=menu((1200,700), False)
    currentMenu.run()

if __name__=="__main__":
    main()


