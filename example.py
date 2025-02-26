 # 출처:https://opentutorials.org/course/3045
 # 이외의 내용은 pygame documentation을 참고함.
 #111
 #
import pygame, math
import sys
import time


pre_time = time.time()
pree_time = time.time()
pre2_time=time.time()
total_time=time.time()
TEXTCOLOR = (255, 255, 255)


class Mundo:
    def __init__(self, x, y):
        self.health = 100
        self.strength = 50
        self.armor = 100
        self.healthregen = 5
        self.cooltime_limit = 2.0
        self.arrows = []
        self.spell1type = 1
        self.spell1cool = 5
        self.spell2type = 2
        self.spell2cool = 10
        self.spelllist=[0,"flash","heal","ghost"]
        self.speed=3
        self.x = x
        self.y = y

    def move(self, k0, k1, k2, k3,ty):  # wasd로 움직임
        if ty==1:
            if k0:
                if 23 <= self.y - self.speed <= 240 - 23:
                    self.y = self.y - self.speed
            elif k2:
                if 23 <= self.y + self.speed <= 240 - 23:
                    self.y = self.y + self.speed
        elif ty==2:
            if k0:
                if 240+23<=self.y-self.speed<=480-23:
                    self.y=self.y-self.speed
            elif k2:
                if 240+23<=self.y+self.speed<=480-23:
                    self.y=self.y+self.speed
        if k1:
            if 32 <= self.x - self.speed <= 640 - 32:
                self.x = self.x - self.speed
        elif k3:
            if 32 <= self.x + self.speed <= 640 - 32:
                self.x = self.x + self.speed

    def attack(self):  # 스킬을 사용
        position = pygame.mouse.get_pos()
        tmptime = time.time();
        self.arrows.append([math.atan2(position[1] - (self.y + 32), position[0] - (self.x + 26)), \
                            self.x + 26, self.y + 32])
        pygame.mixer.music.load('resources/audio/throw.mp3')
        pygame.mixer.music.play(0)
        return tmptime

    def spelluse(self,type): # 스펠을 사용
        returnlist=[]
        tmtime=time.time()
        if type=='r':
            returnlist=spelluses(self.x,self.y,self.spelllist[self.spell1type])
        if type=='f':
            returnlist=spelluses(self.x,self.y,self.spelllist[self.spell2type])
        self.x = returnlist[0]
        self.y = returnlist[1]
        if returnlist[2]=='heal':
            self.health+=20
        elif returnlist[2]=='ghost':
            self.speed=4

        return tmtime

    def injured(self, oppomundo):  # 공격받았을 때 체력이 깎임
        global pre2_time
        index1=0
        for bullet in oppomundo.arrows:
            bullrect = pygame.Rect(arrow.get_rect())
            bullrect.left = bullet[1]
            bullrect.top = bullet[2]
            tmpmundo = pygame.Rect(mundo.get_rect())
            tmpmundo.center=(self.x,self.y)
            if tmpmundo.colliderect(bullrect):
                self.health -= oppomundo.strength / self.armor * 100
                oppomundo.arrows.pop(index1)
                pygame.mixer.music.load('resources/audio/injured.mp3')
                pygame.mixer.music.play(0)
                pre2_time=time.time()
                self.speed=1
            if time.time()-pre2_time>=2 and self.speed!=4:
                self.speed=3
            index1+=1
        if time.time() - pre2_time >= 2 and self.speed!=4:
            self.speed = 3
def spelluses(mx,my,spelltype)->list:
    list = []
    if spelltype == "flash":
        posi = pygame.mouse.get_pos()
        angle = math.atan2(posi[1] - (my + 32), posi[0] - (mx + 26))
        if(my<=220 and (my+math.sin(angle)*100)>=220):
            list.append(mx+math.cos(angle)*100)
            list.append(220)
        if(my<=220 and (my+math.sin(angle)*100)<=220):
            list.append(mx+math.cos(angle)*100)
            list.append(my+math.sin(angle)*100)
        if(my>=260 and (my+math.sin(angle)*100)>=260):
            list.append(mx + math.cos(angle) * 100)
            list.append(my + math.sin(angle) * 100)
        if(my>=260 and (my+math.sin(angle)*100)<=260):
            list.append(mx + math.cos(angle) * 100)
            list.append(260)
        list.append("flash")
        pygame.mixer.music.load('resources/audio/flash.mp3')
        pygame.mixer.music.play(0)
    elif spelltype == "heal":
        list.append(mx)
        list.append(my)
        list.append("heal")
    elif spelltype == "ghost":
        list.append(mx)
        list.append(my)
        list.append("ghost")
    return list

