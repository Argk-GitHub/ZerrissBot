from discord.ext import commands
import discord, time
from discord.ext.commands import has_permissions
import threading

prefix = "."
bot = commands.Bot(command_prefix=prefix)
bot.remove_command("help")

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="Minecraft"))
    print("erfolgreich gestartet")
    








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
        embed = discord.Embed(title=f'ERROR:',
                                description=f"You can't use this command {ctx.author.name}.",
                               color=0x22a7f0)
        await ctx.send(embed=embed)


@bot.command()
async def help(ctx):
    embed = discord.Embed(title=f'**Du brauchst Hilfe **{ctx.author.name}?',
                            description=f'Falls du eine Liste der Commands willst , gibt /commands ein.\n'
                                        f'\n'
                                        f'Du möchtest Metronom auf deinem Server??\n'
                                        f"**Invite Link**: none",
                            color=0x22a7f0)
    await ctx.send(embed=embed)

@bot.command()
async def modhelp(ctx):
    embed = discord.Embed(title=f'**Du brauchst hilfe **{ctx.author.name}?',
                            description=f'**Diese Befehle können nur von mods und höher ausgefführt werden**\n'
                                        f'**ban [member]**-bannt einen Member\n'
                                        f'**kick [member]**-kickt einen Member\n'
                                        f"**shutdown**-Fährt den Bot herunter\n"
                                        f'**clear [anzahl]**-löscht Nachrichten\n'
                                        f"**unban [member mit tag]**-Entbannt einen Member",
                            color=0x22a7f0)
    await ctx.send(embed=embed)
    

@bot.command()
async def unban(ctx, *, member):
    if ctx.author.permissions_in(ctx.channel).ban_members:
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user
  
    if (user.name, user.discriminator) == (member_name, member_discriminator):
        await ctx.guild.unban(user)
        await ctx.send(f"{user} have been unbanned sucessfully")
            



 
 

@bot.command(description="Bannt ein Mitglied bei Regelverstößen")
async def ban(ctx, member : discord.Member, *, reason=None):
    if ctx.author.permissions_in(ctx.channel).ban_members:
        await member.ban(reason=reason)
        await ctx.send(f'banned {member.mention} from the server')



@bot.command()
async def commands(ctx):
    embed = discord.Embed(title=f'**Do you need help **{ctx.author.name}?',
                            description=f'**Der Prefix ist /**\n'
                                        f'**selfinfo**-Zeigt dir die Info von deinem Discord-Account an\n'
                                        f'**userinfo [pinge den User hier]**-Zeigt dir die Info des gepingtenUsers an\n'
                                        f"**msg [userid] [nachricht]**-sendet dem user die Message\n"
                                        f'**botinfo**-Gibt dir Daten über dem Bot\n'
                                        f'**patchnotes**-Zeigt dir die neuen Funktionen des Bots\n'
                                        f'**ping**-Zeigt dir die Verbindung zum Bot\n'                            
                                        f'**echo** [nachricht]-Wiederholt die gegebene Nachricht\n'
                                        f"**support** -Supportet den Bot!",
                            color=0x990000)
    await ctx.send(embed=embed)



@bot.command(pass_context=True, description="schreibt eine message per dm an einen Member")
async def msg(ctx, userid: str, *, msg):
    user = await bot.fetch_user(userid)
    await user.send(f"{msg}")
    await ctx.channel.purge(limit=1)




@bot.command(description="Zeigt den ping!")
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

@bot.event
async def on_command_error(ctx, error):
    print(error)
    await ctx.send("Sorry , Befehl nicht gefunden")
    await ctx.send("Hast du die Groß-Und Kleinschreibung richtig gemacht?")
    await ctx.send("Hast du Permissions, das zu tun?")
    await ctx.send("/help für alle Befehle")

@bot.command()
async def support(ctx):
    embedAnswer = discord.Embed(color=0x22a7f0)
    embedAnswer.add_field(name='Support', value='React with ✅ to support us!')
    embedAnswer.set_footer(text='- Support')
    msg = await ctx.send(embed=embedAnswer)
    await msg.add_reaction('✅')
    del embedAnswer
    channel = await bot.fetch_channel(846797857880408175)

    await channel.send(f"{ctx.author.name} supportet den sheeshBot")
    embed = discord.Embed(title=f"You wan't to support our projekt?",
                            description=f'If you would like to support our project, you are welcome to create\n'
                                        f'a ticket.\n'
                                        f'Just write "#support" in the first line as a distinguishing mark.',
                            color=0x22a7f0)

bot.run("TOKEN")
