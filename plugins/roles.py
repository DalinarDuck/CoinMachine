import discord
from discord.ext import commands
from discord import Message
import re

from time import sleep


class RoleManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.color_reg = '^#[A-Fa-f0-9]{6}'

    @commands.command(aliases=["roleedit","re"], pass_context=True)
    @commands.has_permissions(administrator = True)
    async def roleEdit(self, ctx):
        chan = ctx.channel
        print('--->')
        role_id = ctx.message.role_mentions[0].id
        print(role_id)
        role = discord.utils.get(ctx.guild.roles, id=role_id)
        print(role)
        args = ctx.message.content.split('~')
        for arg in args:
            #look for color
            if arg.startswith('color'):
                print('Validating color')
                color = arg.split(' ')[1]
                valid_color = re.match(self.color_reg, color)
                if valid_color != None:
                    print('valid color')
                    #convert to tuple
                    color = color.strip('#')
                    r,g,b = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
                    print(r,g,b)
                    c = discord.Colour.from_rgb(r,g,b)
                    print(type(c))
                    await chan.send('found color! {}'.format(c))
                    await role.edit(color=c)
                continue
            if arg.startswith('name'):
                name = ' '.join(arg.split(' ')[1:])
                if name != '':
                    await chan.send('found name! {}'.format(name))
                    await role.edit(name=name)
                continue
        print('--->')
        print('Done')


def setup(bot):
    bot.add_cog(RoleManager(bot))