def spellchoice(class1,flag):
    background = pygame.image.load("resources/images/background2.jpg")
    window.blit(background, (0, 0))
    pygame.display.update()
    if flag==1:
        draw_text("Choose attacker's spells.", font0, window, (width / 3) - 150, (height / 3))
    elif flag == 2:
        draw_text("Choose defender's spells.", font0, window, (width / 3) - 150, (height / 3))
    draw_text("1 :      flash  (cool 5)   teleport a little(direction: mouse cursor)", font1, window, (width / 3) - 150, (height / 3) + 50)
    draw_text("2 :      heal   (cool 10)   recover HP 20", font1, window, (width / 3) - 150, (height / 3) + 70)
    draw_text("3 :      ghost  (cool 20)  move faster until you hit", font1, window, (width / 3) - 150, (height / 3) + 90)
    pygame.display.update()
    count = 0
    choice = {1: 'flash', 2: 'heal', 3: 'ghost'}
    presslist = []
    while count < 2:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    presslist.append(1)
                    if count == 0:
                        class1.spell1type = 1
                        class1.spell1cool=5
                    elif count == 1:
                        class1.spell2type = 1
                        class1.spell2cool = 5
                    count += 1
                elif event.key == pygame.K_2:
                    presslist.append(2)
                    if count == 0:
                        class1.spell1type = 2
                        class1.spell1cool = 10
                    elif count == 1:
                        class1.spell2type = 2
                        class1.spell2cool = 10
                    count += 1
                elif event.key == pygame.K_3:
                    presslist.append(3)
                    if count == 0:
                        class1.spell1type = 3
                        class1.spell1cool = 20
                    elif count == 1:
                        class1.spell2type = 3
                        class1.spell2cool = 20
                    count += 1
    window.blit(background, (0, 0))
    draw_text("You chose two spells", font0, window, (width / 3) - 150, (height / 3))
    draw_text("Choice 1 : %s" % (choice[presslist[0]]), font1, window, (width / 3) - 150, (height / 3) + 50)
    draw_text("Choice 2 : %s" % (choice[presslist[1]]), font1, window, (width / 3) - 150, (height / 3) + 70)
    pygame.display.update()
    wait_for_key_pressed()

