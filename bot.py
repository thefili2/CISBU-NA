import discord
from discord.ext import commands
from discord import app_commands, SelectOption, Interaction, Embed
from discord.ui import View, Select

TOKEN = "MTM4Mzg3NTg2MTExOTM3MzMxMg.G2Ofag._61A8qVu4g_H7439pSTKxJwk2QIdoyRpAnVMXs"

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="/", intents=intents)

# Dizionario prodotti
prodotti = {
    "CISPORCHIAMO": 6.00, "CISBACON": 6.00, "CISNONNA": 6.00, "CISPOLLO": 5.00,
    "CISTÀ": 7.00, "Patatine Normali": 2.00, "Patatine Cheddar e Bacon": 3.00,
    "Drink Fragola": 10.00, "Drink Menta": 10.00, "Drink Limone": 10.00,
    "CocaCola": 5.00, "Acqua": 1.00, "Cappuccino": 2.00, "Mocaccino": 2.00,
    "Latte": 1.00, "Espresso": 2.00, "Americano": 2.00, "Crossiant": 3.00,
    "Bombolone": 3.00, "Torta": 3.00, "Ciambella": 3.00, "Babà": 3.00,
    "Nutella Biscuits": 2.00
}

@bot.event
async def on_ready():
    print(f"✅ Bot connesso come {bot.user}")
    try:
        await bot.tree.sync()
        print("✅ Slash commands sincronizzati.")
    except Exception as e:
        print(f"Errore sync: {e}")

# 📄 /nuovo_turno
@bot.tree.command(name="nuovo_turno", description="Registra un nuovo turno")
@app_commands.describe(
    inizio="Orario di inizio turno",
    fine="Orario di fine turno",
    prova_inizio="Link alla prova inizio (Gyazo o altro)",
    prova_fine="Link alla prova fine (Gyazo o altro)"
)
async def nuovo_turno(interaction: discord.Interaction, inizio: str, fine: str, prova_inizio: str, prova_fine: str):
    embed = discord.Embed(title="📄 Nuovo Turno Registrato", color=discord.Color.blue())
    embed.add_field(name="👤 Utente", value=interaction.user.mention, inline=False)
    embed.add_field(name="🕐 Inizio", value=inizio, inline=True)
    embed.add_field(name="🕔 Fine", value=fine, inline=True)
    embed.add_field(name="🔓 Prova Inizio", value=prova_inizio, inline=False)
    embed.add_field(name="🔒 Prova Fine", value=prova_fine, inline=False)

    await interaction.channel.send(embed=embed)
    await interaction.response.send_message("✅ Turno registrato!", ephemeral=True)

# 🟢 /apri
@bot.tree.command(name="apri", description="Apre il locale")
async def apri(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🟢 Apertura CISBÙ S.R.L",
        description=(
            "**CISBÙ S.R.L è APERTO!**\n\n"
            "🍔 **Prova il nostro menu a bassissimo prezzo!**\n"
            "🍟 **Assaggia le nostre prelibatezze inimitabili!**\n"
            "🎉 **Divertiti con amici e familiari!**\n\n"
            "📍 *Vi aspettiamo con entusiasmo!*"
        ),
        color=discord.Color.green()
    )
    await interaction.channel.send(embed=embed)
    await interaction.response.send_message("✅ Messaggio di apertura inviato!", ephemeral=True)


# 🔴 /chiudi
@bot.tree.command(name="chiudi", description="Chiude il locale")
async def chiudi(interaction: discord.Interaction):
    embed = discord.Embed(title="🔴 Cisbù è CHIUSO", description=f"Chiusura segnalata da {interaction.user.mention}", color=discord.Color.red())
    await interaction.channel.send(embed=embed)
    await interaction.response.send_message("📢 Messaggio di chiusura inviato!", ephemeral=True)

# 💰 /vendita
@bot.tree.command(name="vendita", description="Registra una vendita")
async def vendita(interaction: Interaction):
    class ProductSelect(Select):
        def __init__(self):
            options = [SelectOption(label=nome, value=nome) for nome in prodotti]
            super().__init__(placeholder="📦 Seleziona un prodotto", min_values=1, max_values=1, options=options)

        async def callback(self, i: Interaction):
            nome = self.values[0]
            prezzo = prodotti[nome]
            embed = Embed(
                title="💰 Vendita Registrata",
                description=f"**Prodotto:** {nome}\n**Prezzo:** {prezzo:.2f} €\n**Venduto da:** {interaction.user.mention}",
                color=discord.Color.gold()
            )
            await i.channel.send(embed=embed)
            await i.response.send_message("✅ Vendita registrata!", ephemeral=True)

    view = View()
    view.add_item(ProductSelect())
    await interaction.response.send_message("📦 Seleziona il prodotto venduto:", view=view, ephemeral=True)

# ⭐ /recensione
@bot.tree.command(name="recensione", description="Lascia una recensione")
async def recensione(interaction: Interaction):
    class StarSelect(Select):
        def __init__(self):
            options = [
                SelectOption(label="⭐", value="1"),
                SelectOption(label="⭐⭐", value="2"),
                SelectOption(label="⭐⭐⭐", value="3"),
                SelectOption(label="⭐⭐⭐⭐", value="4"),
                SelectOption(label="⭐⭐⭐⭐⭐", value="5"),
            ]
            super().__init__(placeholder="Seleziona quante stelle vuoi dare", min_values=1, max_values=1, options=options)

        async def callback(self, i: Interaction):
            stelle = self.values[0]

            await i.response.send_modal(RecensioneModal(stelle=stelle))

    class RecensioneModal(discord.ui.Modal, title="Scrivi la tua recensione"):
        def __init__(self, stelle):
            super().__init__()
            self.stelle = stelle

        testo = discord.ui.TextInput(label="La tua recensione", style=discord.TextStyle.paragraph, placeholder="Scrivi qui la tua esperienza...", required=True)

        async def on_submit(self, i: Interaction):
            embed = discord.Embed(
                title="📝 Nuova Recensione",
                description=(
                    f"**Stelle:** {'⭐' * int(self.stelle)}\n"
                    f"**Utente:** {interaction.user.mention}\n\n"
                    f"💬 {self.testo.value}"
                ),
                color=discord.Color.purple()
            )
            await i.channel.send(embed=embed)
            await i.response.send_message("✅ Recensione inviata con successo!", ephemeral=True)

    view = View()
    view.add_item(StarSelect())
    await interaction.response.send_message("⭐ Seleziona il numero di stelle da dare:", view=view, ephemeral=True)


bot.run(TOKEN)
