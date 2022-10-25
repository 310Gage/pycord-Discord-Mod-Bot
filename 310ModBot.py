import asyncio
import discord
from discord.ext import commands
import aiohttp
import datetime
import warnings
import humanfriendly
from discord.utils import get

warnings.filterwarnings("ignore", category=DeprecationWarning)
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

bot.remove_command('help')


# CUSTOMIZE THIS OR BOT WILL NOT WORK

rolelist = [123123123, 123123123, 123123123]    # ENTER ALL YOUR MODERATORS ID's   (seperate multiple id's with `,`)
modLogs = bot.get_channel(000000000000)   #add the channel id in the ()  if you dont want logs ignore this
mod = ['example1', 'example2', 'example3']  # Can use (Mute, unMute, kick, Purge)
admin = ['example1', 'example2', 'example3']    # Can use (all mod commands, Ban, unBan, Say, Nuke)




@ bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name + '#' + str(bot.user.discriminator) +
          ' (' + str(bot.user.id) + ')')
    print('Connected to {} servers and {} users | {} shards'.format(
        len(bot.guilds), len(set(bot.get_all_members())), bot.shard_count))
    print('=============================================================')



@ bot.command(name="addrole")
@ commands.has_any_role('three.10')
async def addrole(ctx,member : discord.Member,  role: discord.Role):
    user = member
    await user.add_roles(role)


@ bot.command(name='nuke')
@ commands.has_any_role(*admin)
async def nuke(ctx, limit: int=None):
    mgs = []
    aaa = 0
    tmn = 0
    await ctx.send('Are you sure you want to start nuke? (Y/N)')
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        response = await bot.wait_for('message', check=check, timeout=30.0)
    except asyncio.TimeoutError:
        return

    if response.content.lower() not in ('yes', 'y'):
        await ctx.send('Aborted launch ')
        return
    
    else:
        perms = ctx.channel.overwrites_for(ctx.guild.default_role)
        perms.send_messages = False
        await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=perms)  # Im sure this is probably trash, it was a quick 5 min solution I came up with ((and it works)). I'll fix it up in the future.
        async for msg in ctx.message.channel.history(limit=limit):
            aaa += 1
            tmn += 1
            print(aaa)
        while aaa > 0:
             async for x in ctx.message.channel.history(limit=100):
                mgs.append(x)
             await ctx.message.channel.delete_messages(mgs)
             aaa -= 100
             print(aaa)
             mgs = []
        embed=discord.Embed(title="NUKE COMPLETE", description='%s messages have been nuked' %(tmn), color=0x51ff00)
        embed.set_thumbnail(url="https://media.giphy.com/media/26gscNQHswYio5RBu/giphy-downsized-large.gif")
        await ctx.send(embed=embed)
        perms.send_messages = True
        await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=perms)

@ nuke.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingAnyRole):
        embed = discord.Embed(
            title='Missing Permissions!',
            description='If this is an error please contant the server owner.',
            color=0x7B0B87
            )
        await ctx.send(embed = embed)
        return
    if isinstance(error, commands.CommandError):
        embed=discord.Embed(title="🚩__**ERROR**__🚩",description='A Error has occured.`', color=0xff0000)
        await ctx.send(embed = embed)
        return


@ bot.command(name='kick')
@ commands.has_any_role(*mod,*admin)
async def kick(ctx, member: discord.Member=None, *, reason=None):
    channel = modLogs
    if member is None:
        await ctx.send('🚫**Please provide a member** `!kick @user#1234 (reason)`')
        return
    if reason is None:
        await ctx.send('🚫**Please provide a reason** `!kick @user#1234 (reason)`')
        return
    if member.id == 937271579266678834:
        await ctx.send('**You cant do that.**')
        return
    if ctx.author.id == member.id:
        await ctx.send('You cant kick yourself bozo')
        return
    if any(role.id in rolelist for role in member.roles):
        await ctx.send('🚫**You cannot kick someone with kick permissions**')
        return
    else:
        await member.kick(reason=reason)
        embed=discord.Embed(title="👢user has been kicked", color=0xff0000)
        embed.add_field(name="__User__", value=member.mention, inline=False)
        embed.add_field(name="__Reason__", value=reason, inline=True)
        await ctx.send(embed=embed)
        await channel.send(embed=embed)

@ kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingAnyRole):
        embed=discord.Embed(
            title='Missing Permissions!',
            description='If this is an error please contant the server owner.',
            color=0x7B0B87
            )
        await ctx.send(embed=embed)
        return
    if isinstance(error, commands.CommandError):
        embed=discord.Embed(title="🚩__**ERROR**__🚩",
                            description='__**@ the user to kick them**__\n\n`!kick @user#1234 reason for kicking`', color=0xff0000)
        await ctx.send(embed=embed)
        return


@ bot.command(name='ban')
@ commands.has_any_role(*admin)
async def ban(ctx, member: discord.Member=None, *, reason=None):
    channel = modLogs
    if member is None:
        await ctx.send('🚫**Please provide a member** `!ban @user#1234 (reason)`')
        return
    if reason is None:
        await ctx.send('🚫**Please provide a reason** `!ban @user#1234 (reason)`')
        return
    if member.id == 937271579266678834:
        await ctx.send('**Hol up.** <:Pepega:937296750480343090> **youre joking right???**')
        return
    if ctx.author.id == member.id:
        await ctx.send('%s are you stupid?' % (ctx.author.mention))
        return
    if any(role.id in rolelist for role in member.roles):
        await ctx.send('🚫**You cannot ban other staff**')
        return
    else:
        await member.ban(reason=reason)
        embed=discord.Embed(title="👢user has been banned", color=0xff0000)
        embed.add_field(name="__User__", value=member.mention, inline=False)
        embed.add_field(name="__Reason__", value=reason, inline=True)
        await ctx.send(embed=embed)
        await channel.send(embed=embed)

@ ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingAnyRole):
        embed=discord.Embed(
            title='Missing Permissions!',
            description='If this is an error please contant the server owner.',
            color=0x7B0B87
            )
        await ctx.send(embed=embed)
        return
    if isinstance(error, commands.CommandError):
        embed=discord.Embed(title="🚩__**ERROR**__🚩",
                            description='__**Tag the user to ban them**__\n\n`!ban @user#1234 reason for banning`', color=0xff0000)
        await ctx.send(embed=embed)
        return


@ bot.command(pass_context=True)
@ commands.has_any_role(*mod,*admin)
async def purge(ctx, limit: int):
    if limit > 100:
        await ctx.send('You can only purge up to 100 messages at a time')
    else:
        await ctx.channel.purge(limit=limit+1)
        embed=discord.Embed(title="PURGE COMPLETE", description='%s Messages have been cleared by %s' % (
            limit, ctx.author.mention), color=0x51ff00)
        embed.set_thumbnail(
            url="https://media.giphy.com/media/26gscNQHswYio5RBu/giphy-downsized-large.gif")
        await ctx.send(embed=embed)

@ purge.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingAnyRole):
        embed=discord.Embed(
            title='Missing Permissions!',
            description='If this is an error please contant the server owner.',
            color=0x7B0B87
            )
        await ctx.send(embed=embed)
        return

@ bot.command(name='say')
@ commands.has_any_role(*admin)
async def say(self, channel: discord.TextChannel=None, *, message):
    await channel.send(message)

@ say.error
async def say_error(ctx, error):
    if isinstance(error, commands.MissingAnyRole):
        embed=discord.Embed(
            title='Missing Permissions!',
            description='If this is an error please contant the server owner.',
            color=0x7B0B87
            )
        await ctx.send(embed=embed)
        return

