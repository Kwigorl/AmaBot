import discord
import os
import datetime

TOKEN = os.getenv("TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID"))
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))  # Canal des sondages
ALERT_CHANNEL_ID = int(os.getenv("ALERT_CHANNEL_ID"))  # Canal pour les alertes
ROLE_MAITRE_ID = int(os.getenv("ROLE_MAITRE_ID"))

intents = discord.Intents.default()
intents.reactions = True
intents.guilds = True
intents.members = True
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Connecté en tant que {client.user}")

    guild = client.get_guild(GUILD_ID)
    channel = guild.get_channel(CHANNEL_ID)
    alert_channel = guild.get_channel(ALERT_CHANNEL_ID)

    today = datetime.datetime.utcnow().date()

    async for message in channel.history(limit=100):
        if message.created_at.date() == today and "Qui vient jouer" in message.content:
            survey_message = message
            break
    else:
        print("Sondage non trouvé aujourd'hui.")
        await client.close()
        return

    # Chercher les utilisateurs ayant réagi avec "☝️"
    response_users = set()
    for reaction in survey_message.reactions:
        if str(reaction.emoji) == "☝":  # ☝️
            async for user in reaction.users():
                if not user.bot:
                    response_users.add(user.id)

    # Vérifier si un Maître des clés a réagi
    role_maitres = guild.get_role(ROLE_MAITRE_ID)
    maitres_ids = [member.id for member in role_maitres.members]
    maitres_present = any(uid in response_users for uid in maitres_ids)

    if not maitres_present:
        await alert_channel.send(
            f"⚠️ Aucun <@&{ROLE_MAITRE_ID}> n'a indiqué sa présence à la séance du jour ! → {survey_message.jump_url}"
        )
    else:
        print("Au moins un Maitre des clés a répondu.")

    await client.close()

client.run(TOKEN)
