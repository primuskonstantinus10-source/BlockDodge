import pygame
import time
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("spaceshot")

BG = pygame.transform.scale(pygame.image.load("space1.jpg"), (WIDTH, HEIGHT))


def draw():
    WIN.blit(BG, (0, 0))


def main():
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        draw()
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
