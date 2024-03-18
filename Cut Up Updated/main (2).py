'''
-------------------------------------------------------------------------------
Name:  main.py
Purpose:


Author:  Griffin Lamanna & Diyorbek Primov


Created:  11/14/2023
------------------------------------------------------------------------------
'''
# Imports the required module
import pygame, math
from pygame import mixer
import random
import time
# Define some colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
TGREEN = (133, 187, 101)
RED = (255, 0, 0)
pygame.init()
DARK_GREY = (128, 128, 128)
DARKER_GREY = (100, 100, 100)
GREY = (169, 169, 169)
button_colour = (169, 169, 169)

# Set the width and height of the screen [width, height]
size = (900, 700)
W = 900
H = 700
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Cut Up")

mixer.init()
#hellcat_idle = pygame.mixer.Sound('/Users/diyorbekprimov/PycharmProjects/Cut Up Updated/Hellcat Rev  1')

hellcat_rev = pygame.mixer.Sound('Hellcat Rev  1.mp3')
songs = {
    "Lil Uzi Vert - 20 Min.mp3" : 0,
    "Rich Amiri - One Call.mp3" : 1,
    "Mazza L20 x Aystar - Murdaside.mp3" : 2,
    "INSTASAMKA - КАК MOMMY.mp3" : 3

}

increment_to_enemy_spawn = 1

paused_music = False
change_music = False
song_selection = 0
# Set preferred volume
volume = 0.2
mixer.music.set_volume(volume)
pygame.mixer.music.load(list(songs.keys())[song_selection])
mixer.music.play()
def radio():
    global songs
    global change_music
    global song_selection
    if song_selection == 4:
        song_selection = 0
    elif song_selection == -1:
        song_selection = 3
    if change_music == True:
        pygame.mixer.music.load(list(songs.keys())[song_selection])
        pygame.mixer.music.play()
        change_music = False


# Play the music


play_game_cond = False
play_menu = True

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()
# Hide the mouse cursor

#screen = pygame.display.set_mode((1920,1080), pygame.FULLSCREEN)

settings_menu_cond = False

settings_screen = pygame.image.load('Settings Screen.png')
held_button = pygame.image.load('play button held.png')
held_button2 = pygame.image.load('Settings Hovered.png')
held_button3 = pygame.image.load('held quit button.png')
held_button4 = pygame.image.load('backbutton_held.png')
image = pygame.image.load('cut up main screen.png')
img = pygame.image.load('CUT UP HELLCAT.png')
img = pygame.transform.scale(img, [100, 140])
image = pygame.transform.scale(image, [900,700])

text_font = pygame.font.SysFont("Arial", 30)

# Specifies the file location for the enemy cars graphics
enemycar_filenames = ['Car 1.png','Car 2.png', 'Car 3.png', 'Car 4.png', 'Car 5.png', 'Car 6.png']

# Creates a list that stores the enemy cars graphics
enemycars = []
for enemycar in enemycar_filenames:
    enemy_image = pygame.image.load('Sprites/Enemy Car Sprites/' + enemycar)
    enemycars.append(enemy_image)

vehicle_group = pygame.sprite.Group()

# Loads the
level1 = pygame.image.load('Sprites/Level Sprites/level 1.png')

# Declares the starting position for the users car
hellcat_x = 300
hellcat_y = 200

width_ofhellcat = 60
height_ofhellcat = 140
enemycar_width = 62
enemycar_height = 98


score = 0

enemy_speed = 2
class Vehicle(pygame.sprite.Sprite):

    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        new_width = image.get_rect().width * 1
        new_height = image.get_rect().height * 1
        # scale the image down so it's not wider than the lane
        self.image = pygame.transform.scale(image, (90, 103))

        self.rect = self.image.get_rect()
        self.rect.center = [x, y]


#Define player class with all attributes and draw method
class Player():
    def __init__(self, speed, health):
        self.speed = speed
        self.health = health
        self.xpos = 300
        self.ypos = 200
        self.image = pygame.image.load('CUT UP HELLCAT.png')
        self.image = pygame.transform.scale(self.image, [100, 140])
        self.rect = self.image.get_rect()
    def draw(self):
        screen.blit(self.image, [self.xpos, self.ypos])

#crash_rect = crash.get_rect()

#Creates new_player object from the player class above
new_player = Player(5, 3)

#Creates default system font variable
font = pygame.font.SysFont('Arial', 32)

