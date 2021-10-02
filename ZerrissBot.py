from discord.ext import commands, tasks
import discord, time, os, sys, asyncio, random, aiohttp, string
from discord.ext.commands import has_permissions
from asyncio import sleep as s
from requests import get
import json

prefix = "."
bot = commands.Bot(command_prefix=prefix)
bot.remove_command('help')




@bot.event
async def on_ready():
    print("Bot is ready!")
    bot.loop.create_task(status_task())

@bot.event
async def status_task():
   while True:
       await bot.change_presence(activity=discord.Game(name="Coded by argk#9665"))
       await asyncio.sleep(10)
       await bot.change_presence(activity=discord.Game(name=".help"))
       await asyncio.sleep(10)

@bot.event
async def on_message(ctx):

    print(f"The message's content was: [{ctx.author.name}] sagte [{ctx.content}] auf dem Server [{ctx.guild}]")
    await bot.process_commands(ctx)



@bot.command()
async def kick(ctx, member: discord.Member, *, reason):
    if ctx.author.permissions_in(ctx.channel).kick_members:
        await member.kick(reason=reason)
        embed = discord.Embed(title='Successfully kicked!',
                                description=f'{member.name}#{member.discriminator} was Successfully kicked from '
                                            f'this server\n '
                                            f'Reason: {reason}',
                                color=0x22a7f0)
        await ctx.send(embed=embed)
    else:
        embed=discord.Embed(title="Error", description="Du hast keine Permission ,diesen Command auszuführen", color=0xff6600)
        await ctx.send(embed=embed)

@bot.command()
async def modhelp(ctx):
    embed = discord.Embed(title=f'**Du brauchst hilfe **{ctx.author.name}?',
                            description=f'**Diese Befehle können nur von mods und höher ausgefführt werden**\n'
                                        f'**ban [member]**-bannt einen Member\n'
                                        f'**kick [member]**-kickt einen Member\n'
                                        f'**clear [anzahl]**-löscht Nachrichten\n'
                                        f"**unban [member mit tag]**-Entbannt einen Member\n"
                                        f"**warn [member] [reason]** - warnt einen Member"
                            ,color=0x22a7f0)
    await ctx.send(embed=embed)
    
@bot.command()
async def join(ctx):
  channel = ctx.author.voice.channel
  await channel.connect()

@bot.command()
async def unban(ctx, *, member):
    if ctx.author.permissions_in(ctx.channel).ban_members:
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')
        
    else:
        embed=discord.Embed(title="Error", description="Du hast keine Permission ,diesen Command auszuführen", color=0xff6600)
        await ctx.send(embed=embed)

    for ban_entry in banned_users:
        user = ban_entry.user

    
  
    if (user.name, user.discriminator) == (member_name, member_discriminator):
        await ctx.guild.unban(user)
        embed=discord.Embed(title="**entbannt**", description=f"Du hast {member} entbannt", color=0xff6600)
        await ctx.send(embed=embed)

@bot.command()
async def accept(ctx, member: discord.Member):
    if ctx.author.permissions_in(ctx.channel).ban_members:
      user = await bot.fetch_user(member.id)
      await user.send(f"Hi, \nwir freuen uns, dir mitteilen zu dürfen, dass deine Bewerbung angenommen wurde. Du bist nun Teammitglied des Zerriswave-Networks. Nach einem 14-tägigem Testzeitraum, wo du dein Können unter Beweis stellen kannst, wirst du ein „normales“ Teammitglied. ")

      user =await bot.fetch_user(677850982448889857)
      await user.send(f"{member} wurde akzeptiert")

    else:
      embed=discord.Embed(title="Error", description="Du hast keine Permission ,diesen Command auszuführen",              color=0xff6600) 
      await ctx.send(embed=embed)

@bot.command()
async def declined(ctx, member: discord.Member):
  if ctx.author.permissions_in(ctx.channel).ban_members:
      user = await bot.fetch_user(member.id)
      await user.send(f"Hi,\nes tut uns Leid, dir mitteilen zu müssen, dass deine Bewerbung leider nicht angenommen wurde. ")

      user =await bot.fetch_user(677850982448889857)
      await user.send(f"{member} wurde abgelehnt")

  else:
      embed=discord.Embed(title="Error", description="Du hast keine Permission ,diesen Command auszuführen",              color=0xff6600) 
      await ctx.send(embed=embed)
    
    

