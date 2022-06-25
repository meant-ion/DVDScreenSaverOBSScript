from PubSubHandler import PubSubHandler
import asyncio
import obspython as S


def script_description():
    return "Boots up the script that makes the camera move like a DVD screen saver when a channel points reward is " \
           "redeemed "


def script_properties():
    props = S.obs_properties_create()
    S.obs_properties_add_button(props, "button1", "Activate Screen Saver Script", boot_pubsubclient())
    return props


def boot_pubsubclient():
    client = PubSubHandler()
    loop = asyncio.get_event_loop()

    connection = loop.run_until_complete(client.connect())

    tasks = [
        asyncio.ensure_future(client.pingus(connection)),
        asyncio.ensure_future(client.recv_msg(connection)),
    ]

    loop.run_until_complete(asyncio.wait(tasks))
