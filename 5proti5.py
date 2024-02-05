
# THE ENTIRE CODE ISN'T MADE BY ME
# a part of the code is made by my classmate


import pygame
import sys

# Initialize Pygame
pygame.init()
pygame.mixer.init()

datapath="5proti5/"
gamefile="5proti5 na stužkovú.txt"

with open(gamefile,encoding="utf-8") as s:
    l=s.readlines()
    b=[]
    for i in l:
        a=[]
        for o in i.split(";"):
            a+=[o.strip().split(":")]
        b+=[a]
    gamedata=b

# Get the screen's width and height
screen_info = pygame.display.Info()
screen_width, screen_height = screen_info.current_w, screen_info.current_h
adjust_x = 1920 / screen_width
adjust_y = 1080 / screen_height

# Create a Pygame display with the screen dimensions
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)

# Load the background image and resize it
background = pygame.image.load(datapath+"background.png")
background = pygame.transform.scale(background, (screen_width, screen_height))

# Load the background image for the score
bg_score = pygame.image.load(datapath+"bg_score.png")
bg_score_width = 400 / adjust_x
bg_score_height = 100 / adjust_y
bg_score = pygame.transform.scale(bg_score, (int(bg_score_width), int(bg_score_height)))

# Define the font and create a surface for the "score: 100" text
font = pygame.font.Font(None, int(56 / adjust_x))  # You can change the font and size

# Load the background image for the rows and adjust the dimensions
bg_row = pygame.image.load(datapath+"bg_row.png")
bg_row_width = 1344 / adjust_x
bg_row_height = 90 / adjust_y
bg_row = pygame.transform.scale(bg_row, (int(bg_row_width), int(bg_row_height)))
bg_row_backup=bg_row


# Create a list of answers for the rows

# Calculate the positions for the rows and texts

def rowposgen():
    ret=[]
    for i in range(num_rows):
        row_x = -bg_row_width / 2 + 30 / adjust_x
        row_y = (screen_height - (bg_row_height + 10) * num_rows) // 2 + i * (bg_row_height + 10)
        ret.append((row_x, row_y))
    return(ret)


# Load the "x.png" image
x_image = pygame.image.load(datapath+"x.png")
x_image = pygame.transform.scale(x_image, (int(x_image.get_width() / adjust_x), int(x_image.get_height() / adjust_y)))
x_image_width, x_image_height = x_image.get_size()

# Load the "row_cover.png" image and resize it to match the row dimensions
row_cover = pygame.image.load(datapath+"row_cover.png")
row_cover = pygame.transform.scale(row_cover, (int(bg_row_width), int(bg_row_height)))


# Initialize variables to control the visibility of the "x.png" image
show_x_image = False
x_image_start_time = 0
x_image_duration = 3  # Duration in seconds

# Calculate the position for the "x.png" image under the last row in the middle
x_image_x = (screen_width - x_image_width) // 2
x_image_y = 1080-x_image_height*1.5  # Position under the last row

# Load "bg_1_team.png" and "bg_2_team.png" images and adjust the dimensions
bg_1_team = pygame.image.load(datapath+"bg_1_team.png")
bg_2_team = pygame.image.load(datapath+"bg_2_team.png")

team_image_width = 300  # Adjust the width as needed
team_image_height = 100  # Adjust the height as needed
bg_1_team = pygame.transform.scale(bg_1_team, (int(team_image_width), int(team_image_height)))
bg_2_team = pygame.transform.scale(bg_2_team, (int(team_image_width), int(team_image_height)))

# Create text surfaces for "score" on both sides
score_text_left = font.render("0", True, (255, 255, 255))
score_text_right = font.render("0", True, (255, 255, 255))

# Calculate positions for "bg_1_team.png" and "bg_2_team.png" images and text
team_image_x_left = x_image_x - team_image_width - 70 / adjust_x
team_image_x_right = x_image_x + x_image_width + 70 / adjust_x
team_image_y = x_image_y + (x_image_height - team_image_height) / 1.3 / adjust_y

score_text_x_left = team_image_x_left + (team_image_width - score_text_left.get_width()) // 2
score_text_x_right = team_image_x_right + (team_image_width - score_text_right.get_width()) // 2
score_text_y_left = team_image_y + team_image_height / 2.8
score_text_y_right = team_image_y + team_image_height / 2.8

# Resize the "x.png" image to create smaller versions for Team 1 and Team 2
small_x_width = int(50 / adjust_x)  # Adjust the width for smaller "x.png"
small_x_height = int(50 / adjust_y)  # Adjust the height for smaller "x.png"
small_x_image = pygame.transform.scale(x_image, (small_x_width, small_x_height))

# Calculate positions for the smaller "x.png" images on top of Team 1 and Team 2
small_x_team1_x = team_image_x_left + (team_image_width - small_x_width) // 2
small_x_team2_x = team_image_x_right + (team_image_width - small_x_width) // 2
small_x_y = team_image_y - small_x_height - 20 / adjust_y  # Position above Team 1 and Team 2

