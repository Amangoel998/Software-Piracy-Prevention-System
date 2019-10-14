#!/usr/bin/python3
import ctypes
from ctypes.util import find_library
from ctypes import Structure

class DBusError(Structure):
    _fields_ = [("name", ctypes.c_char_p),
                ("message", ctypes.c_char_p),
                ("dummy1", ctypes.c_int),
                ("dummy2", ctypes.c_int),
                ("dummy3", ctypes.c_int),
                ("dummy4", ctypes.c_int),
                ("dummy5", ctypes.c_int),
                ("padding1", ctypes.c_void_p),]


class HardwareUuid(object):
    def __init__(self, dbus_error=DBusError):
        self._hal = ctypes.cdll.LoadLibrary(find_library('hal'))
        self._ctx = self._hal.libhal_ctx_new()
        self._dbus_error = dbus_error()
        self._hal.dbus_error_init(ctypes.byref(self._dbus_error))
        self._conn = self._hal.dbus_bus_get(ctypes.c_int(1),
                                            ctypes.byref(self._dbus_error))
        self._hal.libhal_ctx_set_dbus_connection(self._ctx, self._conn)
        self._uuid_ = None

    def __call__(self):
        return self._uuid

    @property
    def _uuid(self):
        if not self._uuid_:
            udi = ctypes.c_char_p("/org/freedesktop/Hal/devices/computer")
            key = ctypes.c_char_p("system.hardware.uuid")
            self._hal.libhal_device_get_property_string.restype = \
                                                            ctypes.c_char_p
            self._uuid_ = self._hal.libhal_device_get_property_string(
                                self._ctx, udi, key, self._dbus_error)
        return self._uuid_

if __name__ == "__main__":
    get_uuid = HardwareUuid()
    print(get_uuid)