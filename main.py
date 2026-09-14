import pygame
from game import Game

def main():
    pygame.init()
    juego = Game(num_humans=2, num_ais=0)
    juego.run()

if __name__ == "__main__":
    main()