import sqlite3
import discord
import requests
import logging
import configparser
import random
import textgraph
import os, re

from discord.ext import commands
from discord.ext.commands import Bot, when_mentioned_or

#from utils import config_file



clear = lambda: os.system('clear')

config = configparser.ConfigParser()
#logging.basicConfig(level=logging.INFO)


class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
    #super().__init__(command_prefix=when_mentioned_or('!?'))
    #
        self.server_api = 'xZDG_bA9Evp7D8yJEJ7sNCD_bes'
        self.server_id = '902982432251326504'
        self.h = {'accept':'application/json','X-API-KEY':self.server_api}
        self.url = 'https://discordhub.com/api/points/add'
        self.point = '50'
        self.opt_out = [566684556002983983]
        self.chans = ['929114597670158427','928540833114910820']
        self.freq_table = (80,15,3.0,2.0,1.0)
        self.events = (0,1,5,10,20)
        self.data = {
            '0':.01,
            '1':.01,
            '2':.01,
            '3':.01,
            '4':.01
            }

        self.emoji = [
            '903387628043399228',
            '930639677172637727',
            '929773804866113546',
            '903387621462532106',
            '921855278176141363',
            '929774058764116009',
            '903021366700294204'
            ]

        self.tiers = {2:['930113331384188928',
                '929599186574381097',
                '929834083176038510',
                '908447653006802994'
                ],

                3:[ '903386835458330627',
                '938799901289099304',
                '938798609531539486',
                '903387950149156894'
                ],

             4:[ '938819182634618900',
                '938799873069817937',
                '903387626864779266',
                '903387629461045289'
                ]}


        self.messages = ['Only if its hard! <:aaaaaaa:903022491365146684>']




        self.con = sqlite3.connect('settings.db')
        self.cur = self.con.cursor()
        self.cur.execute('SELECT * FROM opt_outs')
        self.r = self.cur.fetchall()
        for x in self.r:
            self.opt_out.append(int(x[1]))
        self.con.close()

    async def write_log(self, line):
        with open('log.txt','a') as f:
            f.write('-> {}\n'.format(line))

    def event_gen(self, freq_table):
        n = len(freq_table)
        cum_freq = []
        total = 0.0
        for p in freq_table:
            total += p
            cum_freq.append(total)

        def event_f(self):
            r = random.uniform(0,total)
            #print("Random number: {}".format(r))
            for i in range(n):
                if cum_freq[i] >= r:
                    return i
        return event_f


    async def print_graph(self, data):
        d = []
        for k in data.keys():
            d.append((k,data[k]))
        #print(d)
        w = 20
        h = 30
        #clear()
        #print(textgraph.horizontal(d,width=120))
        #print(d)


    async def gp(self, user_id, server_id, point_val, message, print_error = False, print_success = False):
        params = {'user_id':user_id,'server_id':server_id,'amount':point_val}
        r = requests.post(self.url, params=params, headers=self.h)
        if r.status_code == 200:
            if print_success:
                await message.channel.send('Successful: Gave <@{}> {} points'.format(user_id, point_val))
                return True
            else:
                print("|> Gave {} - {} bonus points".format(user_id, point_val))
                await self.write_log('{}'.format("|> Gave {} - {} bonus points".format(user_id, point_val)))
                return True
        else:
            if print_error:
                await message.channel.send('Unsuccessful: attempting to manually award the {} points'.format(point))
                return False
            else:
                print(params)
                print(r.url)
                print(r.status_code)
                return False


    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))
        self.r_win = self.event_gen(freq_table=self.freq_table)

    async def on_message(self, message):
        #global point
        #global data
        if str(message.guild.id) == '902982432251326504':
            if message.content.lower().startswith('!?disable'):
                self.opt_out.append(message.author.id)
                con = sqlite3.connect('settings.db')
                cur = con.cursor()
                s = "INSERT INTO opt_outs(discord_id) VALUES('{}')".format(message.author.id)
                cur.execute(s)
                con.commit()
                con.close()
            if 'fuck off bot' in message.content.lower():
                await message.channel.send("only if you do me hard!! <:aaaaaaa:903022491365146684>")
            if 'good bot' in message.content.lower():
                await message.channel.send("I can be your little pet!")
            if str(message.author.id) == '735147814878969968':
                if 'Thank you for bumping the server' in message.content:
                    m = message.content.split()
                    user_id = m[-1].replace('<','').replace('@','').replace('>','')
                    if await self.gp(user_id, self.server_id, self.point, message, True, True) == False:
                        await message.channel.send('Attempting to manually give points')
                        await message.channel.send('!givepoints <@{}> {}'.format(user_id, point))
            if message.content.startswith('!?points'):
                m = message.content.split()[1]
                self.point = m
                await message.channel.send('Set point value to {}'.format(self.point))
            if str(message.author.id) == '198428748712771584':
                if message.content.startswith('!?test'):
                    print('>> {} used the test command - Gave {} points'.format(message.author.name, point))
                    await self.write_log('>> {} used the test command'.format(message.author.name))
                    await self.gp(message.author.id, self.server_id, point, message, False)
                if message.content.startswith('!?ban'):
                    m = message.content.split()
                    if m[1] == 'chan':
                        print('channel blocking')
                    elif m[1] == 'name':
                        print('user blocking')
                    else:
                        print(m)
            if message.author.id not in self.opt_out and message.author.bot == False and str(message.channel.id) not in self.chans:
                p = self.r_win(self)
                if p > 0:
                    await self.gp(message.author.id, self.server_id, self.events[p], message)
                    if p >=2:
                        e = await message.guild.fetch_emoji(random.choice(self.tiers[p]))
                    if message.author.id not in self.opt_out and p == 2:
                        await message.add_reaction(e)
                    elif message.author.id not in self.opt_out and p == 3:
                        await message.add_reaction(e)
                    elif message.author.id not in self.opt_out and  p == 4:
                        await message.add_reaction(e)
                    else:
                        print('{} opted out'.format(message.author.id))
                self.data[str(p)] = self.data[str(p)] + 1 
            #await self.print_graph(self.data)
            if str(message.author.id) == '320458922580377602' and re.match('.+#\d{4} has \d+ points.', message.content):
                e = await message.guild.fetch_emoji(random.choice(self.emoji))
                await message.add_reaction(e)

    def run(self):
        print('hi')

    #


if __name__ == '__main__':
    client = MyClient()
    client.run('OTM2NDcyNjA2MDU4NjM1Mjg0.YfNsFA.tAj9k0lCEbTe5dSoimagfRONawk')
