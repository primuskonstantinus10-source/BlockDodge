import pygame
import time
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("spaceshot")

BG = pygame.transform.scale(pygame.image.load("space1.jpg"), (WIDTH, HEIGHT))

PLAYER_WIDTH = 40
PLAYER_HEIGHT = 80


def draw(player):
    WIN.blit(BG, (0, 0))

    pygame.draw.rect(WIN, (255, 0, 0), player)


def main():

    player = pygame.Rect(200, HEIGHT-PLAYER_HEIGHT,
                         PLAYER_WIDTH, PLAYER_HEIGHT)

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        draw(player)
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
