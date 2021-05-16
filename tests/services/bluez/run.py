from dbus_next.aio import MessageBus
from dbus_next.service import ServiceInterface, method, dbus_property, signal
from dbus_next import Variant, DBusError

import asyncio

from org_bluez import Application, Adapter1

async def main():
    bus = await MessageBus().connect()

    application = Application(bus)
    hci0 = Adapter1(bus, 'hci0')
    
    application.export()
    hci0.export()

    await bus.request_name('test.simpledbus')
    await bus.wait_for_disconnect()

asyncio.get_event_loop().run_until_complete(main())