@bot.command()
async def help(ctx):
    embed=discord.Embed(title=f"Du brauchst Hilfe {ctx.author}?", description=f"Wenn du alle commands sehen willst, gib **.commands** ein. \n Du willst den Bot auch auf **deinem server** haben? \n link: None", coloor=0xff6600)
    await ctx.send(embed=embed)

@bot.command()
async def restart(ctx):
    if ctx.author.id == 870241231555399692:
        embed=discord.Embed(title="**Restartet**", description=f"Der Bot wurde erfolgreich restartet", color=0xff6600)
        await ctx.send(embed=embed)

        os.execv(sys.executable, ['python'] + sys.argv)
        

    else:
      embed=discord.Embed(title="Error", description="Du hast keine Permission ,diesen Command auszuführen",              color=0xff6600) 
      await ctx.send(embed=embed)
    
@bot.command()
async def commands(ctx):
    embed=discord.Embed(title=f"Du willst alle commands sehen {ctx.author}?\n Hier sind sie:", description=f"\n**Für moderations-commands gib .modhelp ein**\n.msg [username] [message] - sendet eine DM an die gegebene Person\n.ping - zeigt dir den Ping zum Bot-host\n.meme - Gibt dir ein lustiges Meme", color=0xff6600 )
    await ctx.send(embed=embed)

@bot.command()
async def ban(ctx, member : discord.Member, *, reason=None):
    if ctx.author.permissions_in(ctx.channel).ban_members:
        await member.ban(reason=reason)
        embed=discord.Embed(title="**Banned**", description=f"Du hast {member} gebannt", color=0xff6600)
        await ctx.send(embed=embed)
    else:
        embed=discord.Embed(title="Error", description="Du hast keine Permission ,diesen Command auszuführen", color=0xff6600)
        await ctx.send(embed=embed)

@bot.command()
async def warn(ctx, member : discord.Member, *, reason=None):
    if ctx.author.permissions_in(ctx.channel).ban_members:
        embed=discord.Embed(title="**Warned**", description=f"Du hast {member} gewarnt", color=0xff6600)
        await ctx.send(embed=embed)


        user = await bot.fetch_user(677850982448889857)
        await user.send(f"[{member}] wurde von [{ctx.author}] wegen [{reason}] gewarnt")


    else:
        embed=discord.Embed(title="Error", description="Du hast keine Permission ,diesen Command auszuführen", color=0xff6600)
        await ctx.send(embed=embed)


@bot.command(pass_context=True, description="schreibt eine message per dm an einen Member")
async def msg(ctx,  member : discord.Member, *, msg):
    user = await bot.fetch_user(member.id)
    await user.send(msg)
    await ctx.channel.purge(limit=1)



@bot.command()
async def ping(ctx):
    if round(bot.latency * 1000) <= 50:
            embed=discord.Embed(title="PING", description=f":ping_pong: The ping is **{round(bot.latency *1000)}** milliseconds!", color=0x44ff44)
    elif round(bot.latency * 1000) <= 100:
            embed=discord.Embed(title="PING", description=f":ping_pong: The ping is **{round(bot.latency *1000)}** milliseconds!", color=0xffd000)
    elif round(bot.latency * 1000) <= 200:
            embed=discord.Embed(title="PING", description=f":ping_pong: The ping is **{round(bot.latency *1000)}** milliseconds!", color=0xff6600)
    else:
            embed=discord.Embed(title="PING", description=f":ping_pong: The ping is **{round(bot.latency *1000)}** milliseconds!", color=0x990000)
    await ctx.send(embed=embed)

    


    



@bot.command()
async def clear(ctx, amount=2):
    if ctx.author.permissions_in(ctx.channel).kick_members:
        await ctx.channel.purge(limit=amount+1)
        return
    else:
        embed=discord.Embed(title="Error", description="Du hast keine Permission ,diesen Command auszuführen", color=0xff6600)
        await ctx.send(embed=embed)

@bot.event
async def on_command_error(ctx, error):
    embed = discord.Embed(title=f'**Do you need help **{ctx.author.name}?',
                            description=f"**Befehl nicht gefunden \n"
                            f"**Hast du dich vertippt?\n"
                            f"**Wenn du Hilfe brauchst, dann schreib .help!** \n",
                            color=0x990000)
    await ctx.send(embed=embed)




@bot.command()
async def meme(ctx):
    content = get("https://meme-api.herokuapp.com/gimme").text
    data = json.loads(content,)
    meme = discord.Embed(title=f"{data['title']}", Color = discord.Color.random()).set_image(url=f"{data['url']}")
    await ctx.send(embed=meme)



bot.run("DIESISTEINTOKEN")
