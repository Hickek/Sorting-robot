#!/usr/bin/env pybricks-micropython

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, TouchSensor, ColorSensor
from pybricks.parameters import Port, Stop, Direction, Button
from pybricks.tools import wait
from pybricks.messaging import BluetoothMailboxServer, TextMailbox
import threading
import time



ev3 = EV3Brick()

gripper_motor = Motor(Port.A)

# Configure the elbow motor. It has an 8-teeth and a 40-teeth gear
# connected to it.
elbow_motor = Motor(Port.B, Direction.COUNTERCLOCKWISE, [8, 40])

# Configure the motor that rotates the base. It has a 12-teeth and a
# 36-teeth gear connected to it.
base_motor = Motor(Port.C, Direction.COUNTERCLOCKWISE, [12, 36])

base_switch = TouchSensor(Port.S1)

elbow_sensor = ColorSensor(Port.S2)


belt_menu_options = ["Yes", "No"]
belt_selected_option = 0

def display_belt_menu(belt_selected_option):
    ev3.screen.clear()
    for idx, belt_option in enumerate(belt_menu_options):

        ev3.screen.draw_text(10, 20, "Connect conveyor belt?")

        if idx == belt_selected_option:
            ev3.screen.draw_text(10, 20 * idx + 40, "-> " + belt_option)
        else:
            ev3.screen.draw_text(10, 20 * idx + 40, belt_option)

def belt_menu(belt_selected_option):
    while True:
        display_belt_menu(belt_selected_option)

        wait(200)
        while not any(ev3.buttons.pressed()):
            wait(10)

            # Handle button press
            wait(200)  # Debounce delay
            if Button.UP in ev3.buttons.pressed():
                belt_selected_option = (belt_selected_option - 1) % len(belt_menu_options)
            elif Button.DOWN in ev3.buttons.pressed():
                belt_selected_option = (belt_selected_option + 1) % len(belt_menu_options)
            elif Button.CENTER in ev3.buttons.pressed():
                if belt_selected_option == 0:
                    return True
                if belt_selected_option == 1:
                    return False

belt = belt_menu(belt_selected_option)


# Zone Declarations
PICKUP_ZONE = 205
ZONE_1 = 5
ZONE_2 = 45
ZONE_3 = 102
EMERGENCY_ZONE = 155

# Define menu options
menu_options = ["Emergency", "Pause", "Schedule", "Change Zones"]
zone_menu_options = ["Back to menu", "Pickup", "Drop-off 1", "Drop-off 2", "Drop-off 3", "Emergency Zone"]
zone_choice_menu_options = ["Back", "0 Degrees", "45 Degrees", "90 Degrees", "135 Degrees", "180 Degrees"]
schedule_menu_options = ["Back to menu", "1 minute", "10 Minutes", "30 minutes", "1 Hour", "Nonstop running"]
selected_option = 0
zone_selected_option = 0
zone_choice_selected_option = 0
schedule_selected_option = 0
paused = False

found_color = "None"

# Function to display menu
def display_menu():
    ev3.screen.clear()
    ev3.screen.draw_text(10, 10, "Color: " + found_color)
    for idx, option in enumerate(menu_options):

        if idx == selected_option:
            ev3.screen.draw_text(10, 20 * idx + 40, "-> " + option)
        else:
            ev3.screen.draw_text(10, 20 * idx + 40, option)

def display_zone_menu(zone_selected_option):
    ev3.screen.clear()
    for idx, zone_option in enumerate(zone_menu_options):

        if idx == zone_selected_option:
            ev3.screen.draw_text(10, 20 * idx, "-> " + zone_option)
        else:
            ev3.screen.draw_text(10, 20 * idx, zone_option)

def display_zone_choice_menu(zone_choice_selected_option):
    ev3.screen.clear()
    for idx, zone_choice_option in enumerate(zone_choice_menu_options):

        if idx == zone_choice_selected_option:
            ev3.screen.draw_text(10, 20 * idx, "-> " + zone_choice_option)
        else:
            ev3.screen.draw_text(10, 20 * idx, zone_choice_option)

