import threading
import time

from connection import Connection
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
        print('ID: ' + str(light.light_id))
        print('Name: ' + light.name)
        print('On?: ' + str(light.on))
        print('Brightness: ' + str(light.brightness))
        print('Hue: ' + str(light.hue))
        print('Saturation: ' + str(light.saturation))
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


def infinite_rainbow_all_lights(speed=0.1, force_synchronicity=False):
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


def infinite_rainbow(light_id, speed=0.1):
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
