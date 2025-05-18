import discord
import os
import datetime

TOKEN = os.getenv("TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
ROLE1_ID = int(os.getenv("ROLE1_ID"))  # Mercredi
ROLE2_ID = int(os.getenv("ROLE2_ID"))  # Vendredi
ROLE3_ID = int(os.getenv("ROLE3_ID"))  # Dimanche
GUILD_ID = int(os.getenv("GUILD_ID"))

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.guilds = True
intents.members = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Bot connecté en tant que {client.user}')

    # Déterminer le jour actuel
    today = datetime.datetime.utcnow().weekday()  # 0 = Lundi

    if today == 2:  # Mercredi
        role_id = ROLE1_ID
        time_message = "ce soir"
    elif today == 4:  # Vendredi
        role_id = ROLE2_ID
        time_message = "ce soir"
    elif today == 6:  # Dimanche
        role_id = ROLE3_ID
        time_message = "cet après-midi"
    else:
        print("Ce jour ne correspond à aucun rôle prévu.")
        await client.close()
        return

    guild = client.get_guild(GUILD_ID)
    channel = guild.get_channel(CHANNEL_ID)

    message = await channel.send(
        f"🎲 Qui vient jouer {time_message} ? <@&{role_id}>\n\n☝️ Moi    🤔 Peut-être moi    ❌ Pas moi\n\u200B"
    )

    await message.add_reaction('☝️')
    await message.add_reaction('❌')
    await message.add_reaction('❓')

    await client.close()

client.run(TOKEN)