@ bot.command(name='timeout', aliases=['to', 'mute'])
@ commands.has_any_role(*mod,*admin)
async def timeout(ctx, member: discord.Member=None, time=None, *, reason=None):
    time=humanfriendly.parse_timespan(time)
    hftime=humanfriendly.format_timespan(time)
    channel = modLogs
    if member is None:
        await ctx.send('Please provide a member `!timeout @user#1234 5m reason for timeout`')
        return
    if time is None:
        await ctx.send('Please provide an amount of time `!timeout @user#1234 5m reason for timeout`')
        return
    if reason is None:
        await ctx.send('Please provide a reason `!timeout @user#1234 5m reason for timeout`')
        return
    if member.id == 937271579266678834:
        await ctx.send('<:Pepega:937296750480343090><:Pepega:937296750480343090><:Pepega:937296750480343090>')
        return
    if ctx.author.id == member.id:
        await ctx.send('I think you dropped some braincells <a:modCheck:937296737100501002>')
        return
    if any(role.id in rolelist for role in member.roles):
        await ctx.send('🚫**You cannot mute someone with mute permissions**')
        return
    if time > 2419200:
        embed=discord.Embed(title="🚩__**ERROR**__🚩",
                            description='__**Time limit exceeded**__\n\nMaximum time is 4 weeks', color=0xff0000)
        await ctx.send(embed=embed)
        return
    else:
        await member.timeout(until=discord.utils.utcnow() + datetime.timedelta(seconds=time), reason=reason)
        embed=discord.Embed(title="🤫user has been timed out", color=0xff0000)
        embed.add_field(name="__User__", value=member.mention, inline=False)
        embed.add_field(name="__time__", value=hftime, inline=False)
        embed.add_field(name="__Reason__", value=reason, inline=True)
        await ctx.send(embed=embed)
        await channel.send(embed=embed)

@ timeout.error
async def timeout_error(ctx, error):
    if isinstance(error, commands.MissingAnyRole):
        embed=discord.Embed(
            title='Missing Permissions!',
            description='If this is an error please contant the server owner.',
            color=0x7B0B87
            )
        await ctx.send(embed=embed)
        return
    if isinstance(error, commands.CommandError):
        embed=discord.Embed(title="🚩__**ERROR**__🚩",
                            description='Please follow this format. Maximum time for a mute is 4 weeks \n\n`!timeout @user#1345 60s/1m/1w Reason for muting`', color=0xff0000)
        await ctx.send(embed=embed)
        return


@ bot.command(name='untimeout', aliases=['uto', 'unmute'])
@ commands.has_any_role(*mod,*admin)
async def untimeout(ctx, member: discord.Member=None, *, reason=None):
    channel = modLogs
    if member is None:
        await ctx.send('Please provide a member `!untimeout @user#1234 reason for removing timeout`')
        return
    if reason is None:
        await ctx.send('Please provide a reason `!untimeout @user#1234 reason for removing timeout`')
        return
    if member.id == 937271579266678834:
        await ctx.send('Im not timed out')
        return
    if ctx.author.id == member.id:
        await ctx.send('You are not timed out')
        return
    if any(role.id in rolelist for role in member.roles):
        await ctx.send('🚫**They are not timed out**')
        return
    else:
        await member.timeout(until=None, reason=reason)
        embed=discord.Embed(title="😳Timeout removed", color=0xff0000)
        embed.add_field(name="__User__", value=member.mention, inline=False)
        embed.add_field(name="__Reason__", value=reason, inline=True)
        await ctx.send(embed=embed)
        await channel.send(embed=embed)

@ untimeout.error
async def untimeout_error(ctx, error):
    if isinstance(error, commands.MissingAnyRole):
        embed=discord.Embed(
            title='Missing Permissions!',
            description='If this is an error please contant the server owner.',
            color=0x7B0B87
            )
        await ctx.send(embed=embed)
        return
    if isinstance(error, commands.CommandError):
        embed=discord.Embed(title="🚩__**ERROR**__🚩",
                            description='uh oh stinky`', color=0xff0000)
        await ctx.send(embed=embed)
        

bot.run('TOKEN HERE')
