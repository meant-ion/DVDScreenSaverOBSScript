import os
from PubSubHandler import PubSubHandler
import asyncio
import obspython as S


def script_description():
    return "Boots up the script that makes the camera move like a DVD screen saver when a channel points reward is " \
           "redeemed "


# Makes the button that activates the script when pressed
# def script_properties():
#     props = S.obs_properties_create()
#     S.obs_properties_add_button(props, "button1", "Activate Screen Saver Script", boot_pubsubclient())
#     return props


# async def boot_pubsubclient():
client = PubSubHandler()
loop = asyncio.get_event_loop()

if not loop.run_until_complete(client.connect()):
    exit(1)

connection = loop.run_until_complete(client.connect())

tasks = [
    asyncio.ensure_future(client.pingus(connection)),
    asyncio.ensure_future(client.recv_msg(connection)),
]

for task in tasks:
    loop.create_task(task)

try:
    loop.run_forever()
except KeyboardInterrupt:
    pass
except Exception as e:
    print(f'Exception caught: {e!r}')

# loop.run_until_complete(asyncio.wait(tasks))
# future = asyncio.run_coroutine_threadsafe(coro, loop)
#
# try:
#     result = future.result(timeout=5000)
# except concurrent.futures.TimeoutError:
#     print("Coroutines took too long, killing tasks now...")
#     future.cancel()
# except Exception as e:
#     print(f"Exception raised: {e!r}")
# else:
#     print(f"Coroutine finished with {result!r}")

