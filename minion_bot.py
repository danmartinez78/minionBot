import os # for importing env vars for the bot to use
from twitchio.ext import commands
from dotenv import load_dotenv
load_dotenv(dotenv_path='.env')
from minion_arm import MinionArm
import time

class Bot(commands.Bot):

    def __init__(self):
        super().__init__(irc_token=os.environ['TMI_TOKEN'],
    client_id=os.environ['CLIENT_ID'],
    nick=os.environ['BOT_NICK'],
    prefix=os.environ['BOT_PREFIX'],
    initial_channels=[os.environ['CHANNEL']])
        self.last_run = 0
        self.myarm = MinionArm()
        self.myarm.flip()
        self.myarm.flip()

    async def event_ready(self):
        'Called once when the bot goes online.'
        print(f"{os.environ['BOT_NICK']} is online!")
        ws = bot._ws  # this is only needed to send messages within event_ready
        self.myarm.home()
        await ws.send_privmsg(os.environ['CHANNEL'], f"/me has been activated!")

    async def event_message(self, ctx):
        'Runs every time a message is sent in chat.'

        # make sure the bot ignores itself and the streamer
        if ctx.author.name.lower() == os.environ['BOT_NICK'].lower():
            return

        await bot.handle_commands(ctx)
        
        if 'hello' in ctx.content.lower():
            await ctx.channel.send(f"Hi, @{ctx.author.name}!")

    @commands.command(name='test')
    async def test(self, ctx):
        await ctx.send('test passed!')

    @commands.command(name='flip')
    async def flip(self, ctx):
        if time.time() - self.last_run > 5000:
            await ctx.send('Flipping, please wait...')
            self.myarm.flip()
            await ctx.send('Behold! The Gaussian Distribution!')
            self.myarm.flip()
            await ctx.send('Done! Ready for next demonstration!')
            self.last_run = time.time()
        else:
            pass

    @commands.command(name='info')
    async def info(self, ctx):
        time.sleep(1)
        await ctx.send('The Galton Board, is a device invented by Sir Francis Galton to demonstrate the central limit theorem!')
        time.sleep(3)
        await ctx.send('My creator, roboticdaniel, has tasked me to flip the Galton Board at your command!')
        time.sleep(3)
        await ctx.send('Type !flip to flip the Galton Board.')

    @commands.command(name='relax')
    async def relax(self, ctx):
        await ctx.send('Moving to relaxed position...')
        self.myarm.downward_home()
        time.sleep(3)
        await ctx.send('Done!')

# bot = commands.Bot(
#     # set up the bot
#     irc_token=os.environ['TMI_TOKEN'],
#     client_id=os.environ['CLIENT_ID'],
#     nick=os.environ['BOT_NICK'],
#     prefix=os.environ['BOT_PREFIX'],
#     initial_channels=[os.environ['CHANNEL']]
# )

if __name__ == "__main__":
    bot = Bot()
    bot.run()