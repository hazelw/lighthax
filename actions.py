import random
import threading
import time

from connection import Connection
from constants import Colour
from exceptions import InvalidHueError
from validation import validate_light_id, validate_hue, validate_brightness


connection = Connection().connect()


def show_lights():
    lights = connection.lights

    if not len(lights):
        print('There are no lights currently connected')
        return

    print("Here are your current lights:")
    for light in lights:    
        info = [
            f'ID: {light.light_id}',
            f'Name: {light.name}',
            f'On: {light.on}',
            f'Brightness: {light.brightness}',
            f'Hue: {light.hue}',
            f'Saturation: {light.saturation}'
        ]
        print('\n'.join(info))
        print()


def set_brightness_for_all_lights(brightness):
    lights = connection.lights
    
    for light in lights:
        set_light_brightness(light.light_id, brightness)


def set_light_brightness(light_id, brightness):
    validate_light_id(light_id)
    validate_brightness(brightness)

    connection.set_light(light_id, 'bri', brightness)


def set_hue_for_all_lights(hue):
    lights = connection.lights

    for light in lights:
        set_light_hue(light.light_id, hue)


def set_light_hue(light_id, hue):
    validate_light_id(light_id)
    validate_hue(hue)

    connection.set_light(light_id, 'hue', hue)


def infinite_rainbow_all_lights(speed=0.001, force_synchronicity=False):
    lights = connection.lights

    if force_synchronicity:
        # we'll never get true synchronicity because single-threading but
        # this isn't a problem for the human eye (or at least... not a problem
        # for mine)
        first_light = lights[0]
        set_hue_for_all_lights(first_light.hue)

    threads = [
        threading.Thread(target=infinite_rainbow, args=(light.light_id, speed))
        for light in lights
    ]
    for thread in threads:
        thread.start()


def infinite_rainbow(light_id, speed=0.001):
    validate_light_id(light_id)

    light = connection.get_light(light_id)
    current_hue = light['state']['hue']

    while True:
        new_hue = current_hue + 100
        try:
            set_light_hue(light_id, new_hue)
        except InvalidHueError:
            new_hue = 0
            set_light_hue(light_id, new_hue)

        current_hue = new_hue
        time.sleep(speed)


def rise_and_fall_all_lights(speed=0.001, pause_length=10):
    lights = connection.lights

    threads = [
        threading.Thread(
            target=rise_and_fall,
            args=(light.light_id, speed, pause_length)
        )
        for light in lights
    ]
    for thread in threads:
        thread.start()


def rise_and_fall(light_id, speed=0.001, pause_length=10):
    validate_light_id(light_id)

    light = connection.get_light(light_id)
    current_hue = light['state']['hue']
    next_hue = random.choice(list(Colour)).value
    current_brightness = light['state']['bri']
    next_brightness = random.randint(0, 255)

    hue_change = 100 if next_hue > current_hue else -100
    brightness_change = 10 if next_brightness > current_brightness else -10

    hue_transition_complete = False
    brightness_transition_complete = False

    while True:
        if abs(current_hue - next_hue) < 100:
            hue_transition_complete = True
        if abs(current_brightness - next_brightness) < 10:
            brightness_transition_complete = True

        if hue_transition_complete and brightness_transition_complete:
            break

        current_hue = current_hue + hue_change
        current_brightness = current_brightness + brightness_change
        
        if not hue_transition_complete:
            set_light_hue(light_id, current_hue)
        if not brightness_transition_complete:
            set_light_brightness(light_id, current_brightness)
        time.sleep(speed)

    time.sleep(pause_length)
    rise_and_fall(light_id, speed=speed)