def display_schedule_menu(schedule_selected_option):
    ev3.screen.clear()
    for idx, schedule_option in enumerate(schedule_menu_options):

        if idx == schedule_selected_option:
            ev3.screen.draw_text(10, 20 * idx, "-> " + schedule_option)
        else:
            ev3.screen.draw_text(10, 20 * idx, schedule_option)


paused = False

def pause():
    global paused
    paused = True

def resume():
    global paused
    paused = False
    if belt == True:
        mbox.send("Continue")

def shutdown():
    global paused
    paused = True
    wait(1000)
    elbow_motor.run_target(20, 30)
    base_motor.run_target(20, EMERGENCY_ZONE)
    elbow_motor.run_until_stalled(-20, duty_limit=-10)
    gripper_motor.run_target(20, -90)

def is_paused():
    return paused

def pause_check():
    while is_paused():
        time.sleep(0.1)
    if belt == True:
        mbox.send("Pause")

#Connect conveyor belt
if belt is True:

    server = BluetoothMailboxServer()
    mbox = TextMailbox('greeting', server)


    # The server must be started before the client!)
    ev3.screen.clear()
    ev3.screen.draw_text(10, 20, 'Connecting...')
    server.wait_for_connection()
    ev3.screen.clear()
    ev3.screen.draw_text(10, 20, 'Connected!')

    # In this program, the server waits for the client to send the first message
    # and then sends a reply.

elbow_motor.run_time(30, 2000)
elbow_motor.run_until_stalled(-10, then=Stop.HOLD, duty_limit=6)
elbow_motor.reset_angle(-10)
elbow_motor.hold()

# Initialize the base. First rotate it until the Touch Sensor
# in the base is pressed. Reset the motor angle to make this
# the zero point. Then hold the motor in place so it does not move.
elbow_motor.run_target(30, 50)
base_motor.run(-60)
while not base_switch.pressed():
    wait(10)
base_motor.reset_angle(0)
base_motor.hold()

# Initialize the gripper. First rotate the motor until it stalls.
# Stalling means that it cannot move any further. This position
# corresponds to the closed position. Then rotate the motor
# by 90 degrees such that the gripper is open.
gripper_motor.run_until_stalled(100, then=Stop.COAST, duty_limit=50)
gripper_motor.reset_angle(0)
gripper_motor.run_target(100, -90)

# Play three beeps to indicate that the initialization is complete.
for i in range(3):
    ev3.speaker.beep()
    wait(100)

start_time = time.time()
duration = 1000000000

color_list = []
def color_detection():

    rgb = elbow_sensor.rgb()
    R = rgb[0]
    G = rgb[1]
    B = rgb[2]
    if max(rgb) == min(rgb):
        hue = -200
    elif R >= G and R >= B:
        hue = (G - B) / (max(rgb) - min(rgb))
    elif G >= R and G >= B:
        hue = 2 + (B - R) / (max(rgb) - min(rgb))
    elif B >= R and B >= G:
        hue = 4 + (R - G) / (max(rgb) - min(rgb))
    hue *= 60
    if hue < 0:
        hue += 360

    no_item = False
    if gripper_motor.angle() > -10:
        hue = -100
        no_item = True
        wait(5000)


    color_found = False
    if len(color_list) > 0 and not no_item:
        for color in color_list:
            diff = abs(hue - color)
            if diff > 180:
                diff = 360 - diff
            if diff <= 40:

                min_distance = 100000
                closest_color = None
                for color in color_list:
                    distance = abs(hue - color)
                    if distance < min_distance:
                        min_distance = distance
                        closest_color = color
                hue = closest_color


                col = color_list[0]
                for color in color_list:
                    if abs(hue - color) < abs(hue - col):
                        col = color
    else:
        col = hue

    if not color_found and not no_item:
        col = hue
        color_list.append(hue)
    elif no_item == True:
        col = hue

    return col

