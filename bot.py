#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
import discord
import random
from discord.ext import commands
import logging
import traceback
import asyncio
import os
from discord import opus
from asyncio import sleep



logging.basicConfig(level='INFO')
bot = commands.Bot(command_prefix='b!')
bot.load_extension("admin")
bot.remove_command('help')
bot.load_extension("music")
OPUS_LIBS = ['libopus-0.x86.dll', 'libopus-0.x64.dll', 'libopus-0.dll', 'libopus.so.0', 'libopus.0.dylib']

def load_opus_lib(opus_libs=OPUS_LIBS):
    if opus.is_loaded():
        return True
    for opus_lib in opus_libs:
        try:
            opus.load_opus(opus_lib)
            return
        except OSError:
            pass
    raise RuntimeError('Could not load an opus lib. Tried %s' % (', '.join(opus_libs)))
load_opus_lib()


@bot.listen()
async def on_error(message, event, *args, **kwargs):
    await ctx.send(':o: | You __don`t__ have acces to this command!')
    
@commands.cooldown(1, 5, commands.BucketType.user)
@bot.command(name='8ball')
async def l8ball(ctx):
    await ctx.send(random.choice(['● It is certain.', '● It is decidedly so.', '● Without a doubt.', '● Yes - definitely.', '● You may rely on it', '● As I see it, yes.', '● Most likely.', '● Outlook good.', '● Yes.', '● Signs point to yes.', '● Reply hazy, try again', '● Ask again later.', '● Better not tell you now.', '● Cannot predict now.', '● Concentrate and ask again.', '● Don`t count on it.', '● My reply is no.', '● My sources say no', '● Outlook not so good.', '● Very doubtful.' ]))

    
@commands.cooldown(1, 5, commands.BucketType.user) 
@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member = None, *, reason = None):
    if member is None:
        await ctx.send(":x: | Please provide a user to kick")
    if member != ctx.author:
        await member.send(f'You just got kicked by **{ctx.message.author}** on ** {ctx.guild.name}** for **{reason}**')
        await member.kick()
        await ctx.send(f':white_check_mark: | **{member}** just got kicked.')


@bot.check
async def botcheck(ctx):
    return not ctx.message.author.bot


@commands.cooldown(1, 5, commands.BucketType.user)     
@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member = None, *, reason = None):
    if member is None:
        await ctx.send(":x: | Please provide a user to ban")
    if member != ctx.author and member != ctx.bot.user:
        await member.send(f'You just got banned by **{ctx.message.author}** on ** {ctx.guild.name}** for **{reason}** ')
        await member.ban()
        await ctx.send(f':white_check_mark: | **{member}** just got banned.')
  
@bot.command(aliases= ["kitten", "kitty"])
async def cat(ctx):
    fp = "cat/{}".format(random.choice(os.listdir("cat")))
    await ctx.send(file=discord.File(fp))    
        
@bot.listen()
async def on_ready():
          print('Logging in as', bot.user.name)
       

@bot.command(aliases= ["clear", "prune", "delete"])
@commands.has_permissions(manage_channels=True)
async def purge(ctx, number : int):
    await ctx.message.delete()
    await ctx.channel.purge(limit=number)
    await ctx.message.channel.send(':thumbsup: | Messages deleted succefully!', delete_after=10)            
         
            

@commands.cooldown(1, 5, commands.BucketType.user)  
@bot.command()
async def help(ctx):
    """Help"""
    em = discord.Embed(title="".format(ctx.guild.name), description="", color=discord.Colour.blue())
    em.set_author(name="Flex Help")
    em.add_field(name="Funny", value='`say,ping,cat,avatar,8ball`', inline=False)
    em.add_field(name="Info", value='`playerinfo,serverinfo,botinfo,lenny,respect`', inline=False)
    em.add_field(name="Moderation", value='`kick,ban,purge`', inline=False)
    em.add_field(name="Music", value='`play,stop,queue,skip,pause,resume,join`', inline=False)
    em.add_field(name="More", value='`feedback,bug`', inline=False)
    em.set_thumbnail(url=ctx.me.avatar_url)
    msg = await ctx.send(embed=em)





@bot.command()
async def feedback(ctx, *, message=None):
    if message is None:
        await ctx.send('Hey, please do `f.feedback <feedback>`')
    if message is not None:
        await bot.get_channel(465463335228407808).send(f'{ctx.author.name} reported: {message}')
        await ctx.send('Your feedback was reported to the team')



