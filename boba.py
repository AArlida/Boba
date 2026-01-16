import pygame 


pygame.init()

run = True 

#Set up + image loading 

WIDTH,HEIGHT = 400,600 
fps = 60
pygame.display.set_caption("Bonnies Boba!")
clock = pygame.time.Clock()
dragging = False
dragging2 = False
dragged = False
pour = False
intervals = 0.15 
timer = 0.0
start = None
start2 = None
stacknum= 0
button_next = pygame.Rect(300,500,50,50)
stations= (0,1,2,3)
i = 0
current_station = stations[i]
num = 1

screen = pygame.display.set_mode((WIDTH,HEIGHT))

background_img = pygame.image.load(f"background{num}.png")
cup_img = pygame.image.load("cup1.png")
boba_img = pygame.image.load("boba3.png")
ice_img = pygame.image.load("ice1.png")


#boba bin (where the boba is picked from)
Boba_bin = pygame.Rect(49,220,100,40)

#drop zone (area above the cup)
Drop_zone = pygame.Rect(160,0,80,330)

#area for ice
Ice_zone = pygame.Rect(150,200,90,100)

#ice putton
Ice_button = pygame.Rect(160,170,85,50)

#milk button
milk_button = pygame.Rect(33,100,77,90)

#matcha button
matcha_button = pygame.Rect(120,100,77,90)

#ollang button
ollang_button = pygame.Rect(206,100,77,90)

#other
other_button = pygame.Rect(293,100,77,90)

#//////////////////////
#This is where all 'stations' are put for easy switching
#between background a functionalities 
#//////////////////////
class Stations():

    def Boba(event):
        global dragging , pour , background_img , num , current_station, dragged
        background_img = pygame.image.load(f"background{num}.png") 
        mx,my = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if Boba_bin.collidepoint(mx,my):
                mx,my = pygame.mouse.get_pos()
                held_boba.add(Boba(mx,my,boba_img))
                dragging = True
                pour = False 
                dragged = True
            else:
                dragged = False
            if button_next.collidepoint(mx,my):
                    current_station+=1  
                    num+=1
                    background_img = pygame.image.load(f"background{num}.png")
        if event.type == pygame.MOUSEBUTTONUP:
            dragging = False
            mx,my = pygame.mouse.get_pos()
            if Drop_zone.collidepoint(mx,my) and dragged:
                pour = True
                held_boba.empty()
                global start
                start = pygame.time.get_ticks()


    def Start(event):
        global dragging , pour , background_img , num , current_station 
        background_img = pygame.image.load(f"background{num}.png") 
        mx,my = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if button_next.collidepoint(mx,my):
                    current_station+=1  
                    num+=1
                    background_img = pygame.image.load(f"background{num}.png")

    def Ice(event):
        mx,my = pygame.mouse.get_pos()
        global dragging , pour , background_img , num , current_station, dragged, dragging2, start2
        background_img = pygame.image.load(f"background{num}.png") 
        if event.type == pygame.MOUSEBUTTONDOWN and event.button ==1:
            if cup.rect.collidepoint(mx,my):
                dragging2 = True
            if button_next.collidepoint(mx,my):
                current_station+=1  
                num+=1
                background_img = pygame.image.load(f"background{num}.png")
            if Ice_button.collidepoint(mx,my):
                pour = True
                start2 = pygame.time.get_ticks()
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            pour =False
            mx,my = pygame.mouse.get_pos()
            if Ice_zone.colliderect(cup.rect):
                cup.x=300
                dragging2 = False
            

    def Pour(event):
        global dragging , pour , background_img , num , current_station, dragged
        background_img = pygame.image.load(f"background{num}.png") 
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx,my = pygame.mouse.get_pos()
            if button_next.collidepoint(mx,my):
                current_station+=1  
                num+=1
                background_img = pygame.image.load(f"background{num}.png")
            if milk_button.collidepoint(mx,my):
                current_station =4
            if matcha_button.collidepoint(mx,my):
                current_station =5
            if ollang_button.collidepoint(mx,my):
                current_station =6
            if other_button.collidepoint(mx,my):
                current_station =7


    def Milk(event):
        global dragging, pour, background_img, num, current_station, dragged
        background_img = pygame.image.load(f"background{num}.png")
        mx,my = pygame.mouse.get_pos()
        if button_next.collidepoint(mx,my):
                current_station+=1  
                num+=1
                background_img = pygame.image.load(f"background{current_station}.png")

    def Matcha(event):
        global dragging, pour, background_img, num, current_station, dragged
        background_img = pygame.image.load(f"background{num}.png")





class Cup(pygame.sprite.Sprite):
    def __init__(self,x,y,img): 
        super().__init__()
        self.x = float(x)
        self.y= float(y)
        self.image = img 
        self.rect = self.image.get_rect(center=(x,y))
        self.contents = pygame.Surface(self.image.get_size(),pygame.SRCALPHA)
        self.cupclear = pygame.image.load("clearcup2.png")
        self.clearrect = self.cupclear.get_rect(center=((x+1),(y-7)))
        self.mask = pygame.mask.from_surface(self.image)
        global pour_bottom
        self.fill_height = 510

