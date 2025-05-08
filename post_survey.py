import discord
import os
import datetime
from dotenv import load_dotenv

load_dotenv()

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

    # Récupère le jour de la semaine (0 = lundi, 1 = mardi, ..., 6 = dimanche)
    today = datetime.datetime.now().weekday()

    if today == 2:  # Mercredi
        role_id = ROLE1_ID
    elif today == 4:  # Vendredi
        role_id = ROLE2_ID
    elif today == 6:  # Dimanche
        role_id = ROLE3_ID
    else:
        print("Ce n’est ni mercredi, ni vendredi, ni dimanche — aucun message envoyé.")
        await client.close()
        return

    guild = client.get_guild(int(GUILD_ID))
    channel = guild.get_channel(int(CHANNEL_ID))

    message = await channel.send(
        f"🎲 [SONDAGE] **Tu viens jouer aujourd'hui ?** <@&{role_id}>\n\n👍 Oui    👎 Non   ❓ Peut-être\n\u200B"
    )

    await message.add_reaction('👍')
    await message.add_reaction('👎')
    await message.add_reaction('❓')

    await client.close()

client.run(TOKEN)
