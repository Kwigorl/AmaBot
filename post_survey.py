import discord
import os
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv("TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
ROLE1_ID = int(os.getenv("ROLE1_ID"))
ROLE2_ID = int(os.getenv("ROLE2_ID"))
ROLE3_ID = int(os.getenv("ROLE3_ID"))
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

    # Récupère le canal où envoyer le message
    guild = client.get_guild(int(GUILD_ID))
    channel = guild.get_channel(int(CHANNEL_ID))

    # Envoie un message avec les réactions
    message = await channel.send(f"🎲 **Tu viens jouer ce soir ?** <@&{ROLE1_ID}>\n\n👍 Oui    👎 Non   ❓ Peut-être\n\u200B")

    # Ajouter les réactions
    await message.add_reaction('👍')
    await message.add_reaction('👎')
    await message.add_reaction('❓')

client.run(TOKEN)