class Boba(pygame.sprite.Sprite):
    def __init__(self,x,y,img):
        super().__init__()
        self.x = x
        self.y = y
        self.vy= 0.0
        self.image = img
        self.rect = self.image.get_rect(center= (x,y))



    def update(self,dt,bottom):
         g = 1200.0
         self.vy += g * dt
         self.y += self.vy * dt 
         self.rect.y = int(self.y)
         
         
         if self.rect.bottom >= pour_bottom:
            self.rect.bottom =  bottom
            self.vy = 0
        
         # ---------- BAKE ---------- (as in making new additions (sprites) part of the cup image)
    def bake(self):
        local_x = self.rect.x - cup.rect.left
        local_y = self.rect.y - cup.rect.top
        cup.contents.blit(self.image, (local_x, local_y))
        self.kill()


    
    

class Ice(pygame.sprite.Sprite):
    def __init__(self,x,y,img):
        super().__init__()
        self.x = x
        self.y = y
        self.vy= 0.0
        self.image = img
        self.rect = self.image.get_rect(center= (x,y))
        

    def update(self,dt,bot):
        g = 1200.0
        self.vy += g * dt
        self.y += self.vy * dt 
        self.rect.y = int(self.y)

         
        if self.rect.bottom >= bot:
            self.rect.bottom =  bot
            self.vy = 0
        

    def bake(self):
        local_x = self.rect.x - cup.rect.left
        local_y = self.rect.y - cup.rect.top
        cup.contents.blit(self.image, (local_x, local_y))
        self.kill()

def update(event):
    global dragging , pour, timer, intervals, start, current_station, num
    #if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
    mx,my = pygame.mouse.get_pos()   
    if current_station == 0 :
        Stations.Start(event)             
    elif current_station == 1:
        Stations.Boba(event)
    elif current_station == 2:
        Stations.Ice(event)
    elif current_station == 3:
        Stations.Pour(event)
    elif current_station == 4:
        Stations.Milk(event)
    elif current_station == 5:
        Stations.Matcha(event)



                            


cup = Cup(200, 450, cup_img)


held_boba = pygame.sprite.GroupSingle()
falling_boba = pygame.sprite.Group()
boba_bottom= pygame.Rect(160,400,90,100)
ice_falling = pygame.sprite.Group()
while run:
    bottom= cup.rect.bottom -9
    dt = clock.tick(fps)/1000

    screen.blit(background_img,(0,0))
    if current_station >0 and current_station<3:
        screen.blit(cup.image, cup.rect)
        screen.blit(cup.contents, cup.rect.topleft)
        held_boba.draw(screen)
        ice_falling.draw(screen)
        falling_boba.draw(screen) 
        screen.blit(cup.cupclear,cup.clearrect)


    timer+= dt

    if dragging:
        for boba in held_boba:
            mx,my = pygame.mouse.get_pos()
            boba.rect.center = (mx,my)
    
    
    pour_bottom = bottom
    if pour:
        mx,my = pygame.mouse.get_pos()
        if Drop_zone.collidepoint(mx, my) and current_station == 1:
            if timer >= intervals:
                falling_boba.add(Boba(mx, my, boba_img))
                timer = 0.0
        if Ice_button.collidepoint(mx,my) and current_station ==2:
            if timer >= intervals:
                ice_falling.add(Ice(190,200,ice_img))
                timer = 0.0
        
    icetime = pygame.time.get_ticks()      
    for i, ice in enumerate(ice_falling):
        ice.update(dt,pour_bottom)       
        if i == 2:
            pour_bottom -= 7
        if i == 4:
            pour_bottom-=20
        if i == 6:
            pour_bottom-=15 
        if start2 != None:
            if icetime -start2 >= 2000:
                pour =False
                if icetime - start2 >= 3000:
                    bottom = pour_bottom 
                    ice.bake()  
                    

    
    pour_time = pygame.time.get_ticks()
    for i, boba in enumerate(falling_boba):
        boba.update(dt,pour_bottom)
        if i == 15:
            pour_bottom-= 9
        if i == 30:
            pour_bottom-=7
        if i == 45:
            pour_bottom-=7
        if i == 55:
            pour_bottom-=9
        if start != None:
            if pour_time -start >= 6000:
                pour = False
                if pour_time - start >= 7000:
                    bottom = pour_bottom
                    for boba in falling_boba:
                        boba.bake()  

    if dragging2:
        mx,my = pygame.mouse.get_pos()
        cup.rect.center = (mx,my) 
        cup.clearrect.center = (mx+1,my-7)      

    #held_boba.draw(screen)
    #falling_boba.draw(screen) 
    pygame.draw.rect(screen,(255,0,0),button_next)
    pygame.draw.rect(screen,(255,0,0),milk_button)
    pygame.draw.rect(screen, (255,0,0), matcha_button)
    pygame.draw.rect(screen,(255,0,0),ollang_button)
    pygame.draw.rect(screen,(250,0,0),other_button)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run=False   
        update(event)
    pygame.display.update()


pygame.quit()           
