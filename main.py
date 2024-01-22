import time
import random
import pygame
pygame.font.init()
WIDTH, HEIGHT = 1000, 800

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Dodge")

# one way of doing it if you know the image fits the screen
bgImage = pygame.image.load("bg.jpg")
# another way to do it to scale an image to the window if it doesn't fit
BG = pygame.transform.scale(bgImage, (WIDTH, HEIGHT))

PLAYER_WIDTH = 40
PLAYER_HEIGHT = 60
PLAYER_VELOCITY = 5
STAR_WIDTH = 10
STAR_HEIGHT = 10
STAR_VELOCITY = 3
FONT = pygame.font.SysFont("Impact", 30)


def draw(player, elapsed_time, stars):
    # pygame way of setting a background image: paras are (image, coordinates you want the image to be placed) top left corner of image at the coord
    WIN.blit(BG, (0, 0))
    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
    WIN.blit(time_text, (10, 10))
    pygame.draw.rect(WIN, "red", player)  # drawing the player 'character'

    for star in stars:
        pygame.draw.rect(WIN, "white", star)

    pygame.display.update()

# main game loop


def main():
    run = True
    player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT,
                         PLAYER_WIDTH, PLAYER_HEIGHT)

    clock = pygame.time.Clock()  # game clock aka fps

    start_time = time.time()
    elapsed_time = 0

    # projectiles
    star_add_increment = 2000
    star_count = 0
    stars = []
    hit = False

    while run:
        clock.tick(60)  # 60ish fps
        elapsed_time = time.time() - start_time

        star_count += clock.tick(60)
        if star_count > star_add_increment:
            for _ in range(3):
                star_x = random.randint(0, WIDTH-STAR_WIDTH)
                star = pygame.Rect(star_x, -STAR_HEIGHT,
                                   STAR_WIDTH, STAR_HEIGHT)
                stars.append(star)

            star_add_increment = max(200, star_add_increment - 50)
            star_count = 0

        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                run = False
                break
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - PLAYER_VELOCITY >= 0:
            player.x -= PLAYER_VELOCITY
        if keys[pygame.K_RIGHT] and player.x + PLAYER_VELOCITY + player.width <= WIDTH:
            player.x += PLAYER_VELOCITY

        for star in stars[:]:
            star.y += STAR_VELOCITY
            if star.y > HEIGHT:
                stars.remove(star)
            elif star.y + STAR_HEIGHT >= player.y and star.colliderect(player):
                stars.remove(star)
                hit = True
                break

        if hit:
            lost_text = FONT.render("You lose!", 1, "white")
            WIN.blit(lost_text, (WIDTH/2 - lost_text.get_width() /
                     2, HEIGHT/2 - lost_text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(4000)
            break
        draw(player, elapsed_time, stars)

    pygame.quit()


if __name__ == "__main__":
    main()
