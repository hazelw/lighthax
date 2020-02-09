from connection import Connection
from exceptions import (
    InvalidLightIDError, InvalidHueError, InvalidBrightnessError
)


def validate_light_id(light_id):
    # TODO: not this
    connection = Connection().connect()
    if light_id not in [l.light_id for l in connection.lights]:
        raise InvalidLightIDError


def validate_hue(hue):
    if hue < 0 or hue > 65535:
        raise InvalidHueError


def validate_brightness(brightness):
    if brightness < 0 or brightness > 255:
        raise InvalidBrightnessError
