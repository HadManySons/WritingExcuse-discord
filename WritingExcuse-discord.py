import discord
import random
import logging
import time
import os
import sys
from BotCreds import credsClientSecret, admins

# Initialize a logging object and have some examples below from the Python
logging.basicConfig(filename='WritingExcuse-discord.log', level=logging.INFO)

# Get the PID of this process
pid = str(os.getpid())
pidfile = "WritingExcuse-discord.pid"

# Exit if a instance of the bot is already running
if os.path.isfile(pidfile):
    print(pidfile + " already running, exiting")
    sys.exit()

# Create the lock file for the bot
open(pidfile, 'w').write(pid)

logging.info(time.strftime("%Y/%m/%d %H:%M:%S ") + "Starting bot")

#Discord API initialization
client = discord.Client()

@client.event
async def on_ready():
    print(f"Bot has logged in as {client.user}")
    logging.info(time.strftime("%Y/%m/%d %H:%M:%S ") +
                 f"Bot has logged in as {client.user}")

# Initializes variables to be used as global variables inside the processing functions
globalCount = 0
restart = True

logging.info(time.strftime("%Y/%m/%d %H:%M:%S ") +
             "Starting processing loop")

triggerWords = ['WritingExcuse!']

@client.event
async def on_message(message):
    print(message.content)
    global globalCount
    global restart
    if message.author == client.user:
        return

    if "writingexcuse shutdown!" in message.content.lower():
        print("Shutting down due to @client on_message")
        await message.channel.send("WritingExcuse bot shutting down due to request by " + f"{message.author}")
        logging.info(time.strftime("%Y/%m/%d %H:%M:%S ") +
                     f"Shutting down due to request from {message.author}")
        restart = False
        sys.exit(2)

    if "writingexcuse restart!" in message.content.lower():
        print("Restarting due to @client on_message")
        await message.channel.send("WritingExcuse bot restarting due to request by " + f"{message.author}")
        logging.info(time.strftime("%Y/%m/%d %H:%M:%S ") +
                     f"Restarting due to request from {message.author}")
        restart = True
        sys.exit(1)

    if "writingexcuse!" in message.content.lower():
        globalCount += 1
        print("\nMessages processed since start of bot: " + str(globalCount))
        print(f"Processing message: {message.content} from: {message.author}")

        # Initialize dalist
        #dalist = []
        with open('Excuses.txt', 'r') as f:
            dalist = f.read().splitlines()
        print("Dropping an excuse on: " + f"{message.author}")
        logging.info(time.strftime("%Y/%m/%d %H:%M:%S ") +
                     "Dropping an excuse on: " + f"{message.author}")

        await message.channel.send(str((dalist[random.randint(0, len(dalist) - 1)])))


# starts the main processing loop, handles exceptions
while True:
    try:
        client.run(credsClientSecret)

    # what to do if Ctrl-C is pressed while bot is running
    except KeyboardInterrupt:
        print("Keyboard Interrupt experienced, exiting")
        logging.info(time.strftime("%Y/%m/%d %H:%M:%S ") +
                     "Exiting due to keyboard interrupt")
        sys.exit(0)

    # prints and handles unhandled exceptions
    except Exception as err:
        print("Exception: " + str(err.with_traceback()))
        logging.info(time.strftime("%Y/%m/%d %H:%M:%S ") +
                     f"Unhandled exception: {str(err.with_traceback())}")

    finally:
        if restart == True:
            os.unlink(pidfile)
            sys.exit(1)
        else:
            sys.exit(2)
