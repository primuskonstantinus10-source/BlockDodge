import pygame
import time
import random
pygame.font.init()

pygame.init()

WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("spaceshot")

BG = pygame.transform.scale(pygame.image.load("space2.jpg"), (WIDTH, HEIGHT))

PLAYER_WIDTH = 20
PLAYER_HEIGHT = 20

player_vel = 5
enemy_width = 10
enemy_height = 10
enemy_vel = 3*random.uniform(0.5, 2)

bullet_width = 5
bullet_height = 10
bullet_vel = 7

enemy_bullet_width = 3
enemy_bullet_height = 5
enemy_bullet_vel = 5

FONT = pygame.font.SysFont("comicsans", 30)


def draw(player, enemies, bullets, enemy_bullets, elapsed_time):
    WIN.blit(BG, (0, 0))

    time_text = FONT.render(
        f"Time: {round(elapsed_time)}s", 1, (255, 255, 255))
    WIN.blit(time_text, (5, 5))

    pygame.draw.rect(WIN, (255, 0, 0), player)

    for e in enemies:
        pygame.draw.rect(WIN, (255, 255, 0), e)

    for b in bullets:
        pygame.draw.rect(WIN, (255, 255, 255), b)

    for eb in enemy_bullets:
        pygame.draw.rect(WIN, (255, 255, 255), eb)


def game_loop():
    # all local state setup
    player = pygame.Rect(200, HEIGHT-PLAYER_HEIGHT,
                         PLAYER_WIDTH, PLAYER_HEIGHT)
    clock = pygame.time.Clock()

    start_time = time.time()
    elapsed_time = 0

    enemy_add_increment = 2000
    enemy_timer = 0
    enemies = []
    bullets = []
    enemy_bullets = []

    game_over = False
    run = True
    while run:
        dt = clock.tick(60)
        enemy_timer += dt
        elapsed_time = time.time() - start_time

        if not game_over and enemy_timer >= enemy_add_increment:
            enemy_timer = 0
            for _ in range(10):
                star_x = random.randint(0, WIDTH - enemy_width)
                star_speed = random.uniform(2, 6)
                enemies.append((pygame.Rect(star_x, -enemy_height,
                                            enemy_width, enemy_height), star_speed))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            if game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                return True  # restart requested

        if not game_over:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and player.x - player_vel > 0:
                player.x -= player_vel
            if keys[pygame.K_RIGHT] and player.x + player_vel < WIDTH - PLAYER_WIDTH:
                player.x += player_vel

            if keys[pygame.K_SPACE]:
                bullet = pygame.Rect(
                    player.centerx - bullet_width//2, player.y, bullet_width, bullet_height)
                bullets.append((bullet, bullet_vel))

            # move enemies down and check collisions
            new_enemies = []
            for enemy, speed in enemies:
                enemy.y += speed
                if enemy.y > HEIGHT:
                    continue
                if enemy.y > 0 and random.random() < 0.005:
                    enemy_bullet = pygame.Rect(
                        enemy.centerx - enemy_bullet_width//2, enemy.y + enemy_height, enemy_bullet_width, enemy_bullet_height)
                    enemy_bullets.append((enemy_bullet, enemy_bullet_vel))
                if enemy.colliderect(player):
                    game_over = True
                    break
                new_enemies.append((enemy, speed))
            enemies = new_enemies

            # move bullets up and check collisions with enemies
            new_bullets = []
            for bullet, speed in bullets:
                bullet.y -= speed
                if bullet.y < 0:
                    continue
                hit_enemy = False
                new_enemies_temp = []
                for enemy, e_speed in enemies:
                    if bullet.colliderect(enemy):
                        hit_enemy = True
                    else:
                        new_enemies_temp.append((enemy, e_speed))
                hit_eb = False
                new_eb_temp = []
                for eb, eb_speed in enemy_bullets:
                    if bullet.colliderect(eb):
                        hit_eb = True
                    else:
                        new_eb_temp.append((eb, eb_speed))
                if hit_enemy or hit_eb:
                    if hit_enemy:
                        enemies = new_enemies_temp
                    if hit_eb:
                        enemy_bullets = new_eb_temp
                else:
                    new_bullets.append((bullet, speed))
            bullets = new_bullets

            # move enemy bullets down and check collisions with player
            new_enemy_bullets = []
            for eb, speed in enemy_bullets:
                eb.y += speed
                if eb.y > HEIGHT:
                    continue
                if eb.colliderect(player):
                    game_over = True
                    break
                new_enemy_bullets.append((eb, speed))
            enemy_bullets = new_enemy_bullets

        # render
        draw(player, [e for e, _ in enemies], [
             b for b, _ in bullets], [eb for eb, _ in enemy_bullets], elapsed_time)

        if game_over:
            go_text = FONT.render(
                "Game Over! Press R to restart", True, (255, 255, 255))
            WIN.blit(go_text, (WIDTH // 2 -
                     go_text.get_width() // 2, HEIGHT // 2 - 20))

        pygame.display.update()

    return False  # quit


def main():
    pygame.init()
    while True:
        restart = game_loop()
        if not restart:
            break
    pygame.quit()


if __name__ == "__main__":
    main()
