import pygame
import os

pygame.font.init()


WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("First Game!")
FPS = 60
BG_COLOUR = (33,43,253)
BLACK = (0,0,0)
LEBRON_WIDTH,LEBRON_HEIGHT = 160,180
CURRY_WIDTH,CURRY_HEIGHT=110,170
BORDER = pygame.Rect(WIDTH // 2 - 5, 0, 10, HEIGHT) # (x-position, y-position, width, height)
VEL = 7
YELLOW = (239, 235, 15 )
RED = (255, 0, 0 )



YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2


HEALTH_FONT = pygame.font.SysFont('comicsans',40)

YELLOW_SPACESHIP_IMAGE = pygame.image.load(
            os.path.join('Picture', 'lebron_new.png'))
YELLOW_SPACESHIP = pygame.transform.flip(pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (LEBRON_WIDTH, LEBRON_HEIGHT)), 0),True,False)


RED_SPACESHIP_IMAGE = pygame.image.load(
            os.path.join('Picture', 'curry_new.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (CURRY_WIDTH, CURRY_HEIGHT)), 0)

BULLET_IMAGE = pygame.image.load(
    os.path.join('Picture', 'basketball.png'))
BULLET = pygame.transform.rotate(
    pygame.transform.scale(BULLET_IMAGE,
                           (50,50)), 90)
COURT = pygame.transform.scale(
    pygame.image.load(os.path.join('Picture', 'court.jpg')), (WIDTH, HEIGHT))
def handle_yellow_movement(keys_pressed,yellow):
    if keys_pressed[pygame.K_w] and yellow.y - VEL > -5:
        yellow.y = yellow.y - VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL < 400:
        yellow.y = yellow.y + VEL
    if keys_pressed[pygame.K_a] and yellow.x - VEL > -5:
        yellow.x = yellow.x - VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL < 365:
        yellow.x = yellow.x + VEL

def handle_red_movement(keys_pressed,red):
    if keys_pressed[pygame.K_UP] and red.y - VEL > -5:
        red.y = red.y - VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL < 400:
        red.y = red.y + VEL
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > 455:
        red.x = red.x - VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL < 825:
        red.x = red.x + VEL

def main():
    yellow_health = 10
    red_health = 10
    clock = pygame.time.Clock()
    yellow = pygame.Rect(0, HEIGHT//2 -LEBRON_HEIGHT/2, LEBRON_WIDTH, LEBRON_HEIGHT)#(side wall position,top bottom wall position,length,height)
    red = pygame.Rect(720, HEIGHT//2-CURRY_HEIGHT/2, CURRY_WIDTH, CURRY_HEIGHT)
    yellow_bullets = []
    red_bullets = []
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LSHIFT and len(yellow_bullets) < 6:
                    yellow_bullet = pygame.Rect(yellow.x + 80,yellow.y + 50,10,5)
                    yellow_bullets.append(yellow_bullet)
                if event.key == pygame.K_RSHIFT and len(red_bullets) < 6:
                    red_bullet = pygame.Rect(red.x, red.y + 50, 10, 5)
                    red_bullets.append(red_bullet)

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                # if yellow_health <= 0:
                #     yellow_lose_text= HEALTH_FONT.render('YOU LOSE', 1, YELLOW)
                #     WIN.blit(yellow_lose_text, (450,225))
                #     pygame.display.update()
                #     pygame.time.delay(5000)
                #     break

            if event.type == RED_HIT:
                red_health -= 1

            if event.type == pygame.QUIT:
                run = False

                pygame.quit()

        winner_text = ""
        if yellow_health <= 0:
            winner_text = "CURRY WINS!"

        if red_health <= 0:
            winner_text = "LEBRON WINS!"

        if winner_text == "CURRY WINS!":
            red_winner_text = HEALTH_FONT.render(winner_text, 1 , RED)
            WIN.blit(red_winner_text, (450 - red_winner_text.get_width()/2,250 - red_winner_text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(5000)
            break

        if winner_text == "LEBRON WINS!":
            yellow_winner_text = HEALTH_FONT.render(winner_text, 1, YELLOW)
            WIN.blit(yellow_winner_text, (450 - yellow_winner_text.get_width() / 2, 250 - yellow_winner_text.get_height() / 2))
            pygame.display.update()
            pygame.time.delay(5000)
            break

        keys_pressed = pygame.key.get_pressed()
        handle_yellow_movement(keys_pressed,yellow)
        handle_red_movement(keys_pressed,red)

        WIN.fill(BG_COLOUR)
        WIN.blit(COURT,(0,0))
        WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y)) #(x,y)
        WIN.blit(RED_SPACESHIP, (red.x, red.y)) #(x,y)
        pygame.draw.rect(WIN, BLACK, BORDER)

        #Draw health







        for bullet in yellow_bullets:
            bullet.x += 10
            WIN.blit(BULLET,bullet)
            if red.colliderect(bullet):
                pygame.event.post(pygame.event.Event(RED_HIT))
                yellow_bullets.remove(bullet)
            if bullet.x > 900:
                yellow_bullets.remove(bullet)

        for bullet in red_bullets:
            bullet.x -= 10
            WIN.blit(BULLET,bullet)
            if yellow.colliderect(bullet):
                pygame.event.post(pygame.event.Event(YELLOW_HIT))
                red_bullets.remove(bullet)
            if bullet.x < 0:
                red_bullets.remove(bullet)

        yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, YELLOW)
        WIN.blit(yellow_health_text, (7, 0))

        red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, RED)
        WIN.blit(red_health_text, (700, 0))

        pygame.display.update()
    main()










if __name__ == "__main__":
    pygame.init()
    main()
