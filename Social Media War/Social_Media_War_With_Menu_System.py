import pygame
import random

# Initialize Pygame modules
pygame.font.init()
pygame.mixer.init()

# Set up the display
Gamedispley = pygame.display.set_mode((900, 500))
pygame.display.set_caption('Social Media Wars')

# Define colors
white = (255, 255, 255)
black = (0, 0, 0)
blueco = (0, 0, 255)
pinkco = (255, 20, 147)

# Game settings
FPS = 60
velocity = 5
bullvel = 10
max_bullets = 3

# Load sounds
HitSound = pygame.mixer.Sound('Hit_sound.mp3')
FireSound = pygame.mixer.Sound('Fire_sound.mp3')  # Adjusted sound handling

# Load fonts
Healthfont = pygame.font.SysFont('comicsans', 20)
Winnerfont = pygame.font.SysFont('comicsans', 100)
Menufont = pygame.font.SysFont('comicsans', 60)

# Load images
BG9 = pygame.transform.scale(pygame.image.load('Background.png'), (900, 500))
Player1 = pygame.image.load('Facebook.png')
Player2 = pygame.image.load("Instagram.png")
Facebook = pygame.transform.scale(Player1, (40, 40))
Instagram = pygame.transform.scale(Player2, (40, 40))

# Custom events for hits
bluehit = pygame.USEREVENT + 1
pinkhit = pygame.USEREVENT + 2

# Border
Border = pygame.Rect(445, 0, 10, 500)

# AI settings
ai_fire_prob = 0.02  # Probability of AI firing each frame


def ddraw(blue, pink, bluebullets, pinkbullets, hpfb, hpig):
    Gamedispley.blit(BG9, (0, 0))
    pygame.draw.rect(Gamedispley, black, Border)

    fbhelthtext = Healthfont.render("Health: " + str(hpfb), 1, white)
    ighelthtext = Healthfont.render("Health: " + str(hpig), 1, white)
    Gamedispley.blit(fbhelthtext, (10, 10))
    Gamedispley.blit(ighelthtext, (900 - ighelthtext.get_width() - 10, 10))

    Gamedispley.blit(Facebook, (blue.x, blue.y))
    Gamedispley.blit(Instagram, (pink.x, pink.y))

    for b in bluebullets:
        pygame.draw.rect(Gamedispley, blueco, b)
    for b in pinkbullets:
        pygame.draw.rect(Gamedispley, pinkco, b)

    pygame.display.update()


def movementsblue(keysthatarepressedrn, blue):
    if keysthatarepressedrn[pygame.K_a] and blue.x > 0:
        blue.x -= velocity
    if keysthatarepressedrn[pygame.K_d] and blue.x < 400:
        blue.x += velocity
    if keysthatarepressedrn[pygame.K_w] and blue.y > 0:
        blue.y -= velocity
    if keysthatarepressedrn[pygame.K_s] and blue.y < 460:
        blue.y += velocity


def movementspink(keysthatarepressedrn, pink):
    if keysthatarepressedrn[pygame.K_LEFT] and pink.x > 460:
        pink.x -= velocity
    if keysthatarepressedrn[pygame.K_RIGHT] and pink.x < 860:
        pink.x += velocity
    if keysthatarepressedrn[pygame.K_UP] and pink.y > 0:
        pink.y -= velocity
    if keysthatarepressedrn[pygame.K_DOWN] and pink.y < 460:
        pink.y += velocity


def handlebullets(bluebullets, pinkbullets, blue, pink):
    for bullet in bluebullets:
        bullet.x += bullvel
        if pink.colliderect(bullet):
            pygame.event.post(pygame.event.Event(pinkhit))
            bluebullets.remove(bullet)
        elif bullet.x > 900:
            bluebullets.remove(bullet)

    for bullet in pinkbullets:
        bullet.x -= bullvel
        if blue.colliderect(bullet):
            pygame.event.post(pygame.event.Event(bluehit))
            pinkbullets.remove(bullet)
        elif bullet.x < 0:
            pinkbullets.remove(bullet)


