import discord
from discord.ext import commands
from discord import Message
import random
from time import sleep 


class Fortune(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.names = {}
        self.fortuneList = [
            "People are naturally attracted to you.",
            "You learn from your mistakes... You will learn a lot today.",
            "If you have something good in your life, don't let it go!",
            "What ever you're goal is in life, embrace it visualize it, and for it will be yours.",
            "Your shoes will make you happy today.",
            "You cannot love life until you live the life you love.",
            "Be on the lookout for coming events; They cast their shadows beforehand.",
            "Land is always on the mind of a flying bird.",
            "The man or woman you desire feels the same about you.",
            "Meeting adversity well is the source of your strength.",
            "A dream you have will come true.",
            "Our deeds determine us, as much as we determine our deeds.",
            "Never give up. You're not a failure if you don't give up.",
            "You will become great if you believe in yourself.",
            "There is no greater pleasure than seeing your loved ones prosper.",
            "You will marry your lover.",
            "The greatest love is self-love.",
            "A very attractive person has a message for you.",
            "You already know the answer to the questions lingering inside your head.",
            "It is now, and in this world, that we must live.",
            "You must try, or hate yourself for not trying.",
            "You can make your own happiness.",
            "The greatest risk is not taking one.",
            "The love of your life is stepping into your planet this summer.",
            "Love can last a lifetime, if you want it to.",
            "Adversity is the parent of virtue.",
            "Serious trouble will bypass you.",
            "A short stranger will soon enter your life with blessings to share.",
            "Now is the time to try something new.",
            "Wealth awaits you very soon.",
            "If you feel you are right, stand firmly by your convictions.",
            "If winter comes, can spring be far behind?",
            "Keep your eye out for someone special.",
            "You are very talented in many ways.",
            "A stranger, is a friend you have not spoken to yet.",
            "A new voyage will fill your life with untold memories.",
            "You will travel to many exotic places in your lifetime.",
            "Your ability for accomplishment will follow with success.",
            "Nothing astonishes men so much as common sense and plain dealing.",
            "Its amazing how much good you can do if you dont care who gets the credit.",
            "Everyone agrees. You are the best.",
            "LIFE CONSISTS NOT IN HOLDING GOOD CARDS, BUT IN PLAYING THOSE YOU HOLD WELL.",
            "Jealousy doesn't open doors, it closes them!",
            "It's better to be alone sometimes.",
            "When fear hurts you, conquer it and defeat it!",
            "Let the deeds speak.",
            "You will be called in to fulfill a position of high honor and responsibility.",
            "The man on the top of the mountain did not fall there.",
            "You will conquer obstacles to achieve success.",
            "Joys are often the shadows, cast by sorrows.",
            "Fortune favors the brave."
        ]
        print("Loaded {} Fortunes".format(len(self.fortuneList)))

    @commands.command(aliases=["fortune","<:token:936532179066949672>"], pass_context=True)
    async def coin_fortune(self, ctx):
        fortune = random.choice(self.fortuneList)
        await ctx.message.reply('Your Fortune: {}'.format(fortune))

    @commands.command(aliases=["magic","daldance"], pass_context=True)
    async def dal_magic(self,ctx):
        member = ctx.author
        role = discord.utils.get(member.guild.roles, id=983848818732843058)
        print(role)
        for x in range(100):
            c = discord.Colour.from_rgb(random.randint(1,255), random.randint(1,255), random.randint(1,255))
            await role.edit(color=c)
            sleep(1)

    @commands.command(aliases=["1/99","chance"], pass_context=True)
    async def _50(self,ctx):
        if ctx.author not in list(self.names.keys()):
            if random.randint(1,100) == 1:
                await ctx.message.reply("Congrats you are a girl now")
                self.names[ctx.author] = "You are a Girl Now"
            else:
                await ctx.message.reply("You only won $1 million, try again later")
                self.names[ctx.author] = "You won the $1 Mil"
        else:
            await ctx.message.reply("you already played and got: {}".format(self.names[ctx.author]))

def setup(bot):
    bot.add_cog(Fortune(bot))
