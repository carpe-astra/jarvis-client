import asyncio

import kasa

dev1 = kasa.SmartPlug("10.0.0.101")
dev2 = kasa.SmartPlug("10.0.0.102")
devs = (dev1, dev2)


async def _turn_on():
    for dev in devs:
        await dev.update()
        await dev.turn_on()


async def _turn_off():
    for dev in devs:
        await dev.update()
        await dev.turn_off()


def turn_on():
    """Turns the bed heater on."""
    loop = asyncio.get_event_loop()
    loop.run_until_complete(_turn_on())


def turn_off():
    """Turns the bed heater off."""
    loop = asyncio.get_event_loop()
    loop.run_until_complete(_turn_off())
