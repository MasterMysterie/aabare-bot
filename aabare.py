import discord, asyncio

#--Bot things--
client = discord.Client(intents=discord.Intents.all())
token_txt = open("aabaretoken.txt", "r")
TOKEN = token_txt.read()

#--Info--
#Mysterie's Server
mysterie_guild_id = 942534739464699975

mysterie_general_id = 942534740240642151
mysterie_bot_commands_id = 1109134687139536906

#MasterMysterie's bot test server
test_guild_id = 1049772782654849074

test_general_id = 1049772783174955101

#Users
mysterie_id = 356485753406226432

#Magic James Shit
def pad(s):
    return "0" * (6 - len(s)) + s

#Chat-whitelist
whitelist = [mysterie_general_id, mysterie_bot_commands_id, test_general_id]

#--Startup--
@client.event
async def on_ready():
    print("ready")

#--Message--
@client.event
async def on_message(message):
    #checking it doesn't respond to itself
    if message.author == client.user:
        return
    #checking it is in a whitelisted channel
    if message.channel.id not in whitelist:
        return

    msg = message.content.lower()
    #hi command
    if msg.startswith(";hi"):
        await message.channel.send("hello!")

    if msg.startswith(";aabare"):
        await message.channel.send("AABARE!")

    #custom colour role command
    if msg.startswith(";namecolour") or msg.startswith(";namecolor"):
        g = message.guild
        try:
            colour = int(msg.split(" ")[1].replace("0x", "").strip("#"), 16)
            assert colour > 0 and colour <= 0xFFFFFF
        except:
            await message.channel.send("Invalid colour. Please provide a valid hex-code.")
            return

        
        role = None
        for r in g.roles:
            if r.name == pad(hex(colour)[2:]):
                role = r

        if role is None:
            role = await g.create_role(name="hex-{}".format(pad(hex(colour)[2:])), colour=colour)
            await g.edit_role_positions({role: g.me.top_role.position - 1})

        await message.author.add_roles(role)

        for hex_role in message.author.roles:
            hex_name = hex_role.name
            if hex_name.startswith("hex-") and hex_role != role:
                await message.author.remove_roles(hex_role)
                
            empty = True
            for member in g.members:
                if hex_role in member.roles:
                    empty = False
            if empty:
                await hex_role.delete()
            
        await message.channel.send("Done!")

    #help/commands command
    if msg.startswith(";help") or msg.startswith(";commands"):
        embedHelp = discord.Embed(title="Commands for aabare-bot", colour=0x100030)
        embedHelp.add_field(name="", value=";help/commands - Well.. you're looking at it.\n;hi - hello!\n;namecolour/namecolor [hex-code] - Change the colour of your name to a given hex-value.")
        await message.channel.send(embed=embedHelp)

#--Run Client--
client.run(TOKEN)
