import os # for importing env vars for the bot to use
from twitchio.ext import commands
from dotenv import load_dotenv
load_dotenv(dotenv_path='.env')
from minion_arm import MinionArm
import time


myarm = MinionArm()

bot = commands.Bot(
    # set up the bot
    irc_token=os.environ['TMI_TOKEN'],
    client_id=os.environ['CLIENT_ID'],
    nick=os.environ['BOT_NICK'],
    prefix=os.environ['BOT_PREFIX'],
    initial_channels=[os.environ['CHANNEL']]
)

myarm.flip()
myarm.flip()

@bot.event
async def event_ready():
    'Called once when the bot goes online.'
    print(f"{os.environ['BOT_NICK']} is online!")
    ws = bot._ws  # this is only needed to send messages within event_ready
    myarm.home()
    await ws.send_privmsg(os.environ['CHANNEL'], f"/me has been activated!")

@bot.event
async def event_message(ctx):
    'Runs every time a message is sent in chat.'

    # make sure the bot ignores itself and the streamer
    if ctx.author.name.lower() == os.environ['BOT_NICK'].lower():
        return

    await bot.handle_commands(ctx)
    
    if 'hello' in ctx.content.lower():
        await ctx.channel.send(f"Hi, @{ctx.author.name}!")

@bot.command(name='test')
async def test(ctx):
    await ctx.send('test passed!')

@bot.command(name='flip')
async def flip(ctx):
    await ctx.send('Flipping, please wait...')
    myarm.flip()
    await ctx.send('Behold! The Gaussian Distribution!')
    myarm.flip()
    await ctx.send('Done! Ready for next demonstration!')

@bot.command(name='info')
async def info(ctx):
    await ctx.send('The Galton Board, is a device invented by Sir Francis Galton to demonstrate the central limit theorem!')
    time.sleep(3)
    await ctx.send('My creator, roboticdaniel, has tasked me to flip the Galton Board at your command!')
    time.sleep(3)
    await ctx.send('Type !flip to flip the Galton Board.')

if __name__ == "__main__":
    bot.run()