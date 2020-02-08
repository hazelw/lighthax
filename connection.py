import os

from phue import Bridge


class Connection:
    connection = None

    def connect(self):
        if self.connection:
            return self.connection

        ip = os.getenv('HUE_BRIDGE_IP')
        b = Bridge(ip)
        try:
            b.connect()
        except Exception:
            print('Failed to connect to Hue Bridge')
            raise

        self.connection = b
        return self.connection
