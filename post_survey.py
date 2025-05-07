import discord
import os
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv("TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
ROLE_ID = int(os.getenv("ROLE_ID"))
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
    message = await channel.send(f"<@&{ROLE_ID}>Tu viens jouer ce soir ? Votez avec :\n👍 Oui\n👎 Non\n❓ Peut-être")

    # Ajouter les réactions
    await message.add_reaction('👍')
    await message.add_reaction('👎')
    await message.add_reaction('❓')

client.run(TOKEN)
