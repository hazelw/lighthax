from actions import set_brightness_for_all_lights, show_lights


class BridgeInterface():
    def __init__(self):
        while True:
            text = input().lower()
            if text == 'show lights':
                show_lights()
            elif text.startswith('set brightness for all lights to'):
                try:
                    brightness = int(text[32:])
                except ValueError:
                    print(f'Brightness must be a number - found {text[:34]}')
                set_brightness_for_all_lights(brightness)
            elif text.startswith('set brightness for light '):
                pass
            else:
                print('sorry, I didn\'t understand that')