def robot_pick(position):
    pause_check()
    base_motor.run_target(400, position)
    pause_check()
    if belt == True:
        mbox.send("Continue")
    if belt is True:
        while True:
            rgb = elbow_sensor.rgb()
            R = rgb[0]
            G = rgb[1]
            B = rgb[2]
            if R + G + B > 5:
                wait(300)
                rgb = elbow_sensor.rgb()
                R = rgb[0]
                G = rgb[1]
                B = rgb[2]
                mbox.send("Pause")
                break
    pause_check()
    elbow_motor.run_target(60, 0)
    pause_check()
    pause_check()
    gripper_motor.run_until_stalled(200, then=Stop.HOLD, duty_limit=50)
    pause_check()
    if belt is False:
        elbow_motor.run_target(200, 29)
    pause_check()


def robot_release(position):
    pause_check()
    base_motor.run_target(400, position)
    pause_check()
    elbow_motor.run_until_stalled(-100, duty_limit=-10)
    pause_check()
    gripper_motor.run_target(200, -90)
    pause_check()
    elbow_motor.run_target(200, 60)
    pause_check()

def act_based_on_color():
    detected_color = color_detection()
    global found_color

    if detected_color == -100:
        found_color = "None"
    elif detected_color <= 10:
        found_color = "red"
    elif detected_color <= 20:
        found_color = "orange"
    elif detected_color <= 70:
        found_color = "yellow"
    elif detected_color <= 165:
        found_color = "green"
    elif detected_color <= 190:
        found_color = "cyan"
    elif detected_color <= 270:
        found_color = "blue"
    elif detected_color <= 300:
        found_color = "purple"
    elif detected_color <= 340:
        found_color = "pink"
    else:
        found_color = "red"

    pause_check()
    elbow_motor.run_target(200, 60)
    pause_check()

    if detected_color == -100:
        pause_check()
        gripper_motor.run_target(500, -90)
        pause_check()

    elif detected_color == color_list[0]:
        robot_release(ZONE_1)

    elif detected_color == color_list[1]:
        robot_release(ZONE_2)

    elif detected_color == color_list[2]:
        robot_release(ZONE_3)


def zone_menu(zone_selected_option, PICKUP_ZONE, ZONE_1, ZONE_2, ZONE_3, EMERGENCY_ZONE):
    while True:
        display_zone_menu(zone_selected_option)

        wait(200)
        while not any(ev3.buttons.pressed()):
            wait(10)

            # Handle button press
            wait(200)  # Debounce delay
            if Button.LEFT in ev3.buttons.pressed():
                shutdown()
            elif Button.UP in ev3.buttons.pressed():
                zone_selected_option = (zone_selected_option - 1) % len(zone_menu_options)
            elif Button.DOWN in ev3.buttons.pressed():
                zone_selected_option = (zone_selected_option + 1) % len(zone_menu_options)
            elif Button.CENTER in ev3.buttons.pressed():
                if zone_selected_option == 0:
                    zones = [PICKUP_ZONE, ZONE_1, ZONE_2, ZONE_3, EMERGENCY_ZONE]
                    return zones
                if zone_selected_option == 1:
                    temp = ZONE_1
                    PICKUP_ZONE = zone_choice_menu(zone_choice_selected_option)
                    if PICKUP_ZONE == -1:
                        PICKUP_ZONE = temp
                if zone_selected_option == 2:
                    temp = ZONE_1
                    ZONE_1 = zone_choice_menu(zone_choice_selected_option)
                    if ZONE_1 == -1:
                        ZONE_1 = temp
                if zone_selected_option == 3:
                    temp = ZONE_2
                    ZONE_2 = zone_choice_menu(zone_choice_selected_option)
                    if ZONE_2 == -1:
                        ZONE_2 = temp
                if zone_selected_option == 4:
                    temp = ZONE_3
                    ZONE_3 = zone_choice_menu(zone_choice_selected_option)
                    if ZONE_3 == -1:
                        ZONE_3 = temp
                if zone_selected_option == 5:
                    temp = EMERGENCY_ZONE
                    EMERGENCY_ZONE = zone_choice_menu(zone_choice_selected_option)
                    if EMERGENCY_ZONE == -1:
                        EMERGENCY_ZONE = temp