@bot.command()
async def bug(ctx, *, message=None):
    if message is None:
        await ctx.send('Hey, please do `f.bug <bug>`')
    if message is not None:
        await bot.get_channel(465462946718547978).send(f'{ctx.author.name} reported: {message}')
        await ctx.message.channel.send('Your problem was reported to the team')


@bot.listen()
async def on_message(message : discord.Message):
    if bot.user.mentioned_in(message):
        await message.channel.send(':sleeping: | You woke me up :( . My prefix is `b!` , for a list of commands type `b!help`', delete_after=10)

@bot.listen()
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        return await ctx.send(f':no_entry: | Hey, You are being ratelimited! Try again in** {int(error.retry_after)} **seconds!', delete_after=5)
    if isinstance(error, commands.CommandNotFound):
        return await ctx.message.add_reaction('\N{BLACK QUESTION MARK ORNAMENT}')
    error = error.__cause__ or error
    tb = traceback.format_exception(type(error), error, error.__traceback__, limit=2, chain=False)
    tb = ''.join(tb)
    fmt = 'Error in command {}\n\n{}:\n\n{}\n'.format(ctx.command, type(error).__name__, tb)
    print(fmt)





@commands.cooldown(1, 5, commands.BucketType.user)
@bot.command()
async def say(ctx, *, message):
    """Make the BOT say what you want"""
    await ctx.message.delete()
    await ctx.send(f' ** {message} ** ')


@bot.command()
@commands.has_permissions(administrator=True)
async def mass(ctx, *, message):
    async def maybe_send(member):
        try:
            await member.send(message)
        finally:
            await ctx.message.delete()

    await asyncio.gather(*[maybe_send(m) for m in ctx.guild.members])


@commands.is_owner()
@bot.command()
async def shutdown(ctx):
    await ctx.send('Shutting down...')
    await sleep(5)
    await ctx.bot.logout()
   


@commands.cooldown(1, 5, commands.BucketType.user)
@bot.command()
async def ping(ctx):
    """Get your MS"""
    em = discord.Embed(title="".format(ctx.guild.name), description="", color=discord.Colour.green())
    em.set_author(name="")
    em.add_field(name="Ping", value='Pong! :ping_pong:', inline=True)
    em.add_field(name="MS", value=f'Took : **{ctx.bot.latency * 1000:,.2f}ms**', inline=True)
    await ctx.send(embed=em)


@commands.cooldown(1, 5, commands.BucketType.user)
@bot.command()
async def avatar(ctx, member: discord.Member=None):
    """Get your info"""
    if member is None:
        member = ctx.author
    em = discord.Embed(title="", color=discord.Colour.blue())
    em.set_author(name=f"{member}'s avatar")
    em.set_image(url=member.avatar_url)
    msg = await ctx.send(embed=em)






@commands.cooldown(1, 5, commands.BucketType.user)
@bot.command()
async def lenny(ctx):
    """Get the lenny face"""
    await ctx.send("( ͡° ͜ʖ ͡° )")

@commands.cooldown(1, 5, commands.BucketType.user)
@bot.command()
async def sinfo(ctx, member: discord.Member=None):
    """Get the server info"""
    if member is None:
        member = ctx.author
    em = discord.Embed(title=f"{ctx.guild.name}'s info", color=discord.Colour.blue())
    em.set_author(name="Server Info")
    em.add_field(name="Name", value=ctx.guild.name)
    em.add_field(name="ID", value=ctx.guild.id)
    em.add_field(name="Owner", value=ctx.guild.owner)
    em.add_field(name="Owner ID", value=ctx.guild.owner.id)
    em.add_field(name="Roles", value=len(ctx.guild.roles))
    em.add_field(name="Members", value=ctx.guild.member_count)
    em.add_field(name="Created", value=ctx.guild.created_at)
    em.set_thumbnail(url=ctx.guild.icon_url)
    msg = await ctx.send(embed=em)



@commands.cooldown(1, 5, commands.BucketType.user)
@bot.command()
async def serverinfo(ctx, member: discord.Member=None):
    """Get the server info"""
    if member is None:
        member = ctx.author
    em = discord.Embed(title=f"{ctx.guild.name}'s info", color=discord.Colour.blue())
    em.set_author(name="Server Info")
    em.add_field(name="Name", value=ctx.guild.name)
    em.add_field(name="ID", value=ctx.guild.id)
    em.add_field(name="Owner", value=ctx.guild.owner)
    em.add_field(name="Owner ID", value=ctx.guild.owner.id)
    em.add_field(name="Roles", value=len(ctx.guild.roles))
    em.add_field(name="Members", value=ctx.guild.member_count)
    em.add_field(name="Created", value=ctx.guild.created_at)
    em.set_thumbnail(url=ctx.guild.icon_url)
    msg = await ctx.send(embed=em)



