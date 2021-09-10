from discord.ext import commands
import discord, time, os, sys
from discord.ext.commands import has_permissions

prefix = "."
bot = commands.Bot(command_prefix=prefix)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="Minecraft"))
    print("erfolgreich gestartet")
    
@bot.event
async def on_message(ctx):

    print(f"The message's content was: [{ctx.author.name}] sagte [{ctx.content}] auf dem Server [{ctx.guild}]")
    await bot.process_commands(ctx)


@bot.command(description="kickt einen Member")
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

@bot.command(despription="Zeigt dir befehle für Moderator/Höher")
async def modhelp(ctx):
    embed = discord.Embed(title=f'**Du brauchst hilfe **{ctx.author.name}?',
                            description=f'**Diese Befehle können nur von mods und höher ausgefführt werden**\n'
                                        f'**ban [member]**-bannt einen Member\n'
                                        f'**kick [member]**-kickt einen Member\n'
                                        f'**clear [anzahl]**-löscht Nachrichten\n'
                                        f"**unban [member mit tag]**-Entbannt einen Member",
                            color=0x22a7f0)
    await ctx.send(embed=embed)
    

@bot.command(discription="entbannt einen member")
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



@bot.command(description=f"Dieser Command restartet den Bot, kann nur von dem Bot-Owner ausgeführt werden.")
async def restart(ctx):
    if ctx.author.id == 870241231555399692:
        embed=discord.Embed(title="**Restartet**", description=f"Der Bot wurde erfolgreich restartet", color=0xff6600)
        await ctx.send(embed=embed)

        os.execv(sys.executable, ['python'] + sys.argv)
        

    else:
        embed=discord.Embed(title="Error", description="Du hast keine Permission ,diesen Command auszuführen", color=0xff6600)
        await ctx.send(embed=embed)
    
 
 

@bot.command(description="Bannt ein Mitglied bei Regelverstößen")
async def ban(ctx, member : discord.Member, *, reason=None):
    if ctx.author.permissions_in(ctx.channel).ban_members:
        await member.ban(reason=reason)
        embed=discord.Embed(title="**Banned**", description=f"Du hast {member} gebannt", color=0xff6600)
        await ctx.send(embed=embed)
    else:
        embed=discord.Embed(title="Error", description="Du hast keine Permission ,diesen Command auszuführen", color=0xff6600)
        await ctx.send(embed=embed)






@bot.command(pass_context=True, description="schreibt eine message per dm an einen Member")
async def msg(ctx,  member : discord.Member, *, msg):
    user = await bot.fetch_user(member.id)
    await user.send(msg)
    await ctx.channel.purge(limit=1)




@bot.command(description="Zeigt den ping zum bot!")
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

    
        

    



@bot.command(description="Löscht Nachrichten , wenn Permissions da sind")
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
                            f"**Wenn du Hilfe brauchst, dann schreib .help! \n",
                            color=0x990000)
    await ctx.send(embed=embed)


bot.run("NEIN")
