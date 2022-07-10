import discord
from discord.ext import commands
from discord import Message

from utils import coins

import random
import requests
import sqlite3

from time import sleep


class Points(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.api = ''
        self.point_value = 50
        self.banned = [691930561878556703]
        #weights

        self.freq =   (80, 15, 3, 2,  1)  #percentage chance
        self.awards = (1,  5, 10, 20, 50) #associated values
        self.opt_out = []
        self.data = {
                '0':'0.01',
                '1':'0.01',
                '2':'0.01',
                '3':'0.01',
                '4':'0.01'
                } #data tracking

        self.emoji = ['903387628043399228', '930639677172637727','929773804866113546','903387621462532106','921855278176141363','929774058764116009','903021366700294204']

        self.tiers = {2:['930113331384188928','929599186574381097','929834083176038510','908447653006802994'],3:[ '903386835458330627','938799901289099304','938798609531539486','903387950149156894'],4:[ '938819182634618900','938799873069817937','903387626864779266','903387629461045289']}

        self.con = sqlite3.connect('settings.db')
        self.cur = self.con.cursor()
        self.cur.execute('SELECT * FROM opt_outs')
        self.r = self.cur.fetchall()
        for x in self.r:
            self.opt_out.append(int(x[1]))
        self.con.close()

        self.messages = ['Only if its hard! <:aaaaaaa:903022491365146684>']
        self.rp_chans = [986355001171533895,923646662369501225,938325320317145140,910329159362949154,916853844506447872,905191418908254258,905193712383053844,905193675297005569,937521458333249627,910574826199081040,910233033142071346,905194282745466920,905193587417948200,904049796912918528,909659404020908043,920381581053530122,904034692888678400,929832271018622976,916020436968570920,907966638714937385,907966602132226088,907784445447274526,908496116876722196]

        def event_gen(self):
            n = len(self.freq)
            cum_freq = []
            total = 0.0
            for p in self.freq:
                total += p
                cum_freq.append(total)

            def event_f(self):
                r = random.uniform(0,total)
                for i in range(n):
                    if cum_freq[i] >= r:
                        return i
            return event_f

        self.r_win = event_gen(self)
        print('-> ready!!')


    @commands.Cog.listener()
    async def on_message(self, message: Message):
        if message.content.startswith('XXXX') and message.author.id == 198428748712771584:
            self.rp_chans.append(message.channel.id)
            print('Addded: {}'.format(message.channel.id))
            await message.delete(delay=2)
        else: # here we start the long stuff for bonus points
            if message.channel.id in self.rp_chans:
                user = message.author.id
                server = message.guild.id
                p = self.r_win(self)
                if p > 0:
                    res = await coins.add_points(message, user, server, self.awards[p], self.api, print_success=False, print_error=False)
                    print(res)
                    if res:
                        print('points given')
                        if p >= 2:
                            e = await message.guild.fetch_emoji(random.choice(self.tiers[p]))
                            if message.author.id not in self.opt_out and p == 2:
                                await message.add_reaction(e)
                            elif message.author.id not in self.opt_out and p == 3:
                                await message.add_reaction(e)
                            elif message.author.id not in self.opt_out and  p == 4:
                                await message.add_reaction(e)
                            else:
                                print('{} opted out'.format(message.author.id))
                    else:
                        c = message.guild.get_channel(923775468333826079)
                        sleep(2)
                        await c.send('!givepoints <@{}> {}'.format(user, str(self.awards[p])))

def setup(bot):
    bot.add_cog(Points(bot))
