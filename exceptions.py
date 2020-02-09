class InvalidLightIDError(Exception):
    pass


class InvalidHueError(Exception):
    message = 'Invalid hue value - hue must be between 0 and 65535'


class InvalidBrightnessError(Exception):
    message = 'Invalid brightness value - brightness must be between 0 and 255'