# Declares the x value for the enemy spawn positions
lanes = [235, 375, 515, 650]

def main_menu():
    play_menu = True
    if play_menu == True:
        screen.blit(image, [0, 0])
        #Check coordinates of mouse if its over the play button, blit grey button version if it is
        if mouse_x >= 106 and mouse_x <= 321 and mouse_y >= 298 and mouse_y <= 375:
            hover_check = True
            if hover_check is True:
                screen.blit(held_button, [106, 298])
        #Check coordinates of mouse if its over the settings button
        if 34 <= mouse_x <= 365 and mouse_y >= 408 and mouse_y <= 485:
            hover_check2 = True
            if hover_check2 is True:
                screen.blit(held_button2, [34, 408])
        #Check coordinates of mouse if its over the quit button
        if 120 <= mouse_x <= 291 and mouse_y >= 531 and mouse_y <= 608:
            hover_check3 = True
            if hover_check3 is True:
                screen.blit(held_button3, [120, 531])
#class Enemy():
startTime = time.time()


# Create function to blit and create all objects needed to play the game
def play_game():
    global level1_y1
    global level1_y2
    global increment_currentspeed
    global current_speed
    current_speed += increment_currentspeed
    increment_currentspeed = increment_currentspeed * .85
    global score
    alive = True
    screen.blit(level1, [0,level1_y1])
    screen.blit(level1, [0, level1_y2])
    level1_y1 += current_speed
    level1_y2 += current_speed

    if level1_y1 >= 700:
        level1_y1 = -700
    if level1_y2 >= 700:
        level1_y2 = -700
    score_draw = font.render("Score: " + str(score), True, BLACK)
    health = font.render("Health: " + str(new_player.health), True, BLACK)
    screen.blit(health, (0, 550))
    screen.blit(score_draw, (0, 600))
    # hellcat_idle.play(0)
   # screen.blit(img, [hellcat_x, hellcat_y])

    new_player.draw()

#Creates function to display settings image when called
def settings_menu():
    global volume
    settings_menu_cond = True
    hover_check = False
    screen.blit(settings_screen, [0, 0])
    if mouse_x >= 359 and mouse_x <= 540 and mouse_y > 424 and mouse_y < 500:
        screen.blit(held_button4, [359, 424])
    mixer.music.set_volume(volume)


