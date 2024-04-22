import pygame
#import os
pygame.font.init()
pygame.mixer.init()

Gamedispley = pygame.display.set_mode((900,500))
pygame.display.set_caption('Social Media War')

white = (255,255,255)
black = (0,0,0)
blueco =  (0, 0, 255)
pinkco = (255, 20, 147)

FPS = 60
velocity = 5
bullvel = 10
max_bullets = 3

HitSound = pygame.mixer.Sound('Hit_sound.mp3')
FireSound = pygame.mixer.music.load(r'C:\Users\HP\Desktop\Social Media War\Fire_sound.mp3')

Healthfont = pygame.font.SysFont('comicsans', 20)
Winnerfont = pygame.font.SysFont('comicsans', 100)
#Bg123 =
BG9 = pygame.transform.scale(pygame.image.load('BG2.png'), (900,500))

bluehit = pygame.USEREVENT + 1
pinkhit = pygame.USEREVENT + 2

Border = pygame.Rect(445, 0, 10, 500)       #Capital rect surface create krne k kaam ata h - code


Player1 = pygame.image.load(r'C:\Users\HP\Desktop\Social Media War\Facebook.png')
Player2 = pygame.image.load("Instagram.png") #if doesnt work than try os.path.join("PygameModuleYippee", "Facebook.png")

Facebok = pygame.transform.scale(Player1, (40, 40))
Facebook = pygame.transform.rotate(Facebok, 0)
Instagram = pygame.transform.scale(Player2, (40,40))



def drawkaro(blue, pink, bluebullets, pinkbullets, hpfb, hpig): #called the draw window
    #Gamedispley.fill(white)
    Gamedispley.blit(BG9, (0,0))
    pygame.draw.rect(Gamedispley, black, Border)    #small rect surface draw krne k kaam ata h - graphic

    fbhelthtext = Healthfont.render("Health: " + str(hpfb), 1, white)
    ighelthtext = Healthfont.render("Health: " + str(hpig), 1, white)
    Gamedispley.blit(fbhelthtext, (10,10))
    Gamedispley.blit(ighelthtext, (900-ighelthtext.get_width() -10,10))

    Gamedispley.blit(Facebook, (blue.x, blue.y))
    Gamedispley.blit(Instagram, (pink.x, pink.y))

    for b in bluebullets:
        pygame.draw.rect(Gamedispley, blueco, b)
    for b in pinkbullets:
        pygame.draw.rect(Gamedispley, pinkco, b)

    pygame.display.update()                  #so what happemned was ki i update pehle then drew objects so it was all waste, so in general, updtae as last as possible

def movementsblue(keysthatarepressedrn, blue):
    if keysthatarepressedrn[pygame.K_a] and blue.x >0:
        blue.x -= velocity
    if keysthatarepressedrn[pygame.K_d] and blue.x <400 :
        blue.x += velocity
    if keysthatarepressedrn[pygame.K_w] and blue.y >0:
        blue.y -= velocity
    if keysthatarepressedrn[pygame.K_s]and blue.y <460:
        blue.y += velocity

def movementspink(keysthatarepressedrn, pink):
    if keysthatarepressedrn[pygame.K_LEFT] and pink.x > 460:
        pink.x -= velocity
    if keysthatarepressedrn[pygame.K_RIGHT] and pink.x <860:
        pink.x += velocity
    if keysthatarepressedrn[pygame.K_UP] and pink.y >0:
        pink.y -= velocity
    if keysthatarepressedrn[pygame.K_DOWN] and pink.y <460:
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
        elif bullet.x <0:
            pinkbullets.remove(bullet)

def winner(text):
    draw = Winnerfont.render(text, 1, white)
    Gamedispley.blit(draw, (450-draw.get_width()//2, 250 - draw.get_height()//2))
    pygame.display.update()
    pygame.time.delay(5000)

def main():
    blue = pygame.Rect(280,230, 40, 40)     #take 4 arguements, firstthe location of origin, (x,y), then the dimensions (width, height) png suited besht
    pink = pygame.Rect(580, 230, 40 ,40)
    hpfb = 5
    hpig = 5
    bluebullets = []
    pinkbullets =[]

    clockk = pygame.time.Clock()
    run =True
    while run:
        clockk.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()   #ye fxn pehle neeche tha lekin ab victory assure krne k baad upar aa gaya

            if event.type == pygame.KEYDOWN:
                if event.key ==  pygame.K_LCTRL and len(bluebullets) <max_bullets:
                    bullet = pygame.Rect(blue.x + blue.width, blue.y + 20 -2, 6,4)
                    bluebullets.append(bullet)
                    pygame.mixer.music.play()
                if event.key == pygame.K_RCTRL and len(pinkbullets) <max_bullets:
                    bullet = pygame.Rect(pink.x, pink.y + 20 - 2, 6, 4)
                    pinkbullets.append(bullet)
                    pygame.mixer.music.play()
            if event.type == bluehit:
                hpfb -= 1
                HitSound.play()
            if event.type == pinkhit:
                hpig -= 1
                HitSound.play()
        wintext = ""
        if hpfb<=0:
            wintext = 'Instagram Wins!'
        if hpig<=0:
            wintext = 'Facebook Wins!'
        if wintext != "":
            winner(str(wintext))
            break

        #print(bluebullets, pinkbullets)
        keysthatarepressedrn = pygame.key.get_pressed()
        movementspink(keysthatarepressedrn, pink)
        movementsblue(keysthatarepressedrn, blue)

        handlebullets(bluebullets, pinkbullets, blue, pink)

        drawkaro(blue, pink, bluebullets, pinkbullets, hpfb, hpig)

    main()
    #pygame.quit() #agar koi bhi ek baar bhi jeeta to ye game khatam yahi pr, lekin agar main h to ye pygame.quit upar aa jaega

#if __name__ == "__main__":  #important h, but when there are multiple files
main()