def basicscreenblit():
    screen.fill((0, 0, 0))  # R,G,B
    for x in range(width // grass.get_width() + 1):
        for y in range(height // grass.get_height() + 1):
            screen.blit(grass, (x * 100, y * 100))
    screen.blit(bush, (0, 30))
    screen.blit(bush, (0, 135))
    screen.blit(bush, (0, 240))
    screen.blit(bush, (0, 345))
    screen.blit(bush, (540, 30))
    screen.blit(bush, (540, 135))
    screen.blit(bush, (540, 240))
    screen.blit(bush, (540, 345))
    for x in range(width // wall.get_width() + 1):
        screen.blit(wall, (x * 40, 240))
    total_time = time.time();

def mundoblit(tmpmundo, pos,a):  # 문도의 상태 갱신
    angle = math.atan2(pos[1] - (tmpmundo.y + 32), pos[0] - (tmpmundo.x + 26))
    playerrot = pygame.transform.rotate(mundo, 360 - angle * 57.29)
    playerpos1 = (tmpmundo.x - playerrot.get_rect().width // 2, tmpmundo.y - playerrot.get_rect().height // 2)
    if a==0:
        if((tmpmundo.x - playerrot.get_rect().width // 2)>=95 and (tmpmundo.x - playerrot.get_rect().width // 2)<=500):
            screen.blit(playerrot, playerpos1)
        if((tmpmundo.y - playerrot.get_rect().height // 2)<=-5 or (tmpmundo.y - playerrot.get_rect().height // 2)>=410):
            screen.blit(playerrot, playerpos1)
    if a==1:
        screen.blit(playerrot, playerpos1)


def arrowblit(tmpmundo):  # 칼의 상태 갱신
    for bullet in tmpmundo.arrows:
        index = 0
        velx = math.cos(bullet[0]) * 7.5
        vely = math.sin(bullet[0]) * 7.5
        bullet[1] += velx
        bullet[2] += vely
        if bullet[1] < -64 or bullet[1] > 640 or bullet[2] < -64 or bullet[2] > 480:
            tmpmundo.arrows.pop(index)
        index = index + 1
    for projectile in tmpmundo.arrows:
        arrow1 = pygame.transform.rotate(arrow, 360 - projectile[0] * 57.29)
        screen.blit(arrow1, (projectile[1], projectile[2]))



def wait_for_key_pressed():  # 초기 화면 전환
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # When we press the "esc" key we're out of the game
                    exit_game()
                # When we press any key we leave the loop and the game continues.
                return


def draw_text(text, font, surface, x, y):  # 화면에 텍스트 입력
    text_obj = font.render(text, True, TEXTCOLOR)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(font.render(text, True, TEXTCOLOR), text_rect)


def exit_game():  # 게임 종료
    pygame.quit()
    sys.exit()


# 8번까지 구현함
pygame.init()
Mundo1 = Mundo(320.0, 100.0)
Mundo2 = Mundo(320.0, 400.0)
width, height = 640, 480
window = pygame.display.set_mode((width, height))
background = pygame.image.load("resources/images/background.jpg")
window.blit(background, (0, 0))
font0 = pygame.font.SysFont("Agency FB", 36)
font1 = pygame.font.SysFont("Liberation Serif", 24)
draw_text("MUNDO DODGEBALL", font0, window, (width / 3), (height / 3) + 100)
draw_text("press annie key to start!", font1, window, (width / 3), (height / 3) + 150)
draw_text("2019 OOP project by team MUNDO", font1, window, (width / 3) * 2 - 100, (height / 3) * 2 + 100)
pygame.display.update()
wait_for_key_pressed()
spellchoice(Mundo1,1)
spellchoice(Mundo2,2)
screen = pygame.display.set_mode((width, height))
mundo = pygame.image.load("resources/images/mundo.png")
grass = pygame.image.load("resources/images/grass.png")
bush = pygame.image.load("resources/images/bush.png")
arrow = pygame.image.load("resources/images/bullet.png")
wall = pygame.image.load("resources/images/wall.png")
healthbar =pygame.image.load("resources/images/healthbar.png")

keys1 = [False, False, False, False]
keys2 = [False, False, False, False]
check1=0
check2=0
check_time1=0
check_time2=0
check=1
check_time=0
pre3_time=time.time()
pre4_time=time.time()
pre5_time=time.time()
pre6_time=time.time()

while True:
    basicscreenblit()
    if(Mundo2.health>0):
        font2 = pygame.font.SysFont('Liberation Serif', 20)
        newhealth2 = pygame.transform.scale(healthbar, (int(Mundo2.health) * 2, 20))
        screen.blit(newhealth2, (220, 260))
        tm0=time.time() - pre_time
        tm1= time.time() - pre3_time
        tm2 = time.time() - pre4_time
        tm3 = time.time() - pre5_time
        tm4 = time.time() - pre6_time
        if tm0>=Mundo1.cooltime_limit:
            tm0=Mundo1.cooltime_limit
        if tm1>=Mundo1.spell1cool:
            tm1=Mundo1.spell1cool
        if tm2>=Mundo1.spell2cool:
            tm2=Mundo1.spell2cool
        if tm3>=Mundo2.spell1cool:
            tm3=Mundo2.spell1cool
        if tm4>=Mundo2.spell2cool:
            tm4=Mundo2.spell2cool
        tex0 = font2.render("q_cooltime", True, (0, 255, 255))
        tex1 = font2.render("r (spell1)", True, (255, 255, 255))
        tex2 = font2.render("f (spell2)", True, (255, 255, 255))
        tex3 = font2.render(", (spell1)", True, (255, 255, 255))
        tex4 = font2.render(". (spell2)", True, (255, 255, 255))
        q_cooltime = pygame.transform.scale(healthbar, (int((tm0) / Mundo1.cooltime_limit* 100) * 2, 20))
        Mundo1spell1 = pygame.transform.scale(healthbar, (int((tm1)/Mundo1.spell1cool*100) * 2, 20))
        Mundo1spell2 = pygame.transform.scale(healthbar, (int((tm2) / Mundo1.spell2cool * 100) * 2, 20))
        Mundo2spell1 = pygame.transform.scale(healthbar,(int((tm3) / Mundo2.spell1cool * 100) * 2, 20))
        Mundo2spell2 = pygame.transform.scale(healthbar,(int((tm4) / Mundo2.spell2cool * 100) * 2, 20))
        screen.blit(tex0, (10, 30))
        screen.blit(tex1, (10, 10))
        screen.blit(tex2, (350, 10))
        screen.blit(tex3, (10, 440))
        screen.blit(tex4, (350, 440))
        screen.blit(q_cooltime, (80, 30))
        screen.blit(Mundo1spell1,(80,10))
        screen.blit(Mundo1spell2, (420, 10))
        screen.blit(Mundo2spell1, (80, 440))
        screen.blit(Mundo2spell2, (420, 440))

    if (Mundo2.health <= 0):
        font2 = pygame.font.SysFont('Liberation Serif', 28)  # 폰트 설정
        window.blit(background, (0, 0))
        timeprint='total time: '+str(int((time.time()-total_time)))+' s'
        text2 = font2.render("you die", True, (255, 255, 255))
        text3=font2.render(timeprint,True,(255,255,255))
        text4 = font2.render("auto-retry in 3 seconds", True, (255, 255, 255))
        screen.blit(text2, (200, 320))
        screen.blit(text3,(200,360))
        screen.blit(text4, (200, 400))
        pygame.display.update()
        time.sleep(3)
        Mundo2.health=100
        Mundo1.x = 320.0
        Mundo1.y = 100.0
        Mundo2.x=320.0
        Mundo2.y=400.0
        total_time=time.time()
    if time.time() - pree_time >= 1:
        Mundo2.health += Mundo2.healthregen
        if Mundo2.health>=100.0:
            Mundo2.health=100.0
        pree_time = time.time()
    position = pygame.mouse.get_pos()
    mundoblit(Mundo1, position,check1)
    mundoblit(Mundo2, position,check2)
    if(Mundo1.x<=135 and Mundo2.x<=135):
        mundoblit(Mundo1, position, check)
        mundoblit(Mundo2, position, check)
    if (Mundo1.x >= 500 and Mundo2.x >= 500):
        mundoblit(Mundo1, position, check)
        mundoblit(Mundo2, position, check)
    if(check_time1 !=0):
        now_time1=time.time()
        if(now_time1-check_time1>=0.5):
            check1=0
    if (check_time2 != 0):
        now_time2 = time.time()
        if (now_time2 - check_time2 >= 0.5):
            check2 = 0
    arrowblit(Mundo1)
    arrowblit(Mundo2)
    Mundo1.injured(Mundo2)
    Mundo2.injured(Mundo1)
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                keys1[0] = True
            elif event.key == pygame.K_a:
                keys1[1] = True
            elif event.key == pygame.K_s:
                keys1[2] = True
            elif event.key == pygame.K_d:
                keys1[3] = True
            elif event.key == pygame.K_q and time.time() - pre_time >= Mundo1.cooltime_limit:
                pre_time = Mundo1.attack()
                check1=1
                check_time1=time.time()
                mundoblit(Mundo1,position,check1)
            elif event.key == pygame.K_r and time.time() - pre3_time >= Mundo1.spell1cool:
                pre3_time = Mundo1.spelluse('r')
            elif event.key == pygame.K_f and time.time() - pre4_time >= Mundo1.spell2cool:
                pre4_time = Mundo1.spelluse('f')
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                keys1[0] = False
            elif event.key == pygame.K_a:
                keys1[1] = False
            elif event.key == pygame.K_s:
                keys1[2] = False
            elif event.key == pygame.K_d:
                keys1[3] = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                keys2[0] = True
            elif event.key == pygame.K_LEFT:
                keys2[1] = True
            elif event.key == pygame.K_DOWN:
                keys2[2] = True
            elif event.key == pygame.K_RIGHT:
                keys2[3] = True
            elif event.key==pygame.K_COMMA and time.time()-pre5_time>=Mundo2.spell1cool:
                pre5_time=Mundo2.spelluse('r')
            elif event.key==pygame.K_PERIOD and time.time()-pre6_time>=Mundo2.spell2cool:
                pre6_time=Mundo2.spelluse('f')
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                keys2[0] = False
            elif event.key == pygame.K_LEFT:
                keys2[1] = False
            elif event.key == pygame.K_DOWN:
                keys2[2] = False
            elif event.key == pygame.K_RIGHT:
                keys2[3] = False
    Mundo1.move(keys1[0], keys1[1], keys1[2], keys1[3],1)
    Mundo2.move(keys2[0], keys2[1], keys2[2], keys2[3],2)