def zone_choice_menu(zone_choice_selected_option):
    while True:
        display_zone_choice_menu(zone_choice_selected_option)

        wait(200)
        while not any(ev3.buttons.pressed()):
            wait(10)

            # Handle button press
            wait(200)  # Debounce delay
            if Button.LEFT in ev3.buttons.pressed():
                shutdown()
            elif Button.UP in ev3.buttons.pressed():
                zone_choice_selected_option = (zone_choice_selected_option - 1) % len(zone_choice_menu_options)
            elif Button.DOWN in ev3.buttons.pressed():
                zone_choice_selected_option = (zone_choice_selected_option + 1) % len(zone_choice_menu_options)
            elif Button.CENTER in ev3.buttons.pressed():
                if zone_choice_selected_option == 0:
                    return -1
                if zone_choice_selected_option == 1:
                    return 5
                if zone_choice_selected_option == 2:
                    return 45
                if zone_choice_selected_option == 3:
                    return 102
                if zone_choice_selected_option == 4:
                    return 155
                if zone_choice_selected_option == 5:
                    return 205
                
def schedule_menu(schedule_selected_option):
    while True:
        display_schedule_menu(schedule_selected_option)

        wait(200)
        while not any(ev3.buttons.pressed()):
            wait(10)

            # Handle button press
            wait(200)  # Debounce delay
            if Button.LEFT in ev3.buttons.pressed():
                shutdown()
            elif Button.UP in ev3.buttons.pressed():
                schedule_selected_option = (schedule_selected_option - 1) % len(schedule_menu_options)
            elif Button.DOWN in ev3.buttons.pressed():
                schedule_selected_option = (schedule_selected_option + 1) % len(schedule_menu_options)
            elif Button.CENTER in ev3.buttons.pressed():
                if schedule_selected_option == 0:
                    return -1
                if schedule_selected_option == 1:
                    return 60 # 1 min
                if schedule_selected_option == 2:
                    return 600 # 10 min
                if schedule_selected_option == 3:
                    return 1800 # 30 min
                if schedule_selected_option == 4:
                    return 3600 # 1 Hour
                if schedule_selected_option == 5:
                    return 1000000000 # Forever


# This is the main part of the program. It is a loop that repeats endlessly.
def main_loop():

    elbow_motor.run_target(60, 70)
    pause_check()
    while True:
        while (time.time() - start_time) < duration:
            #pause_event.wait()
            pause_check()
            robot_pick(PICKUP_ZONE)
            #pause_event.wait()
            pause_check()
            act_based_on_color()  # Check color and act accordingly
            #pause_event.wait()
            pause_check()       


if __name__ == "__main__":
    main_thread = threading.Thread(target=main_loop)
    main_thread.start()

    while True:
        display_menu()

        # Wait for button press
        while not any(ev3.buttons.pressed()):
            wait(10)

        # Handle button press
        wait(200)  # Debounce delay
        if Button.LEFT in ev3.buttons.pressed():
                shutdown()
        elif Button.UP in ev3.buttons.pressed():
            selected_option = (selected_option - 1) % len(menu_options)
        elif Button.DOWN in ev3.buttons.pressed():
            selected_option = (selected_option + 1) % len(menu_options)
        elif Button.CENTER in ev3.buttons.pressed():

            if selected_option == 0:
                if belt == True:
                    mbox.send("Pause")
                shutdown()

            elif selected_option == 1:
                paused = not paused
                if paused == True:
                    menu_options[1] = "Resume"
                    if belt == True:
                        mbox.send("Pause")
                    pause()
                else:
                    menu_options[1] = "Pause"
                    if belt == True:
                        mbox.send("Continue")
                    resume()

            elif selected_option == 2:
                start_time = time.time()
                duration = schedule_menu(schedule_selected_option)

            elif selected_option == 3:
                zones = zone_menu(zone_selected_option, PICKUP_ZONE, ZONE_1, ZONE_2, ZONE_3, EMERGENCY_ZONE)
                PICKUP_ZONE = zones[0]
                ZONE_1 = zones[1]
                ZONE_2 = zones[2]
                ZONE_3 = zones[3]
                EMERGENCY_ZONE = zones[4]
