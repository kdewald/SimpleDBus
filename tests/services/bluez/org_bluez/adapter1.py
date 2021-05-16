from dbus_next.aio import MessageBus
from dbus_next.service import ServiceInterface, method, dbus_property, signal, PropertyAccess
from dbus_next import Variant, DBusError

import asyncio
import random

class Adapter1(ServiceInterface):
    def __init__(self, bus, path):
        self.bus = bus
        self.path = path
        super().__init__('org.bluez.Adapter1')
        self._discovering = False
        self._address = "00:00:00:00:00:00"

    def export(self):
        self.bus.export(f'/org/bluez/{self.path}', self)

    @method()
    def SetDiscoveryFilter(self, properties: 'a{sv}'):
        return

    @method()
    async def StartDiscovery(self):
        await self._update_discoverying(True)
        return

    @method()
    async def StopDiscovery(self):
        await self._update_discoverying(False)
        return

    @dbus_property(access=PropertyAccess.READ)
    def Discoverying(self) -> 'b':
        return self._discovering

    async def _update_discoverying(self, new_value: bool):
        await asyncio.sleep(random.uniform(0.5, 2.5))
        self._discovering = new_value
        self.emit_properties_changed({'Discovering': self._discovering})
        
