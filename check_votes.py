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

    guild = client.get_guild(int(GUILD_ID))
    channel = guild.get_channel(int(CHANNEL_ID))
    messages = await channel.history(limit=10).flatten()

    # Trouve le dernier message de sondage
    message = None
    for msg in messages:
        if msg.author == client.user and msg.content.startswith("Tu viens jouer ce soir ?"):
            message = msg
            break

    if message:
        thumbs_up_users = []
        for reaction in message.reactions:
            if str(reaction.emoji) == '👍':
                users = await reaction.users().flatten()
                # On enlève le bot de la liste s’il a réagi
                thumbs_up_users = [user for user in users if not user.bot]

        count = len(thumbs_up_users)

        if count > 0:
            user_mentions = "\n".join(user.mention for user in thumbs_up_users)
            await channel.send(f"**{count} personne{'s' if count > 1 else ''} présente{'s' if count > 1 else ''} ce soir :**\n{user_mentions}")
        else:
            await channel.send("Personne n'a encore réagi avec 👍.")

    await client.close()

client.run(TOKEN)
        # Affiche les résultats
        await channel.send(f"**Présents :**\n" + "\n".join(thumbs_up) if thumbs_up else "Aucun présent.\n")
        await channel.send(f"**Absents :**\n" + "\n".join(thumbs_down) if thumbs_down else "Aucun absent.\n")
        await channel.send(f"**Indécis :**\n" + "\n".join(unsure) if unsure else "Aucun indécis.\n")

client.run(TOKEN)
