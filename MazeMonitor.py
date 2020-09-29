#DISCORD
import discord
from discord.ext import tasks, commands
# GOOGLE SHEETS
import gspread
from oauth2client.service_account import ServiceAccountCredentials
# SCRAPING
import requests
from bs4 import BeautifulSoup as bs
# UTILIDADES
from pprint import pprint

# Credenciais
TOKEN = '' #TOKEN DO BOT DO DISCORD
client = commands.Bot(command_prefix = '.') #PREFIXO DOS COMANDOS
channelID = 0 #ID DO CANAL QUE VAI CHEGAR A NOTIFICAÇÃO
planilha = "" #NOME DA PLANILHA NO DRIVE

# Global variables
itens = {}

# Funções planilha e estoque
def get_itens():
    scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open(planilha).sheet1
    nomes = sheet.col_values(1)
    del nomes[0]
    links = sheet.col_values(2)
    del links[0]
    itens = dict(zip(nomes, links)) 
    return itens

def get_maze(url):
    try:
        payload = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 OPR/68.0.3618.206'} 
        r = requests.get(url,headers=payload)
        soup = bs(r.text, 'html.parser')
        div = soup.find('div', {"class": "variations-wrapper"})
        if div is None:
            return 'indisponivel'
        else:
            sizes_in_stock = []
            avaliable_sizes = div.find_all('label', {"class":"size-box box"})
            for each in avaliable_sizes:
                sizes_in_stock.append(str(each.get_text()))
            return sizes_in_stock         
    except:
        return 'indisponivel'

# Comandos Discord Bot
@client.event
async def on_ready():
    print('bot pronto')
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=".ajuda maze para ver comandos"))

@client.command()
async def ajuda(ctx, ver):
    if (ver == 'maze'):
        embed = discord.Embed(title="Comandos Maze Monitor", description="lista de comandos")
        embed.add_field(name=".start maze", value="começa a monitorar a planilha", inline=False)
        embed.add_field(name=".stop maze", value="para de monitorar a planilha", inline=False)
        embed.add_field(name=".close maze", value="fecha o bot", inline=False)
        await ctx.send(content=None, embed=embed)

@client.command()
async def start(ctx, ver):
    global itens
    if (ver == 'maze'):
        await ctx.send('monitoramento maze iniciado')
        itens = get_itens()
        estoque.start()
        

@client.command()
async def stop(ctx, ver):
    global itens
    if (ver == 'maze'):
        await ctx.send('monitoramento maze parado')
        itens = {}
        estoque.stop()

@tasks.loop(seconds=30)
async def estoque():
    channel = client.get_channel(channelID)

    results = {}
    for nome in itens:
        results.update({nome:get_maze(itens[nome])})

    embed = discord.Embed(title="Resultados", description="")
    for item in results:
        embed.add_field(name=f'{item}', value=f'{results[item]} \n {itens[item]}', inline=False)

    await channel.send(content=None, embed=embed)

@client.command()
async def close(ctx, ver):
    if (ver == 'maze'):
        await ctx.send('bye!')
        await client.close()

client.run(TOKEN)