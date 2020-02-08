import os

from phue import Bridge


def connect():
    ip = os.getenv('HUE_BRIDGE_IP')
    b = Bridge(ip)
    try:
        b.connect()
    except Exception:
        print('Failed to connect to Hue Bridge')
        raise

    return b
