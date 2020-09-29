#DISCORD
import discord
from discord.ext import tasks, commands
# GOOGLE SHEETS
import gspread
from oauth2client.service_account import ServiceAccountCredentials
# SCRAPING
import requests
from bs4 import BeautifulSoup as bs
import re
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
def get_id(url):
    if 'calendario-sneaker' in url:
        try:
            r = requests.get(url)
            soup = bs(r.text, 'html.parser')
            div = soup.find('div', {"class": "id-prod"})
            id = div.text
            return id
        except:
            return '0'
    else:
        r = requests.get(url).text
        id = re.search(r'"productId":"(.*?)"', r).group(1)
        return id

def get_itens():
    scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open(planilha).sheet1
    nomes = sheet.col_values(1)
    del nomes[0]
    links = sheet.col_values(2)
    del links[0]
    ids = []
    for url in links:
        ids.append([get_id(url),url])
    itens = dict(zip(nomes, ids))
    return itens

def get_artwalk(id):
    r = requests.get(f'https://www.artwalk.com.br/api/catalog_system/pub/products/variations/{id}').text
    if 'not found' in r:
        return 'indisponivel'
    else:
        sizes = re.findall(r'dimensions":{"Tamanho":"(.*?)"', r)
        disponibilidade = re.findall(r'},"available":(.*?),', r)
        skus = re.findall(r'"sku":(.*?),', r)
        sku_links = []
        for sku in skus:
            sku_links.append(f'https://www.artwalk.com.br/checkout/cart/add?sku={sku}&qty=1&seller=1&redirect=true&sc=1')
        sizes_disponibilidade = dict(zip(sizes, disponibilidade))
        for key in [key for key in sizes_disponibilidade if sizes_disponibilidade[key] == 'false']: del sizes_disponibilidade[key]
        sizes_avaliable = list(sizes_disponibilidade.keys())
        sizes_skus = dict(zip(sizes, sku_links))
        sizes_skus_available = {}
        for tamanho in sizes_avaliable:
            sizes_skus_available.update({tamanho : sizes_skus[tamanho]})
        if sizes_skus_available == {}:
            return 'indisponivel'
        else:
            return sizes_skus_available

# Comandos Discord Bot
@client.event
async def on_ready():
    print('bot pronto')
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=".ajuda artwalk para ver comandos"))

@client.command()
async def ajuda(ctx, ver):
    if (ver == 'artwalk'):
        embed = discord.Embed(title="Comandos Artwalk Monitor", description="lista de comandos")
        embed.add_field(name=".start artwalk", value="começa a monitorar a planilha", inline=False)
        embed.add_field(name=".stop artwalk", value="para de monitorar a planilha", inline=False)
        embed.add_field(name=".close artwalk", value="fecha o bot", inline=False)
        await ctx.send(content=None, embed=embed)

@client.command()
async def start(ctx, ver):
    global itens
    if (ver == 'artwalk'):
        await ctx.send('monitoramento artwalk iniciado')
        itens = get_itens()
        estoque.start()

@client.command()
async def stop(ctx, ver):
    global itens
    if (ver == 'artwalk'):
        await ctx.send('monitoramento artwalk parado')
        itens = {}
        estoque.stop()

@tasks.loop(seconds=30)
async def estoque():
    channel = client.get_channel(channelID)

    results = {}
    for item in itens:
        id_link = itens[item]
        if (id_link[0] == '0'):
            verify = get_id(id_link[1])
            if (verify == '0'):
                results.update({item:'indisponivel'})
            else:
                results.update({item:get_artwalk(id_link[0])})
        else:
            results.update({item:get_artwalk(id_link[0])})

    embed = discord.Embed(title="Resultados", description="")
    for nome in results:
        if (results[nome] == 'indisponivel'):
            embed.add_field(name=f'{nome}', value='indisponivel', inline=False)
        else:
            sizes = results[nome]
            msg = ''
            for size in sizes:
                msg = msg + f'\n {size} : {sizes[size]}'
            embed.add_field(name=f'{nome}', value=msg, inline=False)
    await channel.send(content=None, embed=embed)

@client.command()
async def close(ctx, ver):
    if (ver == 'artwalk'):
        await ctx.send('bye!')
        await client.close()

client.run(TOKEN)