def winner(text):
    draw = Winnerfont.render(text, 1, white)
    Gamedispley.blit(draw, (450 - draw.get_width() // 2, 250 - draw.get_height() // 2))
    pygame.display.update()
    pygame.time.delay(2000)


def start_menu():
    menu = True
    mode = None
    while menu:
        Gamedispley.fill(black)
        title = Menufont.render('Social Media Wars', True, white)
        single_player = Healthfont.render('Press 1 for Single Player', True, white)
        two_player = Healthfont.render('Press 2 for Two Player', True, white)
        quit_game = Healthfont.render('Press Q to quit', True, white)

        Gamedispley.blit(title, (900 // 2 - title.get_width() // 2, 150))
        Gamedispley.blit(single_player, (900 // 2 - single_player.get_width() // 2, 300))
        Gamedispley.blit(two_player, (900 // 2 - two_player.get_width() // 2, 350))
        Gamedispley.blit(quit_game, (900 // 2 - quit_game.get_width() // 2, 400))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    exit()
                elif event.key == pygame.K_1:
                    mode = 'single'
                    menu = False
                elif event.key == pygame.K_2:
                    mode = 'two'
                    menu = False
    return mode


def ai_movement(pink):
    if pink.y < 460 and random.random() < 0.5:
        pink.y += velocity
    elif pink.y > 0:
        pink.y -= velocity


def ai_fire(pink, pinkbullets):
    if len(pinkbullets) < max_bullets and random.random() < ai_fire_prob:
        bullet = pygame.Rect(pink.x, pink.y + 20 - 2, 6, 4)
        pinkbullets.append(bullet)
        FireSound.play()


def end_game_menu():
    menu = True
    choice = None
    while menu:
        Gamedispley.fill(black)
        rematch = Healthfont.render('Press R for Rematch', True, white)
        start_menu_option = Healthfont.render('Press M for Main Menu', True, white)
        quit_game = Healthfont.render('Press Q to quit', True, white)

        Gamedispley.blit(rematch, (900 // 2 - rematch.get_width() // 2, 300))
        Gamedispley.blit(start_menu_option, (900 // 2 - start_menu_option.get_width() // 2, 350))
        Gamedispley.blit(quit_game, (900 // 2 - quit_game.get_width() // 2, 400))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    exit()
                elif event.key == pygame.K_r:
                    choice = 'rematch'
                    menu = False
                elif event.key == pygame.K_m:
                    choice = 'main_menu'
                    menu = False
    return choice


def main():
    while True:
        mode = start_menu()  # Display the start menu before the game starts

        blue = pygame.Rect(280, 230, 40, 40)
        pink = pygame.Rect(580, 230, 40, 40)
        hpfb = 5
        hpig = 5
        bluebullets = []
        pinkbullets = []

        clockk = pygame.time.Clock()
        run = True
        while run:
            clockk.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LCTRL and len(bluebullets) < max_bullets:
                        bullet = pygame.Rect(blue.x + blue.width, blue.y + 20 - 2, 6, 4)
                        bluebullets.append(bullet)
                        FireSound.play()  # Adjusted sound play
                    if mode == 'two' and event.key == pygame.K_RCTRL and len(pinkbullets) < max_bullets:
                        bullet = pygame.Rect(pink.x, pink.y + 20 - 2, 6, 4)
                        pinkbullets.append(bullet)
                        FireSound.play()  # Adjusted sound play
                if event.type == bluehit:
                    hpfb -= 1
                    HitSound.play()
                if event.type == pinkhit:
                    hpig -= 1
                    HitSound.play()

            wintext = ""
            if hpfb <= 0:
                wintext = 'Instagram Wins!'
            if hpig <= 0:
                wintext = 'Facebook Wins!'
            if wintext != "":
                winner(str(wintext))
                choice = end_game_menu()  # Display end game menu
                if choice == 'rematch':
                    break  # Restart the game loop
                elif choice == 'main_menu':
                    main()  # Go back to the main menu

            keysthatarepressedrn = pygame.key.get_pressed()
            movementspink(keysthatarepressedrn, pink)
            movementsblue(keysthatarepressedrn, blue)

            handlebullets(bluebullets, pinkbullets, blue, pink)

            ddraw(blue, pink, bluebullets, pinkbullets, hpfb, hpig)

            if mode == 'single':
                ai_movement(pink)
                ai_fire(pink, pinkbullets)

    pygame.quit()


if __name__ == "__main__":
    main()
