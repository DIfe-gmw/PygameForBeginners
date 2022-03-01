import pygame, os, time
pygame.font.init()
pygame.mixer.init()

options = {
    'WIDTH': 900, # NOT RECOMMENDED TO CHANGE
    'HEIGHT': 600, # NOT RECOMMENDED TO CHANGE
    'CAPTION': 'Batalha Espacial',
    'FPS': 60,
    'SPACESHIP_SIZE': (55, 40),
    'SPEED': 5,
    'BULLET_SPEED': 7, 
    'MAX_BULLETS': 4, 
    'RED_HEALTH': 10,
    'YELLOW_HEALTH': 10,
    'HEALTH_FONT': pygame.font.SysFont('comicsans', 40),
    'WINNER_FONT': pygame.font.SysFont('comicsans', 100)
}

colors = {
    'WHITE': (255, 255, 255),
    'BLACK': (0, 0, 0),
    'RED': (255, 0, 0),
    'YELLOW': (255, 255, 0),
    'TRANSPARENT': (0, 0, 0, 0),
}

sound_effects = {
    'BULLET_HIT_SOUND': pygame.mixer.Sound(os.path.join('assets', 'Grenade+1.mp3')),
    'BULLET_FIRE_SOUND': pygame.mixer.Sound(os.path.join('assets', 'Gun+Silencer.mp3')),
}

BORDER = pygame.Rect(options['WIDTH']//2 + 5, 0, 10, options['HEIGHT'])
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2
WIN = pygame.display.set_mode((options['WIDTH'], options['HEIGHT']))
pygame.display.set_caption(options['CAPTION'])

RED_SPACESHIP_IMG = pygame.image.load(os.path.join('assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMG, options['SPACESHIP_SIZE']), 90)

YELLOW_SPACESHIP_IMG = pygame.image.load(os.path.join('assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMG, options['SPACESHIP_SIZE']), 270)

SPACE = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'bg.png')), (options['WIDTH'], options['HEIGHT']))

def handle_movement(keys_pressed, red, yellow):
    if keys_pressed[pygame.K_a] and red.x - options['SPEED'] > 0: # Left
        red.x -= options['SPEED']
    if keys_pressed[pygame.K_d] and red.x + options['SPEED'] + options['SPACESHIP_SIZE'][0] < BORDER.x: # Right
        red.x += options['SPEED']
    if keys_pressed[pygame.K_w] and red.y - options['SPEED'] > 0: # Up
        red.y -= options['SPEED']
    if keys_pressed[pygame.K_s] and red.y + options['SPEED'] + options['SPACESHIP_SIZE'][1] < options['HEIGHT'] - 15: # Down
        red.y += options['SPEED']

    if keys_pressed[pygame.K_LEFT] and yellow.x - options['SPEED'] > BORDER.x + BORDER.width: # Left
        yellow.x -= options['SPEED']
    if keys_pressed[pygame.K_RIGHT] and yellow.x + options['SPEED'] + options['SPACESHIP_SIZE'][0] < options['WIDTH']: # Right
        yellow.x += options['SPEED']
    if keys_pressed[pygame.K_UP] and yellow.y - options['SPEED'] > 0: # Up
        yellow.y -= options['SPEED']
    if keys_pressed[pygame.K_DOWN] and yellow.y + options['SPEED'] + options['SPACESHIP_SIZE'][1] < options['HEIGHT'] - 15: # Down
        yellow.y += options['SPEED']

def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    WIN.blit(SPACE, (0,0))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))

    red_health_text = options['HEALTH_FONT'].render("Vida: " + str(red_health), 1, colors['WHITE'])
    yellow_health_text = options['HEALTH_FONT'].render("Vida: " + str(yellow_health), 1, colors['WHITE'])

    WIN.blit(red_health_text, (10,10))
    WIN.blit(yellow_health_text, (options['WIDTH'] - yellow_health_text.get_width() - 10, 10))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, colors['RED'], bullet)
    
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, colors['YELLOW'], bullet)
    pygame.display.update()

def draw_winner(text):
    draw_text = options['WINNER_FONT'].render(text, 1, colors['WHITE'])
    WIN.blit(draw_text, (options['WIDTH']/2 - draw_text.get_width()/2, options['HEIGHT']/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)
    pygame.quit()


def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in red_bullets:
        bullet.x += options['BULLET_SPEED']
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x > options['WIDTH']:
            red_bullets.remove(bullet)

    for bullet in yellow_bullets:
        bullet.x -= options['BULLET_SPEED']
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x < 0:
            yellow_bullets.remove(bullet)

def main():
    red = pygame.Rect(100, 300, options['SPACESHIP_SIZE'][0], options['SPACESHIP_SIZE'][1])
    yellow = pygame.Rect(700, 300, options['SPACESHIP_SIZE'][0], options['SPACESHIP_SIZE'][1])

    red_bullets = []
    yellow_bullets = []

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(options['FPS'])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(red_bullets) < options['MAX_BULLETS']:
                    bullet = pygame.Rect(red.x + red.width - 5, red.y + red.height//2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    sound_effects['BULLET_FIRE_SOUND'].play().set_volume(0.2)
                    
                if event.key == pygame.K_RCTRL and len(yellow_bullets) < options['MAX_BULLETS']:
                    bullet = pygame.Rect(yellow.x, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    sound_effects['BULLET_FIRE_SOUND'].play().set_volume(0.2)

            if event.type == RED_HIT:
                options['RED_HEALTH'] -= 1
                sound_effects['BULLET_HIT_SOUND'].play().set_volume(0.2)

            if event.type == YELLOW_HIT:
                options['YELLOW_HEALTH'] -= 1
                sound_effects['BULLET_HIT_SOUND'].play().set_volume(0.2)

        winner_text = ""
        if options['RED_HEALTH'] <= 0:
            winner_text = "Amarelo ganhou!"

        if options['YELLOW_HEALTH'] <= 0:
            winner_text = "Vermelho ganhou!"

        if winner_text != "":
            draw_winner(winner_text)
            break;

        keys_pressed = pygame.key.get_pressed()
        handle_movement(keys_pressed, red, yellow)
        draw_window(red, yellow, red_bullets, yellow_bullets, options['RED_HEALTH'], options['YELLOW_HEALTH'])
        handle_bullets(yellow_bullets, red_bullets, yellow, red)

    main()

if __name__ == '__main__':
    main()