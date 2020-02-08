# TODO: better name
class BridgeInterface():
    def __init__(self):
        pass

    def show_lights(self):
        pass

    def find_lights(self):
        pass

    def set_light_brightness(self, light, brightness):
        if brightness < 0 or brightness > 256:
            raise Exception('Brightness must be between 0 and 256')