@commands.cooldown(1, 5, commands.BucketType.user)
@bot.command()
async def respect(ctx):
    """Pay respect"""
    em = discord.Embed(title="".format(ctx.guild.name), description="", color=discord.Colour.green())
    em.set_author(name="")
    em.add_field(name=f"{ctx.author.name}", value='Press :regional_indicator_f: to pay respect', inline=True)
    msg = await ctx.send(embed=em)
    await msg.add_reaction('\N{regional indicator symbol letter f}')


@commands.cooldown(1, 5, commands.BucketType.user)
@bot.command()
async def playerinfo(ctx, member: discord.Member=None):
    """Get your info"""
    if member is None:
        member = ctx.author
    em = discord.Embed(title=f"{member}'s info", color=discord.Colour.blue())
    em.set_author(name="Player info")
    em.add_field(name="Name", value=member.name)
    em.add_field(name="ID", value=member.id)
    em.add_field(name="BOT:", value=member.bot)
    em.add_field(name="Tag", value=member.discriminator)
    em.add_field(name="Top Role", value=member.top_role)
    em.add_field(name="Nick", value=member.nick)
    em.add_field(name="Joined", value=member.joined_at)
    em.set_thumbnail(url=member.avatar_url)
    msg = await ctx.send(embed=em)


@commands.cooldown(1, 5, commands.BucketType.user)
@bot.command()
async def pinfo(ctx, member: discord.Member=None):
    """Get your info"""
    if member is None:
        member = ctx.author
    em = discord.Embed(title=f"{member}'s info", color=discord.Colour.blue())
    em.set_author(name="Player info")
    em.add_field(name="Name", value=member.name)
    em.add_field(name="ID", value=member.id)
    em.add_field(name="BOT:", value=member.bot)
    em.add_field(name="Tag", value=member.discriminator)
    em.add_field(name="Top Role", value=member.top_role)
    em.add_field(name="Nick", value=member.nick)
    em.add_field(name="Joined", value=member.joined_at)
    em.set_thumbnail(url=member.avatar_url)
    msg = await ctx.send(embed=em)


async def presence():
    await bot.wait_until_ready()
    while not bot.is_closed():
        a = 0
        for i in bot.guilds:
            for u in i.members:
                if u.bot == False:
                    a = a + 1

        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='%s servers | b!help' % (len(bot.guilds))))
        await sleep(30)
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='%s users | b!help' % (len(bot.users))))
        await sleep(30)
 


@commands.cooldown(1, 5, commands.BucketType.user)  
@bot.command()
async def binfo(ctx):
    """Get the BOT info"""
    em = discord.Embed(title="".format(ctx.guild.name), description="", color=discord.Colour.blue())
    em.set_author(name="BOT Info")
    em.add_field(name="Name", value=ctx.bot.user.name, inline=True)
    em.add_field(name="ID", value=ctx.bot.user.id, inline=True)
    em.add_field(name="Prefix", value=ctx.bot.command_prefix, inline=True)
    em.add_field(name="Made with", value='Python 3.6.6', inline=True)
    em.add_field(name="Tag:", value=ctx.me.discriminator, inline=True)
    em.add_field(name="Creator", value='<@353967891319619587>', inline=True)
    em.add_field(name="Created at", value=ctx.bot.user.created_at, inline=True)
    em.set_thumbnail(url=ctx.me.avatar_url)
    msg = await ctx.send(embed=em)
        



@commands.cooldown(1, 5, commands.BucketType.user)  
@bot.command()
async def botinfo(ctx):
    """Get the BOT info"""
    em = discord.Embed(title="".format(ctx.guild.name), description="", color=discord.Colour.blue())
    em.set_author(name="BOT Info")
    em.add_field(name="Name", value=ctx.bot.user.name, inline=True)
    em.add_field(name="ID", value=ctx.bot.user.id, inline=True)
    em.add_field(name="Prefix", value=ctx.bot.command_prefix, inline=True)
    em.add_field(name="Made with", value='Python 3.6.6', inline=True)
    em.add_field(name="Tag:", value=ctx.me.discriminator, inline=True)
    em.add_field(name="Creator", value='<@353967891319619587>', inline=True)
    em.add_field(name="Created at", value=ctx.bot.user.created_at, inline=True)
    em.set_thumbnail(url=ctx.me.avatar_url)
    msg = await ctx.send(embed=em)
        






bot.loop.create_task(presence())
bot.run(os.getenv("TOKEN"))
