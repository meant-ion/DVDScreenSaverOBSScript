# DVDScreenSaverOBSScript
Basic script that uses websockets to listen to Twitch's PubSub API and make the camera behave like a DVD screen saver when a channel points reward is redeemed

Currently, there is an issue with getting it to not freeze OBS when activated, 
due to it waiting on the script to finish executing. Any and all help with this
issue would be greatly appreciated and welcome.

I believe the issue is to do with the PubSub API listener, as that runs constantly, 
waiting for the channel points redemption. I don't know exactly how to make it run on 
a separate thread from the rest of OBS so it does not freeze the program.