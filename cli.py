from connection import Connection


class BridgeInterface():
    connection = None

    def __init__(self):
        c = Connection()
        self.connection = c.connect()

        while True:
            text = input().lower()
            if text == 'show lights':
                self.show_lights()
            elif text.startswith('set brightness for all lights to'):
                try:
                    brightness = int(text[32:])
                except ValueError:
                    print(f'Brightness must be a number - found {text[:34]}')
                self.set_brightness_for_all_lights(brightness)
            elif text.startswith('set brightness for light '):
                pass
            else:
                print('sorry, I didn\'t understand that')

    def show_lights(self):
        lights = self.connection.lights

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

    def set_brightness_for_all_lights(self, brightness):
        lights = self.connection.lights
        
        for light in lights:
            self.set_light_brightness(light.light_id, brightness)

    def set_light_brightness(self, light_id, brightness):
        assert light_id in [l.light_id for l in self.connection.lights], (
            'Light ID is not valid'
        )
        
        if brightness < 0 or brightness > 255:
            raise Exception('Brightness must be between 0 and 255')

        self.connection.set_light(light_id, 'bri', brightness)