# Calculate positions for the additional smaller "x.png" images on top of Team 1 and Team 2
small_x_team1_x1 = small_x_team1_x - small_x_width - 10 / adjust_x
small_x_team1_x2 = small_x_team1_x + small_x_width + 10 / adjust_x
small_x_team2_x1 = small_x_team2_x - small_x_width - 10 / adjust_x
small_x_team2_x2 = small_x_team2_x + small_x_width + 10 / adjust_x

team1_x = 0
team2_x = 0
#nok_sound = pygame.mixer.Sound(datapath+"nok_sound.mp3")

def ďalšiekolo(rl):
    Animation(koloAnim,3,0,kolo=kolo+1,rl=rl)

def _kolosetter(num):
    global kolo,num_rows,row_positions,team1_x,team2_x,row_covered,current_rows
    kolo=num
    current_rows=gamedata[num]
    num_rows=len(current_rows)
    row_positions=rowposgen()
    team1_x=0
    team2_x=0
    row_covered=[True]*num_rows

class Animation:
  '''
  func parameter takes a function

  def func(d:Animation):
    pass
    
  seconds=3
  anim=Animation(func, seconds)
  while True:
    Animation.update(deltatime) # deltatime = 1 if you want to count it in frames
  '''
  _register=[]

  def update(deltatime):
    o=-1
    for i in Animation._register:
      i:Animation
      o+=1
      if(i.delay>0):
        i.delay-=deltatime
      else:
        i.deltatime=deltatime
        i.func(i)
        i.time+=deltatime
        if i.time>=i.length:
            del Animation._register[o]
            del i

  def __init__(c,func,duration,delay=0,**params):
    Animation._register.append(c)
    c.mulstat=1
    c.length=duration
    c.func=func
    c.params=params
    c.time=0
    c.delay=delay
    c.deltatime=0

def koloAnim(d:Animation):
    global koloanimactive
    if(d.time==0):
        koloanimactive=True
        d.params.update({"stat":0},idealpos=row_positions[0][0],xrl=[row_positions[0][0]+1920/adjust_x*d.params["rl"],row_positions[0][0]-1920/adjust_x*d.params["rl"]])
    if(d.time<d.length/2):
        for i,o in enumerate(row_positions):
            row_positions[i]=(row_positions[i][0]-d.params["xrl"][0])/pow(1920,d.deltatime)+d.params["xrl"][0],row_positions[i][1]
    else:
        if(d.params["stat"]==0):
            d.params["stat"]=1
            _kolosetter(d.params["kolo"])
            for i,o in enumerate(row_positions):
                row_positions[i]=d.params["xrl"][1],row_positions[i][1]
        for i,o in enumerate(row_positions):
            row_positions[i]=(row_positions[i][0]-d.params["idealpos"])/pow(1920,d.deltatime)+d.params["idealpos"],row_positions[i][1]
    if(d.time+d.deltatime>d.length):
        koloanimactive=False
        for i,o in enumerate(row_positions):
            row_positions[i]=d.params["idealpos"],row_positions[i][1]

def answerAnim(d:Animation):
    global current_score
    a,b=0.5,0.9
    časť=0.9
    if(d.time==0):
        print("playsound odokrytie")
        d.params.update({"bodyplayed":False})
    if(d.time>d.length*b and not(d.params["bodyplayed"])):
        d.params["bodyplayed"]=True
        current_score+=int(d.params["body"])
        print("playsound body")
    if(d.time<d.length*a):
        časť*=d.time/(d.length*a)
    elif(d.time>d.length*b):
        časť=časť+(d.time-d.length*b)/(d.length-d.length*b)*0.1
    tex=row_cover
    x,y=d.params["xy"]
    xx=x+bg_row_width*časť
    screen.blit(tex,(xx,y),(bg_row_width*časť,0,bg_row_width,bg_row_height))

teamscores=0,0
koloanimactive=False
current_score=0
current_rows=[]
row_positions=[]
num_rows=0
_kolosetter(0)
print(current_rows,num_rows)

