import turtle
import colorsys
import random
import math

screen = turtle.Screen()
screen.setup(1000,1000)
screen.title("Synchronized Fireflies - PythonTurtle.Academy")
turtle.hideturtle()
turtle.speed(0)
turtle.tracer(0,0)

# Constants
H_YELLOWGREEN = 0.22 # constant: hue value of yellow green color.
V_DARK = 0.1 # constant: brightness value of initial dark state
V_BRIGHT = 1 # constant: brightness value of the brightest state
FPS = 30 # constant: refresh about 30 times per second
TIMER_VALUE = 1000//FPS # the timer value in milliseconds for timer events
CYCLE = 5 # costant: 5 second cycle for firefly to light up
LIGHTUP_TIME = 1 # constant: 1 second light up and dim
SPEED = 100 # 100 units per second
CLOSE_ENOUGH = 16 # if distance squared to target is less than 16, then it is close enough.
                    # make sure that this number is greater than SPEED/FPS squared
N = 300 # Number of fireflies

PHASE_DELTA = 0.01 # increment of phase when saw a neighbor fires up

# Variables
fireflies = [] # list of firefly turtles
v = [] # list of brightness values
phase = [] # list of phases
current_xpos = [] # list of current x coordinate
current_ypos = [] # list of current y coordinate
target_xpos = [] # list of target x coordinate
target_ypos = [] # list of raget y coordinate

def initialze_fireflies():
    for i in range(N):
        fireflies.append(turtle.Turtle()) # Add a turtle to the firefly turtle list
        v.append(V_DARK) # set them DARK first. The update function will update it to the correct value
        phase.append(random.uniform(0,CYCLE)) # phase is random from 0 to CYCLE
        current_xpos.append(random.uniform(-500,500)) # Let them go anywhere on screen
        current_ypos.append(random.uniform(-500,500))
        target_xpos.append(random.uniform(-500,500))
        target_ypos.append(random.uniform(-500,500))

    for firefly in fireflies: # initialize these turtles
        firefly.hideturtle()
        firefly.up()

# this function computes brightness based on phase
def compute_brightness(phase):
    if phase < CYCLE-LIGHTUP_TIME:
        temp = V_DARK # dormant period
    elif phase < CYCLE-LIGHTUP_TIME/2: # gradually (linearly) lighting up period
        temp = V_DARK + (V_BRIGHT-V_DARK)*(phase-(CYCLE-LIGHTUP_TIME))/(LIGHTUP_TIME/2)
    else: # gradually (linearly) dimming period
        temp = V_BRIGHT - (V_BRIGHT-V_DARK)*(phase-(CYCLE-LIGHTUP_TIME/2))/(LIGHTUP_TIME/2)
    return temp

def update_neibors(k):
    global phase
    for i in range(N):
        if i == k or phase[i] == CYCLE-LIGHTUP_TIME/2: # don't update phase for itself or fireflies at peak
            continue
        if phase[i] < CYCLE-LIGHTUP_TIME/2: # before peak
            phase[i] = min(CYCLE-LIGHTUP_TIME/2,phase[i]+PHASE_DELTA) # make sure don't pass the peak after incrementing phase
        else: # after peak
            phase[i] += PHASE_DELTA # increment phase by delta
            if phase[i] > CYCLE: # phase passed CYCLE
                phase[i] -= CYCLE # make sure stays within CYCLE
        v[i] = compute_brightness(phase[i]) # with new phase, update the brightness
                
def update_brightness():
    global phase,v
    for i in range(N):
        phase[i] += TIMER_VALUE/1000 # increase the phase by time passed
        if phase[i] > CYCLE: # phase passed CYCLE
            phase[i] -= CYCLE # make sure phase stays within CYCLE
        if phase[i] > CYCLE-LIGHTUP_TIME/2 and phase[i] - TIMER_VALUE/1000 < CYCLE-LIGHTUP_TIME/2: # skipped peak
            phase[i] = CYCLE-LIGHTUP_TIME/2 #cheat here: adjust phase to peak value 
        v[i] = compute_brightness(phase[i]) # compute the brightness based on phase

    for i in range(N): # update other fireflies
       if phase[i] == CYCLE-LIGHTUP_TIME/2: # only update when firefly is in peak
            update_neibors(i) # try to influence other fireflies

def update_position():
    global current_xpos,current_ypos,target_xpos,target_ypos
    for i in range(N):
        # move towards target SPEED/FPS steps
        # figure out angle to target first
        angle_to_target = math.atan2(target_ypos[i]-current_ypos[i],target_xpos[i]-current_xpos[i])
        # compute changes to current position based on the angle and distance to move per 1/FPS second.
        current_xpos[i] += SPEED/FPS*math.cos(angle_to_target)
        current_ypos[i] += SPEED/FPS*math.sin(angle_to_target)
        # check to see if close enough to target.
        dist_to_target_squared = (current_xpos[i]-target_xpos[i])**2 + (current_ypos[i]-target_ypos[i])**2
        if dist_to_target_squared < CLOSE_ENOUGH: # close enough, set new target
            target_xpos[i] = random.randint(-500,500) # target x coordinate, random location
            target_ypos[i] = random.randint(-500,500) # target y coordinate, random location
        
def update_states():
    global should_draw
    update_brightness()
    update_position()
    should_draw = True
    screen.ontimer(update_states,TIMER_VALUE)

def draw():
    global v,fireflies,should_draw,current_xpos,current_ypos
    if should_draw == False: # There is no change. Don't draw and return immediately
        return
    for i in range(N):
        fireflies[i].clear() # clear the current drawing
        color = colorsys.hsv_to_rgb(H_YELLOWGREEN,1,v[i]) # use colorsys to convert HSV to RGB color
        fireflies[i].color(color)
        fireflies[i].goto(current_xpos[i],current_ypos[i])
        fireflies[i].dot(10)
    should_draw = False # just finished drawing, set should_draw to False

screen.bgcolor('black')
initialze_fireflies()                
update_states()
while True:
    draw() # draw forever
    screen.update()