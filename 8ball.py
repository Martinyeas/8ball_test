import pygame
import time
import random
import math
import sys

pygame.init()
class ball():
    def __init__(self,pos,szin,lendulet,mass):
        self.pos = pos
        self.szin = szin
        self.lendulet = lendulet
        self.mass = mass

debug_erzekenyseg = 0.00001
coll_diff = 60
coll_diff = coll_diff / 100
golox,goloy = 20,20
golor = golox / 1.5
surlodas = .999
defa_mass = 1
print("surlodas: ",surlodas)
sizemultiplier = 3
zold = (42, 148, 10)
w,h = 112*sizemultiplier,224*sizemultiplier
wind = pygame.display.set_mode((w,h))
pygame.display.set_caption("NIGGERS")
holew,holeh = 24,24
holecolor = (0,0,0)
holenum = [[0,0,holecolor],[w-holew,0,holecolor],[0,h-holeh,holecolor],[w-holew,h-holeh,holecolor],[0,h/2-holeh,holecolor],[w-holew,h/2-holeh,holecolor]]
golok_szam = 0
lendulet_sum = 0
lendulet_sum_chng = 0
vonalw = 5
hole_detection_dist = 23
balls_NUM = golok_szam

balls = []
for i in range(golok_szam):
    xpos,ypos = random.randint(0+((golox/2)+1),w-((golox/2)+1)),random.randint(0+((goloy/2)+1),h-((goloy/2)+1))
    for poz in balls:
        while True:
            if (xpos,ypos) != poz.pos:
                break
            xpos,ypos = random.randint(0+((golox/2)+1),w-((golox/2)+1)),random.randint(0+((goloy/2)+1),h-((goloy/2)+1))
    balls.append(ball([xpos,ypos],(random.randint(0,255),random.randint(0,255),random.randint(0,255)), [random.randint(-200,200)/100,random.randint(-200,200)/100],defa_mass))

holding_mouse = False
clickpos = None
running = True
font = pygame.font.Font("freesansbold.ttf", 72)
text = font.render('NUM', True,(255,255,255))
textRect = text.get_rect()
textRect.center = (w/2,golox)
while running:
    wind.fill(zold)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            holding_mouse = True
            clickpos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONUP:
            holding_mouse = False
            uppos = pygame.mouse.get_pos()
            magn = pygame.Vector2(clickpos[0]-uppos[0],clickpos[1]-uppos[1])
            balls.append(ball([clickpos[0],clickpos[1]],(random.randint(0,255),random.randint(0,255),random.randint(0,255)), [magn[0]/25,magn[1]/25],defa_mass))
            clickpos = None
    if holding_mouse:
        pygame.draw.line(wind,(255,255,255),(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]),(clickpos[0],clickpos[1]),vonalw)
    #lendulet_sum_chng = 0
    balls_NUM = 0
    for i in balls:
        balls_NUM += 1
        #lendulet_sum_chng += abs(i.lendulet[0]) + abs(i.lendulet[1])
        i.pos[0] += i.lendulet[0] / 10
        i.pos[1] += i.lendulet[1] / 10
        i.lendulet[0] *= surlodas
        i.lendulet[1] *= surlodas
        rect = pygame.draw.circle(wind,(i.szin),(i.pos),golor)
        for hole in holenum:
            if pygame.Vector2(i.pos[0] - hole[0],i.pos[1] - hole[1]).magnitude() <= hole_detection_dist:
                balls.remove(i)
        if rect.right >= w or rect.left <= 0:
            i.lendulet[0] = -i.lendulet[0]
        if rect.bottom >= h or rect.top <= 0:
            i.lendulet[1] = -i.lendulet[1]

        for b in balls:
            if b != i:
                brect = pygame.draw.circle(wind,(b.szin),(b.pos),golor)
                if rect.colliderect(brect):
                    # b.lendulet = [i.lendulet[0],i.lendulet[1]]
                    # i.lendulet = [-b.lendulet[0]*coll_diff,-b.lendulet[1]*coll_diff]
                    collision_normal = None
                    if not i.pos[0] == 0 or not b.pos[0] == 0 or not i.pos[1] == 0 or not b.pos[1] == 0:
                        collision_normal = pygame.Vector2(i.pos[0] - b.pos[0], i.pos[1] - b.pos[1]).normalize()
                    else:
                        collision_normal = 1
                    relative_velocity = pygame.Vector2(i.lendulet[0] - b.lendulet[0], i.lendulet[1] - b.lendulet[1])
                    impulse = 2 * pygame.Vector2.dot(relative_velocity, collision_normal) / (i.mass + b.mass) * collision_normal
                    i.lendulet -= impulse * b.mass
                    b.lendulet += impulse * i.mass
                    overlap = golor - math.sqrt((i.pos[0] - b.pos[0]) ** 2 + (i.pos[1] - b.pos[1]) ** 2)
                    if overlap > 0:
                        separation_distance = 0.1 * overlap
                        separation_vector = separation_distance * collision_normal
                        i.pos[0] += separation_vector[0]
                        i.pos[1] += separation_vector[1]
                        b.pos[0] -= separation_vector[0]
                        b.pos[1] -= separation_vector[1]
    #if lendulet_sum_chng != lendulet_sum:
        #lendulet_sum = lendulet_sum_chng
    text = font.render(str(balls_NUM), True,(255,255,255))
    wind.blit(text, textRect)
    for hole in holenum:
        pygame.draw.rect(wind,(hole[2]),(hole[0],hole[1],holew,holeh),0,10)
    pygame.display.flip()