# Your game loop goes here
deltatime=0
predt=pygame.time.get_ticks()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_y:
                # Pressed "y" key, show the "x.png" image for the specified duration
                show_x_image = True
                team1_x += 1
                #nok_sound.play()
                x_image_start_time = pygame.time.get_ticks() / 1000  # Convert milliseconds to seconds
            if event.key == pygame.K_x:
                # Pressed "x" key, show the "x.png" image for the specified duration
                show_x_image = True
                team2_x += 1
                #nok_sound.play()
                x_image_start_time = pygame.time.get_ticks() / 1000  # Convert milliseconds to seconds

            if event.key == pygame.K_y and pygame.key.get_mods() & pygame.KMOD_LSHIFT:
                show_x_image = True
                team1_x = 3
                #nok_sound.play()
                x_image_start_time = pygame.time.get_ticks() / 1000  # Convert milliseconds to seconds

            if event.key == pygame.K_x and pygame.key.get_mods() & pygame.KMOD_LSHIFT:
                show_x_image = True
                team2_x = 3
                #nok_sound.play()
                x_image_start_time = pygame.time.get_ticks() / 1000  # Convert milliseconds to seconds

            if event.key==pygame.K_ESCAPE:
                running=False
            
            if((event.key==pygame.K_m or event.key==pygame.K_n) and not(koloanimactive)):
                o=True
                for i in row_covered:
                    if(i):
                        o=False
                        break
                if(o):
                    if(event.key==pygame.K_m):
                        teamscores=teamscores[0],teamscores[1]+current_score
                        ďalšiekolo(1)
                    else:
                        teamscores=teamscores[0]+current_score,teamscores[1]
                        ďalšiekolo(-1)
                    current_score=0

            # Check if number keys are pressed to uncover rows
            if pygame.K_1 <= event.key <= pygame.K_9:
                row_number = event.key - pygame.K_1  # Calculate the row number (0 to 4)
                if 0 <= row_number < num_rows:
                    row_covered[row_number] = False  # Uncover the corresponding row
                    Animation(answerAnim,3,0,xy=(row_positions[row_number][0] + screen_width / 2 - 20 / adjust_x, row_positions[row_number][1]),body=current_rows[row_number][1])

    # Clear the screen
    screen.fill((0, 0, 0))

    # Blit the background image onto the screen
    screen.blit(background, (0, 0))

    score_text = font.render(str(current_score), True, (255, 255, 255))
    score_text_width, score_text_height = score_text.get_size()
    bg_score_x = (screen_width - bg_score_width) // 2
    bg_score_y = 100 / adjust_y
    score_text_x = screen_width / 2 - score_text_width / 2
    score_text_y = 135 / adjust_y
    screen.blit(bg_score, (bg_score_x, bg_score_y))
    screen.blit(score_text, (score_text_x, score_text_y))

    # Blit the rows and texts onto the screen
    for i, row_position in enumerate(row_positions):
        screen.blit(bg_row, (row_position[0] + screen_width / 2 - 20 / adjust_x, row_position[1]))
        text = font.render(str(i+1)+")", True, (255, 255, 255))
        text_x = row_position[0] + screen_width / 2  # Adjust as needed for horizontal padding
        text_y = row_position[1] + (bg_row_height - text.get_height()) // 2
        screen.blit(text, (text_x, text_y))

        # Check if the row should be covered
        if row_covered[i]:
            screen.blit(row_cover, (row_position[0] + screen_width / 2 - 20 / adjust_x, row_position[1]))

        # Add answer text if the row is uncovered
        else:
            answer_text = font.render(current_rows[i][0], True, (255, 255, 255))
            answer_points = font.render(current_rows[i][1], True, (255, 255, 255))
            answer_text_x = text_x + 100 / adjust_x  # Adjust as needed for horizontal padding
            answer_points_x = text_x + 1245 / adjust_x  # Adjust as needed for horizontal padding
            answer_text_y = text_y  # Adjust as needed for vertical alignment
            screen.blit(answer_text, (answer_text_x, answer_text_y))
            screen.blit(answer_points, (answer_points_x, answer_text_y))

    # Blit "bg_1_team.png" and "bg_2_team.png" images and text
    screen.blit(bg_1_team, (team_image_x_left, team_image_y))
    screen.blit(bg_2_team, (team_image_x_right, team_image_y))
    score_text_left = font.render(str(teamscores[0]), True, (255, 255, 255))
    score_text_right = font.render(str(teamscores[1]), True, (255, 255, 255))
    screen.blit(score_text_left, (score_text_x_left, score_text_y_left))
    screen.blit(score_text_right, (score_text_x_right, score_text_y_right))

    # Blit the smaller "x.png" images on top of Team 1 and Team 2
    if team1_x == 1:
        screen.blit(small_x_image, (small_x_team1_x1, small_x_y))
    if team1_x == 2:
        screen.blit(small_x_image, (small_x_team1_x, small_x_y))
        screen.blit(small_x_image, (small_x_team1_x1, small_x_y))
    if team1_x == 3:
        screen.blit(small_x_image, (small_x_team1_x, small_x_y))
        screen.blit(small_x_image, (small_x_team1_x1, small_x_y))
        screen.blit(small_x_image, (small_x_team1_x2, small_x_y))

    if team2_x == 1:
        screen.blit(small_x_image, (small_x_team2_x1, small_x_y))
    if team2_x == 2:
        screen.blit(small_x_image, (small_x_team2_x, small_x_y))
        screen.blit(small_x_image, (small_x_team2_x1, small_x_y))
    if team2_x == 3:
        screen.blit(small_x_image, (small_x_team2_x, small_x_y))
        screen.blit(small_x_image, (small_x_team2_x1, small_x_y))
        screen.blit(small_x_image, (small_x_team2_x2, small_x_y))

    # Blit the "x.png" image if it should be visible
    if show_x_image:
        current_time = pygame.time.get_ticks() / 1000  # Convert milliseconds to seconds
        if current_time - x_image_start_time < x_image_duration:
            # Display the "x.png" image for the specified duration
            screen.blit(x_image, (x_image_x, x_image_y))

    # Update the display
    Animation.update(deltatime)
    pygame.display.flip()
    deltatime=pygame.time.get_ticks()/1000-predt
    predt=pygame.time.get_ticks()/1000

# Quit Pygame
pygame.quit()
sys.exit()
