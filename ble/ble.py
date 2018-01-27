import pygatt
import logging


PYGATT_DEBUG = False
if PYGATT_DEBUG:
    logging.basicConfig()
    logging.getLogger('pygatt').setLevel(logging.DEBUG)

BLE_DEBUG = True
if BLE_DEBUG:
    logging.basicConfig()
    logging.getLogger('ble').setLevel(logging.DEBUG)

ADDRESS_TYPE = pygatt.BLEAddressType.random


class BLEAdapter(object):
    """A wrapper for the BGAPI backend from the pygatt library."""
    def __init__(self):
        self.oldadapter = pygatt.BGAPIBackend()

    @property
    def nearby_devices(self):
        try:
            devices = NearbyDevices(self.oldadapter.scan(timeout=2,
                                                         active=False))
            logging.info('Found %i devices nearby.' % len(devices))
            return devices
        except Exception:
            logging.debug('Error scanning devices.')
            return None

    def start(self):
        try:
            self.oldadapter.start()
            logging.info('Connected to the ble adapter.')
            return True
        except pygatt.backends.exceptions.BGAPIError:
            logging.debug('Connected to ble adapter.')
            return False

    def stop(self):
        try:
            self.adapter.stop()
            logging.info('Error connecting to ble adapter.')
            return True
        except pygatt.backends.exceptions.BGAPIError:
            logging.debug('Error disconnecting from ble adapter.')
            return False

    def connect(self, addr):
        try:
            device = Device(self.oldadapter.connect(addr,
                                                    address_type=ADDRESS_TYPE))
            logging.info('Connected to device Address: %s.' %  addr)
            return device
        except Exception:
            logging.debug('Failed to connect to Address: %s.' % addr)
            return None

    def is_started(self):
        return self.adapter.adapter_started()


class Device(object):

    def __init__(self, connection):
        self.connection = connection

    @property
    def rssi(self):
        try:
            rssi = self.connection.get_rssi()
            logging.info('Received rssi: %i' % rssi)
            return rssi
        except Exception:
            logging.debug('Failed to retrieve rssi.')

    def disconnect(self):
        try:
            self.connection.disconnect()
            logging.info('Disconnected device.')
        except Exception:
            logging.debug('Failed to disconnected device.')

    def is_connected(self):
        return self.connection.connected()


class NearbyDevices(object):

    def __init__(self, scanresults):
        self.scanresults = scanresults

    def __len__(self):
        return len(self.scanresults)

    def __getitem__(self, index):
        if index >= len(self):
            raise IndexError
        return ScannedDevice(self.scanresults[index])


class ScannedDevice(object):

    def __init__(self, device):
        self.device = device

    @property
    def name(self):
        return self.device['name']

    @property
    def rssi(self):
        return self.device['rssi']

    @property
    def manufacturer_specific_data(self):
        packet_data = self.device['packet_data']
        adv_packet = packet_data['connectable_advertisement_packet']
        return adv_packet['manufacturer_specific_data']


if __name__ == '__main__':
    pass
