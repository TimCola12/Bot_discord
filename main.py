import discord
from discord.ext import commands
import mysql.connector
import os

# Configuration du bot
token_secret = os.environ['token']
passwd = os.environ['password']
# Configuration de la base de données
DB_HOST = 'sql2.minestrator.com'
DB_USER = 'minesr_NyxktWQ4'
DB_PASSWORD = passwd
DB_NAME = 'nom_de_ta_base_de_donnees'

# Create a new instance of the Bot class
intents = discord.Intents.default()  # Set default intents
intents.members = True  # Enable the member intent if you need to access member information
bot = commands.Bot(command_prefix='!', intents=intents)


# Fonction de connexion à la base de données
def connect_db():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

# Classe pour gérer les étapes de saisie des informations utilisateur
class AjoutTechnique(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.user_data = {}

    @commands.command(name='technique_add')
    async def technique_add(self, ctx):
        """Débute le processus d'ajout d'une technique en demandant des informations étape par étape."""

        # Demande le nom
        await ctx.send("Quel est le nom de ta technique ?")
        self.user_data[ctx.author.id] = {'step': 'noms', 'data': {}}

        # Définir une attente de 60 secondes pour chaque étape
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        try:
            # Obtenir le nom
            msg = await self.bot.wait_for('message', check=check, timeout=300)
            self.user_data[ctx.author.id]['data']['noms'] = msg.content
            await ctx.send("Quel est le nom plugin de ta technique ? Comme par exemplee chinoike_ketsuryugan")

            # Obtenir le nom de plugin
            msg = await self.bot.wait_for('message', check=check, timeout=300)
            self.user_data[ctx.author.id]['data']['nameInPlugin'] = msg.content
            await ctx.send("Quel est la description de ta technique ?")

            # Obtenir la description de la technique
            msg = await self.bot.wait_for('message', check=check, timeout=300)
            self.user_data[ctx.author.id]['data']['description'] = msg.content
            await ctx.send("Quel est le rang de ta technique ?")


            # Obtenir le rang de la technique 
            msg = await self.bot.wait_for('message', check=check, timeout=300)
            self.user_data[ctx.author.id]['data']['level'] = msg.content
            await ctx.send("Quel est le type de ta technique ? (Katon, Denki...)")


            # Obtenir le type de la technique (Katon, Chinoike etc...)
            msg = await self.bot.wait_for('message', check=check, timeout=300)
            self.user_data[ctx.author.id]['data']['type'] = msg.content

            

            # Récupération des données
            data = self.user_data[ctx.author.id]['data']
            del self.user_data[ctx.author.id]

            # Connexion à la base de données et insertion
            db = connect_db()
            cursor = db.cursor()
            requete = "INSERT INTO utilisateurs (noms, nameInPlugin, description, level, type) VALUES (%s, %s, %s, %s, %s)"
            valeurs = (data['nom'], data['nameInPlugin'], data['description'], data['level' ], data['type'])
            cursor.execute(requete, valeurs)
            db.commit()

            # Confirmation
            await ctx.send(f"L'utilisateur {data['nom']} a été ajouté avec succès.")

        except mysql.connector.Error as err:
            await ctx.send(f"Erreur lors de l'insertion dans la base de données : {err}")
        except Exception as e:
            await ctx.send("Temps écoulé ou erreur. Veuillez recommencer la commande.")
        finally:
            # Nettoyage
            cursor.close()
            db.close()
            if ctx.author.id in self.user_data:
                del self.user_data[ctx.author.id]

# Ajouter le cog au bot
bot.add_cog(AjoutTechnique(bot))
# Lancer le bot
bot.run(token_secret)