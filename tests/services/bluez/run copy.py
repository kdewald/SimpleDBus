from dbus_next.aio import MessageBus
from dbus_next.service import (ServiceInterface,
                               method, dbus_property, signal)
from dbus_next import Variant, DBusError

import asyncio

from org_bluez import Application



class ExampleInterface(ServiceInterface):
    def __init__(self):
        super().__init__('com.example.SampleInterface0')
        self._bar = 105

    @method()
    def Frobate(self, foo: 'i', bar: 's') -> 'a{us}':
        print(f'called Frobate with foo={foo} and bar={bar}')

        return {
            1: 'one',
            2: 'two'
        }

    @method()
    async def Bazify(self, bar: '(iiu)') -> 'vv':
        print(f'called Bazify with bar={bar}')

        return [Variant('s', 'example'), Variant('s', 'bazify')]

    @method()
    async def Hello(self) -> 'vv':
        print(f'called Hello with')

        return [Variant('s', 'example'), Variant('s', 'bazify')]

    @method()
    def Mogrify(self, bar: '(iiav)'):
        raise DBusError('com.example.error.CannotMogrify',
                        'it is not possible to mogrify')

    @signal()
    def Changed(self) -> 'b':
        return True

    @dbus_property()
    def Bar(self) -> 'y':
        return self._bar

    @Bar.setter
    def Bar(self, val: 'y'):
        if self._bar == val:
            return

        self._bar = val

        self.emit_properties_changed({'Bar': self._bar})

async def main():
    bus = await MessageBus().connect()
    interface = ExampleInterface()
    application = Application(bus)
    bus.export('/com/example/sample0', interface)
    await bus.request_name('com.example.name')

    # emit the changed signal after two seconds.
    # await asyncio.sleep(8)

    bus.export('/', application)

    interface.Changed()

    await bus.wait_for_disconnect()

asyncio.get_event_loop().run_until_complete(main())