# -------- Main Program Loop -----------
while not done:
    #Get mouse x, y in 2 variables
    pos = pygame.mouse.get_pos()
    mouse_x = pos[0]
    mouse_y = pos[1]

    pressed = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        pressed = pygame.key.get_pressed()
        if event.type == pygame.MOUSEBUTTONDOWN:
            #Check if user clicks the settings
            if 34 <= mouse_x <= 365 and mouse_y >= 408 and mouse_y <= 485:
                hover_check2 = False
                play_menu = False
                settings_menu_cond = True
                settings_menu()
            #Check if user clicks play
            if mouse_x >= 106 and mouse_x <= 321 and mouse_y >= 298 and mouse_y <= 375:
                hover_check = False
                button_colour = DARKER_GREY
                play_menu = False
                play_game_cond = True
                totaltime = 0
                current_speed = 0
                level1_y1 = 0
                level1_y2 = -700
                increment_currentspeed = .5
                #pygame.mixer.Channel(1).play(hellcat_idle, -1)
                play_game()
            #Check if user wants to change the song
            if mouse_x >= 606 and mouse_x <= 642 and mouse_y >= 596 and mouse_y <= 646:
                song_selection -= 1
                change_music = True
                radio()
                print(song_selection)
            elif mouse_x >= 849 and mouse_x <= 883 and mouse_y >= 598 and mouse_y <= 647:
                song_selection += 1
                change_music = True
                radio()
            #Check if music is paused, if not let them pause on button click
            if paused_music == False:
                if mouse_x >= 765 and mouse_x <= 802 and mouse_y >= 596 and mouse_y <= 646:
                    pygame.mixer.music.pause()
                    paused_music = True
            #Elif check if music is paused, if it is let them unpause on button click
            elif paused_music == True:
                if mouse_x >= 687 and mouse_x <= 713 and mouse_y >= 598 and mouse_y <= 644:
                    pygame.mixer.music.unpause()
                    paused_music = False
            #Check if user clicks on back while in settings screen, go back to menu if they do
            if mouse_x >= 359 and mouse_x <= 540 and mouse_y >= 423 and mouse_y <= 500:
                if settings_menu_cond is True:
                    play_game_cond = False
                    play_menu = True
                    settings_menu_cond = False
            if settings_menu_cond is True:
                if mouse_x >= 309 and mouse_x <= 342 and mouse_y > 252 and mouse_y < 268:
                    if volume <= 0:
                        volume = 0
                    volume -= 0.1
                    print(volume)
                if mouse_x >= 565 and mouse_x <= 605 and mouse_y > 238 and mouse_y < 277:
                    if volume >= 1:
                        volume = 1
                    volume += 0.1
                    print(volume)
            #Quit game if user clicks on exit button
            if 120 <= mouse_x <= 291 and mouse_y >= 531 and mouse_y <= 608:
                exit()
    #Use 4 if statements to create 8 way movement with the new_player object based on key press
    if pressed[pygame.K_w]:
        new_player.ypos -= new_player.speed
        #pygame.mixer.Channel(1).play(hellcat_rev)
        #pygame.mixer.music.queue(hellcat_idle,'.mp3', -1)
    if pressed[pygame.K_s]:
        new_player.ypos += new_player.speed
    if pressed[pygame.K_a]:
        new_player.xpos -= new_player.speed
    if pressed[pygame.K_d]:
        new_player.xpos += new_player.speed


    #Check if user presses escape while in game, open settings if they do
    if pressed[pygame.K_ESCAPE]:
        if play_game_cond == True:
            settings_menu_cond = True
            play_game_cond = False

    if new_player.xpos <= 145:
        new_player.xpos = 145
    elif new_player.xpos >= 640:
        new_player.xpos = 640
    elif new_player.ypos <= -20:
        new_player.ypos = -20
    elif new_player.ypos >= 660:
        new_player.ypos = 660


    # Creates graphics and cursor using functions

    # Creates the illuminati title with shadow
    if play_menu is True:
        main_menu()
    hover_check = True
    if play_game_cond is True:
        play_game()

    if settings_menu_cond is True:
        settings_menu()
        
    

    if play_game_cond is True:
        if len(vehicle_group) < 4:
            add_vehicle = True
            for vehicle in vehicle_group:
                if vehicle.rect.top  <  vehicle.rect.height * 1.5:
                    add_vehicle = False
            if add_vehicle:
                lane = random.choice(lanes)
                enemy_image = random.choice(enemycars)
                vehicle_to_add = Vehicle(enemy_image, lane, 0)
                vehicle_group.add(vehicle_to_add)
        for vehicle in vehicle_group:
            #if new_player.ypos < vehicle.rect.y + 98:
                #if new_player.xpos > vehicle.rect.x and new_player.xpos < vehicle.rect.x + 62 or new_player.rect.x + 62 > vehicle.rect.x and new_player.xpos + 62:
                #    new_player.health -= 1


            vehicle.rect.y += enemy_speed
            if vehicle.rect.top >= H:
                vehicle.kill()
                score += 1

                if score > 0 and score % 8 == 0:
                    enemy_speed += increment_to_enemy_spawn
                    increment_to_enemy_spawn = increment_to_enemy_spawn * .93
                    new_player.speed += .20
       #collide = pygame.sprite.spritecollide(new_player, vehicle_group, False)
        ###if collide:
            #new_player.health -= 1
            if pygame.Rect.colliderect(new_player, vehicle_group):
                print("COLLIDE)")


        vehicle_group.draw(screen)
    else:
        score = 0
        vehicle_group.empty()
        enemy_speed = 2

    track0_name = font.render("Lil Uzi Vert - 20 min", True, BLACK)
    track1_name = font.render("Rich Amiri - One Call", True, BLACK)
    track2_name = font.render("Mazza L20 x Aystar - Murdaside", True, BLACK)
    track3_name = font.render("INSTASAMKA - КАК MOMMY", True, BLACK)

    if song_selection == 0:
        screen.blit(track0_name, (550, 0))
    if song_selection == 1:
        screen.blit(track1_name, (550, 0))
    if song_selection == 2:
        screen.blit(track2_name, (550, 0))
    if song_selection == 3:
        screen.blit(track3_name, (550, 0))

   # if collision_has_occured():
        #print("COLLISION")

    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
    # --- Limit to 60 frames per second
    clock.tick(60)

# Close the window and quit.
pygame.quit()
